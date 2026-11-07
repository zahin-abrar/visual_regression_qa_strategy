"""empty_feed Android real-UI screenshot test (successful zero-item fixture fetch).

Not offline/error coverage: the app exposes qa-empty-feed-ready only after its
single configured synthetic source resolved successfully with []. Never creates
a golden automatically.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

import pytest

from visualqa.image_diff import compare_png, write_result

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = "empty_feed"
EXPECTED_MESSAGE = (
    "Keine Ergebnisse. Versuche es später erneut oder erweitere deine Feeds in den Einstellungen."
)


@pytest.mark.visual
@pytest.mark.qa_scenario(SCENARIO)
def test_empty_feed_android_state_matches_reviewed_golden(qa_scenario):
    profile = os.environ.get("VVP_GOLDEN_PROFILE", "pixel10-api37")
    if not re.fullmatch(r"[a-z0-9_-]+", profile):
        pytest.fail("VVP_GOLDEN_PROFILE must contain only lowercase letters, digits, _ and -")
    output = ROOT / "artifacts" / "android" / profile
    output.mkdir(parents=True, exist_ok=True)
    baseline = ROOT / "baselines" / "android" / profile / f"{SCENARIO}.png"
    actual = output / f"{SCENARIO}.actual.png"
    diff = output / f"{SCENARIO}.diff.png"
    metrics = output / f"{SCENARIO}.comparison.json"

    from visualqa.android import make_driver, save_diagnostics
    from visualqa.screens.home_screen import HomeScreen

    driver = make_driver(qa_scenario)
    try:
        try:
            from visualqa.scenario_launch import wait_for_scenario_identity
            wait_for_scenario_identity(driver, SCENARIO)
            state = HomeScreen(driver).empty_feed_state
            # Readiness = successful empty fetch + loading finished + layout.
            state.wait_until_ready()
            assert state.effective_theme == "light"
            rect = state.wait_for_stable_layout()
            message = state.message
            assert message == EXPECTED_MESSAGE, f"Empty-state message mismatch: {message!r}"
            residue = state.residue()
            assert residue == dict.fromkeys(residue, 0), f"Stale/loading UI in empty feed: {residue}"
            actual.write_bytes(state.capture_screenshot())
            (output / f"{SCENARIO}.hierarchy.xml").write_text(driver.page_source, encoding="utf-8")
            (output / f"{SCENARIO}.capture.json").write_text(json.dumps({
                "scenario": SCENARIO, "identity": "qa-scenario:empty_feed",
                "ready_id": state.READY_ID, "theme": state.effective_theme,
                "message": message, "rect": rect, "residue": residue,
                "session": driver.session_id,
            }, indent=2), encoding="utf-8")
            # Diagnostic only (dynamic status bar, donation card): never the golden.
            (output / f"{SCENARIO}.context.png").write_bytes(driver.get_screenshot_as_png())
        except Exception:
            save_diagnostics(driver, output)
            raise
    finally:
        try:
            driver.terminate_app(os.environ.get("VVP_ANDROID_PACKAGE", "de.volksverpetzer.app"))
        finally:
            driver.quit()

    assert actual.is_file() and actual.stat().st_size > 0
    if not baseline.is_file():
        pytest.fail(
            "Golden missing. An ACTUAL native screenshot was saved at "
            f"{actual}. Review the image and make a SECOND capture to check stability; "
            f"then manually copy the reviewed PNG to {baseline}. "
            "The test does not silently approve or update baselines."
        )

    result = compare_png(
        baseline, actual, diff,
        channel_tolerance=int(os.environ.get("VVP_CHANNEL_TOLERANCE", "12")),
        max_changed_ratio=float(os.environ.get("VVP_MAX_CHANGED_RATIO", "0.002")),
    )
    write_result(result, metrics)
    assert result.passed, (
        f"Visual regression: changed={result.changed_pixels}/{result.total_pixels} "
        f"({result.changed_ratio:.3%}), allowed={result.max_changed_ratio:.3%}; "
        f"same_size={result.size_match}. Review {actual}, {baseline}, {diff}, {metrics}. "
        "Do NOT auto-regenerate the golden."
    )

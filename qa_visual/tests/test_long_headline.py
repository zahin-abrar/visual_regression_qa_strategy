"""One Android real-UI screenshot test; never creates a golden automatically."""

from __future__ import annotations

import os
import re
from pathlib import Path

import pytest

from visualqa.image_diff import compare_png, write_result

ROOT = Path(__file__).resolve().parents[1]
SCENARIO = "long_headline"


@pytest.mark.visual
def test_long_headline_android_card_matches_reviewed_golden():
    profile = os.environ.get("VVP_GOLDEN_PROFILE", "pixel10-api37")
    if not re.fullmatch(r"[a-z0-9_-]+", profile):
        pytest.fail("VVP_GOLDEN_PROFILE must contain only lowercase letters, digits, _ and -")
    output = ROOT / "artifacts" / "android" / profile
    output.mkdir(parents=True, exist_ok=True)
    baseline = ROOT / "baselines" / "android" / profile / f"{SCENARIO}.png"
    actual = output / f"{SCENARIO}.actual.png"
    diff = output / f"{SCENARIO}.diff.png"
    metrics = output / f"{SCENARIO}.comparison.json"

    # Import Android/Appium only for the integration test; pure comparison tests
    # stay runnable without an Appium installation.
    from visualqa.android import make_driver, save_diagnostics
    from visualqa.screens.home_screen import HomeScreen

    driver = make_driver()
    try:
        try:
            article_card = HomeScreen(driver).article_card
            article_card.wait_until_ready()
            title = article_card.title
            assert "QA-FIXTUR:" in title, f"Fixture title not found: {title!r}"
            actual.write_bytes(article_card.capture_screenshot())
            # Context image demonstrates the card inside the running app.
            # It is *not* used as the golden: status-bar clock is dynamic.
            (output / f"{SCENARIO}.context.png").write_bytes(driver.get_screenshot_as_png())
        except Exception:
            save_diagnostics(driver, output)
            raise
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

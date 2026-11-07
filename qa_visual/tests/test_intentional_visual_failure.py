"""INTENTIONAL visual failure demonstration — expected to FAIL (exit code 1).

This is a reference-mismatch demonstration, not an application UI regression. The
real ``breaking_news`` banner is launched, verified and captured exactly as in
``test_breaking_news.py``, then compared with a deliberately incorrect reference
(``demo_assets/intentional_mismatch_breaking_news.png``, red/blue channels swapped).
The comparator performs a genuine comparison, writes actual/diff/JSON artifacts and
the final assertion fails.

Excluded from default runs by ``addopts = -m "not intentional_failure"`` in
pytest.ini. Run explicitly from qa_visual/:
    python -m pytest tests/test_intentional_visual_failure.py -m intentional_failure -v -s
"""

import json
import os
from pathlib import Path
import re

import pytest

from visualqa.image_diff import compare_png, write_result

EXPECTED_TITLE = "QA-Test: Redaktion meldet wichtige Neuigkeiten zur synthetischen Testausgabe für alle Leserinnen und Leser"
ROOT = Path(__file__).resolve().parents[1]
# Deliberately INCORRECT reference. Not an approved golden; never stored in baselines/.
INTENTIONAL_MISMATCH_REFERENCE = ROOT / "demo_assets/intentional_mismatch_breaking_news.png"
ARTIFACT_PREFIX = "intentional_failure"


@pytest.mark.intentional_failure
@pytest.mark.qa_scenario("breaking_news")
def test_breaking_news_banner_against_intentionally_wrong_reference(qa_scenario):
    from visualqa.android import make_driver, save_diagnostics
    from visualqa.scenario_launch import wait_for_scenario_identity
    from visualqa.screens.home_screen import HomeScreen

    if not INTENTIONAL_MISMATCH_REFERENCE.is_file():
        pytest.fail(f"Demo reference missing: {INTENTIONAL_MISMATCH_REFERENCE}")
    profile = os.environ.get("VVP_GOLDEN_PROFILE", "pixel10-api37")
    if not re.fullmatch(r"[a-z0-9_-]+", profile):
        pytest.fail("Invalid VVP_GOLDEN_PROFILE")
    output = ROOT / "artifacts/android" / profile
    output.mkdir(parents=True, exist_ok=True)
    actual = output / f"{ARTIFACT_PREFIX}.actual.png"
    driver = make_driver(qa_scenario)
    try:
        wait_for_scenario_identity(driver, "breaking_news")
        banner = HomeScreen(driver).breaking_banner
        banner.wait_until_ready()
        assert banner.title == EXPECTED_TITLE
        png, rect = banner.capture_screenshot()
        actual.write_bytes(png)
        (output / f"{ARTIFACT_PREFIX}.context.png").write_bytes(driver.get_screenshot_as_png())
        (output / f"{ARTIFACT_PREFIX}.capture.json").write_text(json.dumps({"scenario": "breaking_news", "identity": "qa-scenario:breaking_news", "title": banner.title, "rect": rect, "session": driver.session_id, "reference": INTENTIONAL_MISMATCH_REFERENCE.relative_to(ROOT).as_posix(), "note": "intentional reference-mismatch demonstration; expected to fail"}, indent=2), encoding="utf-8")
    except Exception:
        save_diagnostics(driver, output)
        raise
    finally:
        try:
            driver.terminate_app(os.environ.get("VVP_ANDROID_PACKAGE", "de.volksverpetzer.app"))
        finally:
            driver.quit()
    print(f"\n[intentional_failure] identity, readiness and title verified; native capture saved: {actual}")
    result = compare_png(INTENTIONAL_MISMATCH_REFERENCE, actual, output / f"{ARTIFACT_PREFIX}.diff.png")
    write_result(result, output / f"{ARTIFACT_PREFIX}.comparison.json")
    print(f"[intentional_failure] comparison: {result.changed_pixels}/{result.total_pixels} changed ({result.changed_ratio:.4%}), limit {result.max_changed_ratio:.2%}")
    assert result.passed, f"INTENTIONAL visual mismatch (demo reference, not an app regression): {result}"

"""Native QA banner capture; a missing golden requires explicit human approval."""

import json
import os
from pathlib import Path
import re

import pytest

from visualqa.image_diff import compare_png, write_result

EXPECTED_TITLE = "QA-Test: Redaktion meldet wichtige Neuigkeiten zur synthetischen Testausgabe für alle Leserinnen und Leser"


@pytest.mark.visual
@pytest.mark.qa_scenario("breaking_news")
def test_breaking_news_banner_matches_reviewed_golden(qa_scenario):
    from visualqa.android import make_driver, save_diagnostics
    from visualqa.scenario_launch import wait_for_scenario_identity
    from visualqa.screens.home_screen import HomeScreen

    profile = os.environ.get("VVP_GOLDEN_PROFILE", "pixel10-api37")
    if not re.fullmatch(r"[a-z0-9_-]+", profile):
        pytest.fail("Invalid VVP_GOLDEN_PROFILE")
    root = Path(__file__).resolve().parents[1]
    output = root / "artifacts/android" / profile
    output.mkdir(parents=True, exist_ok=True)
    actual = output / "breaking_news.actual.png"
    baseline = root / "baselines/android" / profile / "breaking_news.png"
    driver = make_driver(qa_scenario)
    try:
        wait_for_scenario_identity(driver, "breaking_news")
        banner = HomeScreen(driver).breaking_banner
        banner.wait_until_ready()
        assert banner.title == EXPECTED_TITLE
        png, rect = banner.capture_screenshot()
        actual.write_bytes(png)
        (output / "breaking_news.context.png").write_bytes(driver.get_screenshot_as_png())
        (output / "breaking_news.hierarchy.xml").write_text(driver.page_source, encoding="utf-8")
        (output / "breaking_news.capture.json").write_text(json.dumps({"scenario": "breaking_news", "identity": "qa-scenario:breaking_news", "title": banner.title, "rect": rect, "session": driver.session_id}, indent=2), encoding="utf-8")
    except Exception:
        save_diagnostics(driver, output)
        raise
    finally:
        try:
            driver.terminate_app(os.environ.get("VVP_ANDROID_PACKAGE", "de.volksverpetzer.app"))
        finally:
            driver.quit()
    if not baseline.exists():
        pytest.fail(f"Golden missing: review native capture {actual}; no baseline is approved automatically")
    result = compare_png(baseline, actual, output / "breaking_news.diff.png")
    write_result(result, output / "breaking_news.comparison.json")
    assert result.passed, f"Breaking-news visual regression: {result}"

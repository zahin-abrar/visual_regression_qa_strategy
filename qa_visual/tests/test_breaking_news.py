"""Native QA banner capture; a missing golden requires explicit human approval."""

import pytest

from visualqa.android import android_session
from visualqa.scenario_launch import wait_for_scenario_identity
from visualqa.screens.home_screen import HomeScreen
from visualqa.visual_check import VisualArtifacts

EXPECTED_TITLE = (
    'QA-Test: Redaktion meldet wichtige Neuigkeiten zur synthetischen Testausgabe '
    'für alle Leserinnen und Leser'
)


@pytest.mark.visual
@pytest.mark.qa_scenario("breaking_news")
def test_breaking_news_banner_matches_reviewed_golden(qa_scenario: str) -> None:
    artifacts = VisualArtifacts.for_scenario("breaking_news")
    with android_session(qa_scenario, artifacts.output) as driver:
        wait_for_scenario_identity(driver, "breaking_news")
        banner = HomeScreen(driver).breaking_banner
        banner.wait_until_ready()
        assert banner.title == EXPECTED_TITLE
        png, rect = banner.capture_screenshot()
        artifacts.actual.write_bytes(png)
        artifacts.save_context(driver)
        artifacts.save_hierarchy(driver)
        artifacts.save_metadata(
            {
                "scenario": "breaking_news",
                "identity": "qa-scenario:breaking_news",
                "title": banner.title,
                "rect": rect,
                "session": driver.session_id,
            }
        )

    result = artifacts.compare()
    assert result.passed, artifacts.failure_message(result)

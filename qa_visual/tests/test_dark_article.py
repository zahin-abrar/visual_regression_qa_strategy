"""One Android real-UI screenshot test; never creates a golden automatically."""

from __future__ import annotations

import pytest

from visualqa.android import android_session
from visualqa.scenario_launch import wait_for_scenario_identity
from visualqa.screens.home_screen import HomeScreen
from visualqa.visual_check import VisualArtifacts

SCENARIO = "dark_article"
EXPECTED_TITLE = (
    'QA-FIXTUR: Ein absichtlich sehr langer Nachrichtenartikel-Titel prüft den '
    'Zeilenumbruch auf kleinen Smartphone-Bildschirmen'
)


@pytest.mark.visual
@pytest.mark.qa_scenario(SCENARIO)
def test_dark_article_android_card_matches_reviewed_golden(qa_scenario: str) -> None:
    artifacts = VisualArtifacts.for_scenario(SCENARIO)
    with android_session(qa_scenario, artifacts.output) as driver:
        wait_for_scenario_identity(driver, SCENARIO)
        article_card = HomeScreen(driver).article_card
        article_card.wait_until_ready()
        assert article_card.effective_theme == "dark"
        rect = article_card.wait_for_stable_layout()
        title = article_card.title
        assert title == EXPECTED_TITLE, f"Fixture title not found: {title!r}"
        artifacts.actual.write_bytes(article_card.capture_screenshot())
        artifacts.save_hierarchy(driver)
        artifacts.save_metadata(
            {
                "scenario": SCENARIO,
                "identity": "qa-scenario:dark_article",
                "theme": article_card.effective_theme,
                "title": title,
                "rect": rect,
                "session": driver.session_id,
            }
        )
        # Context image demonstrates the card inside the running app.
        # It is *not* used as the golden: status-bar clock is dynamic.
        artifacts.save_context(driver)

    result = artifacts.compare(use_environment_tolerances=True)
    assert result.passed, artifacts.failure_message(result)

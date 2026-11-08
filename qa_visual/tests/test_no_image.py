"""no_image Android real-UI screenshot test (QA-only absent-media fixture); never creates a golden automatically."""

from __future__ import annotations

import pytest

from visualqa.android import android_session
from visualqa.scenario_launch import wait_for_scenario_identity
from visualqa.screens.home_screen import HomeScreen
from visualqa.visual_check import VisualArtifacts

SCENARIO = "no_image"
EXPECTED_TITLE = (
    'QA-FIXTUR: Ein absichtlich sehr langer Nachrichtenartikel-Titel prüft den '
    'Zeilenumbruch auf kleinen Smartphone-Bildschirmen'
)


@pytest.mark.visual
@pytest.mark.qa_scenario(SCENARIO)
def test_no_image_android_card_matches_reviewed_golden(qa_scenario: str) -> None:
    artifacts = VisualArtifacts.for_scenario(SCENARIO)
    with android_session(qa_scenario, artifacts.output) as driver:
        wait_for_scenario_identity(driver, SCENARIO)
        article_card = HomeScreen(driver).no_image_article_card
        # Readiness is text-layout driven (no image onLoad in this scenario).
        article_card.wait_until_ready()
        assert article_card.effective_theme == "light"
        rect = article_card.wait_for_stable_layout()
        image_views = article_card.image_views_in_card()
        assert image_views == [], f"Image panel present in no_image card: {len(image_views)} ImageView(s)"
        assert not HomeScreen(driver).article_card._find_test_id("qa-article-card-ready"), (
            "Image-bearing ready marker must not appear in no_image"
        )
        title = article_card.title
        assert title == EXPECTED_TITLE, f"Fixture title not found: {title!r}"
        artifacts.actual.write_bytes(article_card.capture_screenshot())
        artifacts.save_hierarchy(driver)
        artifacts.save_metadata(
            {
                "scenario": SCENARIO,
                "identity": "qa-scenario:no_image",
                "ready_id": article_card.READY_ID,
                "theme": article_card.effective_theme,
                "title": title,
                "rect": rect,
                "card_image_views": len(image_views),
                "session": driver.session_id,
            }
        )
        # Context image demonstrates the card inside the running app.
        # It is *not* used as the golden: status-bar clock is dynamic.
        artifacts.save_context(driver)

    result = artifacts.compare(use_environment_tolerances=True)
    assert result.passed, artifacts.failure_message(result)

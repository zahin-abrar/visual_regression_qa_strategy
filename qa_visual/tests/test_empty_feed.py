"""empty_feed Android real-UI screenshot test (successful zero-item fixture fetch).

Not offline/error coverage: the app exposes qa-empty-feed-ready only after its
single configured synthetic source resolved successfully with []. Never creates
a golden automatically.
"""

from __future__ import annotations

import pytest

from visualqa.android import android_session
from visualqa.scenario_launch import wait_for_scenario_identity
from visualqa.screens.home_screen import HomeScreen
from visualqa.visual_check import VisualArtifacts

SCENARIO = "empty_feed"
EXPECTED_MESSAGE = (
    "Keine Ergebnisse. Versuche es später erneut oder erweitere deine Feeds in den Einstellungen."
)


@pytest.mark.visual
@pytest.mark.qa_scenario(SCENARIO)
def test_empty_feed_android_state_matches_reviewed_golden(qa_scenario: str) -> None:
    artifacts = VisualArtifacts.for_scenario(SCENARIO)
    with android_session(qa_scenario, artifacts.output) as driver:
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
        artifacts.actual.write_bytes(state.capture_screenshot())
        artifacts.save_hierarchy(driver)
        artifacts.save_metadata(
            {
                "scenario": SCENARIO,
                "identity": "qa-scenario:empty_feed",
                "ready_id": state.READY_ID,
                "theme": state.effective_theme,
                "message": message,
                "rect": rect,
                "residue": residue,
                "session": driver.session_id,
            }
        )
        # Diagnostic only (dynamic status bar, donation card): never the golden.
        artifacts.save_context(driver)

    result = artifacts.compare(use_environment_tolerances=True)
    assert result.passed, artifacts.failure_message(result)

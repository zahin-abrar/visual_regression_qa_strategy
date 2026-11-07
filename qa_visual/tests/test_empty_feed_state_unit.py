from unittest.mock import Mock

import pytest

from visualqa.components.empty_feed_state import EmptyFeedState
from visualqa.screens.home_screen import HomeScreen


def _element(rect=None, label="qa-theme:light", text="Keine Ergebnisse. Versuche es später erneut"):
    element = Mock(rect=rect or {"x": 26, "y": 900, "width": 1028, "height": 200}, text=text)
    element.get_attribute.return_value = label
    element.is_displayed.return_value = True
    return element


@pytest.mark.unit
def test_home_screen_exposes_empty_feed_state():
    state = HomeScreen(Mock()).empty_feed_state
    assert isinstance(state, EmptyFeedState)
    assert state.READY_ID == "qa-empty-feed-ready"


@pytest.mark.unit
def test_missing_ready_marker_fails_instead_of_capturing():
    driver = Mock()
    driver.find_elements.return_value = []
    with pytest.raises(AssertionError, match="qa-empty-feed-ready"):
        EmptyFeedState(driver).capture_screenshot()


@pytest.mark.unit
@pytest.mark.parametrize("label", ["", "qa-theme:", "qa-scenario:empty_feed"])
def test_theme_requires_explicit_marker(label):
    driver = Mock()
    driver.find_elements.return_value = [_element(label=label)]
    with pytest.raises(AssertionError, match="theme marker"):
        _ = EmptyFeedState(driver).effective_theme


@pytest.mark.unit
def test_theme_and_capture_use_ready_region():
    ready = _element()
    ready.screenshot_as_png = b"png"
    driver = Mock()
    driver.find_elements.return_value = [ready]
    state = EmptyFeedState(driver)
    assert state.effective_theme == "light"
    assert state.capture_screenshot() == b"png"


@pytest.mark.unit
def test_residue_counts_every_forbidden_element_kind():
    driver = Mock()
    driver.find_elements.return_value = []
    residue = EmptyFeedState(driver).residue()
    assert residue == {
        "article_markers": 0, "fixture_titles": 0, "breaking_banner": 0,
        "loading_text": 0, "progress_bars": 0, "pending_empty_marker": 0,
    }
    assert driver.find_elements.call_count == len(residue)

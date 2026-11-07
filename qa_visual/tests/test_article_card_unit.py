"""Unit checks for the article-card screenshot target bounds."""

import pytest
from unittest.mock import Mock

from appium.webdriver.common.appiumby import AppiumBy

from visualqa.components.article_card import ArticleCard


class FakeElement:
    def __init__(self, rect, screenshot=b"container-png", parent=None):
        self.rect = rect
        self.screenshot_as_png = screenshot
        self.parent = parent

class FakeDriver:
    def __init__(self, element):
        self.element = element

    def find_elements(self, by, value):
        if by == AppiumBy.ID and value == ArticleCard.READY_ID:
            return [self.element]
        return []

    def find_element(self, by, value):
        assert by == AppiumBy.XPATH
        assert value == f'//*[@resource-id="{ArticleCard.READY_ID}"]/..'
        return self.element.parent


@pytest.mark.unit
def test_capture_screenshot_uses_containing_parent():
    parent = FakeElement({"x": 0, "y": 0, "width": 100, "height": 120})
    ready = FakeElement({"x": 0, "y": 0, "width": 100, "height": 100}, parent=parent)

    screenshot = ArticleCard(FakeDriver(ready)).capture_screenshot()

    assert screenshot == b"container-png"


@pytest.mark.unit
def test_capture_screenshot_rejects_parent_that_does_not_contain_ready_element():
    parent = FakeElement({"x": 5, "y": 0, "width": 100, "height": 120})
    ready = FakeElement({"x": 0, "y": 0, "width": 100, "height": 100}, parent=parent)

    with pytest.raises(AssertionError, match="do not contain"):
        ArticleCard(FakeDriver(ready)).capture_screenshot()


@pytest.mark.unit
def test_capture_screenshot_rejects_parent_without_larger_bottom_extent():
    parent = FakeElement({"x": 0, "y": 0, "width": 100, "height": 100})
    ready = FakeElement({"x": 0, "y": 0, "width": 100, "height": 100}, parent=parent)

    with pytest.raises(AssertionError, match="not below"):
        ArticleCard(FakeDriver(ready)).capture_screenshot()


@pytest.mark.unit
@pytest.mark.parametrize("theme", ["light", "dark"])
def test_effective_theme_reads_rendered_hook_marker(theme):
    card = ArticleCard(Mock())
    element = Mock()
    element.get_attribute.return_value = f"qa-theme:{theme}"
    card._find_test_id = Mock(return_value=element)
    assert card.effective_theme == theme


@pytest.mark.unit
def test_effective_theme_does_not_infer_from_scenario():
    card = ArticleCard(Mock())
    element = Mock()
    element.get_attribute.return_value = ""
    card._find_test_id = Mock(return_value=element)
    with pytest.raises(AssertionError, match="marker missing"):
        _ = card.effective_theme


@pytest.mark.unit
def test_layout_wait_requires_repeated_geometry():
    driver = Mock()
    container = Mock()
    container.rect = {"x": 0, "y": 0, "width": 100, "height": 120}
    driver.find_element.return_value = container
    driver.get_window_size.return_value = {"width": 200, "height": 200}
    title = Mock()
    title.rect = {"x": 5, "y": 5, "width": 80, "height": 40}
    card = ArticleCard(driver)
    card._find_test_id = Mock(return_value=title)
    assert card.wait_for_stable_layout() == container.rect
    assert driver.find_element.call_count == 2

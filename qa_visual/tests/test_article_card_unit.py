"""Unit checks for the article-card screenshot target bounds."""

import pytest

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

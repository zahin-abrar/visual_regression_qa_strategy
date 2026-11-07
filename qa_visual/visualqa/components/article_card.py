"""Appium operations for the article card used by the long-headline scenario."""

from __future__ import annotations

import os

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait


class ArticleCard:
    READY_ID = "qa-article-card-ready"
    TITLE_ID = "qa-article-title"

    def __init__(self, driver):
        self.driver = driver

    def _find_test_id(self, test_id: str):
        # React Native testIDs may be exposed with or without the package prefix.
        package = os.environ.get("VVP_ANDROID_PACKAGE", "de.volksverpetzer.app")
        locators = (
            (AppiumBy.ID, test_id),
            (AppiumBy.ID, f"{package}:id/{test_id}"),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{test_id}")'),
        )
        for by, value in locators:
            try:
                matches = self.driver.find_elements(by, value)
            except WebDriverException:
                # Some UiAutomator2 versions reject a locator spelling.
                continue
            if matches:
                return matches[0]
        return None

    def wait_until_ready(self, timeout: int = 45) -> None:
        """Wait for the app's explicit ready testID to become visible."""
        def ready(_driver):
            element = self._find_test_id(self.READY_ID)
            return element if element and element.is_displayed() else False

        WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(ready)

    @property
    def effective_theme(self) -> str:
        element = self._find_test_id(self.READY_ID)
        if element is None:
            raise AssertionError("Article must be ready before checking effective theme")
        label = element.get_attribute("content-desc") or ""
        if label not in {"qa-theme:light", "qa-theme:dark"}:
            raise AssertionError(f"Effective theme marker missing: {label!r}")
        return label.removeprefix("qa-theme:")

    def wait_for_stable_layout(self, timeout: int = 15) -> dict:
        """Observe unchanged outer/title bounds twice after bundled-image readiness."""
        previous = None

        def settled(_driver):
            nonlocal previous
            container = self.driver.find_element(
                AppiumBy.XPATH, f'//*[@resource-id="{self.READY_ID}"]/..'
            )
            title = self._find_test_id(self.TITLE_ID)
            if title is None:
                return False
            rect, title_rect = container.rect, title.rect
            viewport = self.driver.get_window_size()
            valid = (
                rect["width"] > 0 and rect["height"] > 0
                and 0 <= rect["x"] and 0 <= rect["y"]
                and rect["x"] + rect["width"] <= viewport["width"]
                and rect["y"] + rect["height"] <= viewport["height"]
                and title_rect["width"] > 0 and title_rect["height"] > 0
                and rect["x"] <= title_rect["x"]
                and rect["y"] <= title_rect["y"]
                and title_rect["x"] + title_rect["width"] <= rect["x"] + rect["width"]
                and title_rect["y"] + title_rect["height"] <= rect["y"] + rect["height"]
            )
            state = (rect, title_rect)
            stable = valid and state == previous
            previous = state if valid else None
            return rect if stable else False

        return WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(settled)

    @property
    def title(self) -> str:
        element = self._find_test_id(self.TITLE_ID)
        if element is None:
            raise AssertionError(
                f"Ready article card found but testID={self.TITLE_ID} is missing; inspect page-source XML"
            )
        return element.text or element.get_attribute("text") or ""

    def capture_screenshot(self) -> bytes:
        """Return a screenshot of the ready element's containing card view."""
        ready = self._find_test_id(self.READY_ID)
        if ready is None:
            raise AssertionError(f"Article card testID={self.READY_ID} is missing")
        try:
            parent_selector = f'//*[@resource-id="{self.READY_ID}"]/..'
            container = self.driver.find_element(AppiumBy.XPATH, parent_selector)
        except WebDriverException as error:
            raise AssertionError("Could not resolve the ready article card's direct parent") from error
        if container is None:
            raise AssertionError("Could not resolve the ready article card's direct parent")

        ready_rect = ready.rect
        container_rect = container.rect
        ready_right = ready_rect["x"] + ready_rect["width"]
        ready_bottom = ready_rect["y"] + ready_rect["height"]
        container_right = container_rect["x"] + container_rect["width"]
        container_bottom = container_rect["y"] + container_rect["height"]
        contains_ready = (
            container_rect["x"] <= ready_rect["x"]
            and container_rect["y"] <= ready_rect["y"]
            and container_right >= ready_right
            and container_bottom >= ready_bottom
        )
        if not contains_ready:
            raise AssertionError(
                f"Article card parent bounds {container_rect} do not contain ready element bounds {ready_rect}"
            )
        if container_bottom <= ready_bottom:
            raise AssertionError(
                f"Article card parent bottom {container_bottom} is not below ready element bottom {ready_bottom}"
            )
        return container.screenshot_as_png

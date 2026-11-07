"""Appium operations for the real feed empty-state message region (empty_feed)."""

from __future__ import annotations

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait


class EmptyFeedState:
    """The message region of the app's real EmptyComponent inside the Feed.

    The app exposes READY_ID only after a successful zero-item fixture fetch,
    finished loading/refresh, zero posts and a measured layout. The donation
    card below the message is a separate sibling and is not captured.
    """

    READY_ID = "qa-empty-feed-ready"
    PENDING_ID = "qa-empty-feed"
    MESSAGE_PREFIX = "Keine Ergebnisse."

    def __init__(self, driver):
        self.driver = driver

    def _by_id(self, identifier: str) -> list:
        return self.driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{identifier}")'
        )

    def _ready(self):
        matches = self._by_id(self.READY_ID)
        if not matches:
            raise AssertionError(f"Empty-state testID={self.READY_ID} is missing")
        return matches[0]

    def wait_until_ready(self, timeout: int = 45) -> None:
        def ready(_driver):
            matches = self._by_id(self.READY_ID)
            return matches[0] if matches and matches[0].is_displayed() else False

        WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(
            ready, message=f"{self.READY_ID} (successful empty fetch + layout) never appeared"
        )

    @property
    def effective_theme(self) -> str:
        label = self._ready().get_attribute("content-desc") or ""
        if label not in {"qa-theme:light", "qa-theme:dark"}:
            raise AssertionError(f"Effective theme marker missing: {label!r}")
        return label.removeprefix("qa-theme:")

    def _message_element(self):
        matches = self.driver.find_elements(
            AppiumBy.XPATH,
            f'//*[@resource-id="{self.READY_ID}"]//android.widget.TextView'
            f'[starts-with(@text, "{self.MESSAGE_PREFIX}")]',
        )
        if not matches:
            raise AssertionError("Empty-state message text is not inside the ready region")
        return matches[0]

    @property
    def message(self) -> str:
        element = self._message_element()
        return element.text or element.get_attribute("text") or ""

    def residue(self) -> dict:
        """Count elements that must not exist in a completed successful-empty feed."""
        xpath_counts = {
            "article_markers": '//*[starts-with(@resource-id, "qa-article")]',
            "fixture_titles": '//*[contains(@text, "QA-FIXTUR")]',
            "breaking_banner": '//*[starts-with(@resource-id, "qa-breaking-banner")]',
            "loading_text": '//*[@text="Lade Feed..."]',
            "progress_bars": "//android.widget.ProgressBar",
            "pending_empty_marker": f'//*[@resource-id="{self.PENDING_ID}"]',
        }
        return {
            name: len(self.driver.find_elements(AppiumBy.XPATH, xpath))
            for name, xpath in xpath_counts.items()
        }

    def wait_for_stable_layout(self, timeout: int = 15) -> dict:
        """Observe unchanged region/message bounds twice, fully inside the viewport."""
        previous = None

        def settled(_driver):
            nonlocal previous
            rect, text_rect = self._ready().rect, self._message_element().rect
            viewport = self.driver.get_window_size()
            valid = (
                rect["width"] > 0 and rect["height"] > 0
                and rect["x"] >= 0 and rect["y"] >= 0
                and rect["x"] + rect["width"] <= viewport["width"]
                and rect["y"] + rect["height"] <= viewport["height"]
                and rect["x"] <= text_rect["x"] and rect["y"] <= text_rect["y"]
                and text_rect["x"] + text_rect["width"] <= rect["x"] + rect["width"]
                and text_rect["y"] + text_rect["height"] <= rect["y"] + rect["height"]
            )
            state = (rect, text_rect)
            stable = valid and state == previous
            previous = state if valid else None
            return rect if stable else False

        return WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(settled)

    def capture_screenshot(self) -> bytes:
        """Native element screenshot of the ready message region only."""
        return self._ready().screenshot_as_png

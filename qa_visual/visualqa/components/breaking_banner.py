"""Capture the complete QA banner itself, with measured readiness and bounds."""

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait


class BreakingBanner:
    READY_ID = "qa-breaking-banner-ready"
    TITLE_ID = "qa-breaking-banner-title"

    def __init__(self, driver):
        self.driver = driver

    def _find(self, identifier):
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().resourceId("{identifier}")',
        )

    def wait_until_ready(self, timeout=45):
        previous = None

        def stable(_driver):
            nonlocal previous
            banner = self._find(self.READY_ID)
            rect = banner.rect
            current = tuple(rect[key] for key in ("x", "y", "width", "height"))
            ready = banner.is_displayed() and rect["width"] > 0 and rect["height"] > 0 and current == previous
            previous = current
            return ready

        WebDriverWait(self.driver, timeout, poll_frequency=0.5).until(stable)

    @property
    def title(self):
        return self._find(self.TITLE_ID).text

    def capture_screenshot(self):
        banner = self._find(self.READY_ID)
        rect = banner.rect
        window = self.driver.get_window_size()
        if rect["x"] < 0 or rect["y"] < 0 or rect["x"] + rect["width"] > window["width"] or rect["y"] + rect["height"] > window["height"]:
            raise AssertionError(f"Banner is clipped by the viewport: {rect}")
        for identifier in (self.TITLE_ID, "qa-breaking-banner-label"):
            child = self._find(identifier).rect
            if not (rect["x"] <= child["x"] and rect["y"] <= child["y"] and child["x"] + child["width"] <= rect["x"] + rect["width"] and child["y"] + child["height"] <= rect["y"] + rect["height"]):
                raise AssertionError(f"Banner does not contain {identifier}: {rect}, {child}")
        return banner.screenshot_as_png, rect

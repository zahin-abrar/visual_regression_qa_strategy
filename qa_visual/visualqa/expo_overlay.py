"""Recognise and dismiss the Expo development-client developer-menu onboarding sheet.

The first launch of an Expo development build shows a bottom sheet ("This is the developer menu...")
over the running app. It hides the app's accessibility tree from UiAutomator2, so the scenario marker
cannot be found. Detection uses only the UiAutomator2 hierarchy (no coordinates) and needs several
independent signals; dismissal is a single element click on the sheet's own ``Continue`` control.
"""

from __future__ import annotations

import re
import time
import xml.etree.ElementTree as ET
from collections.abc import Callable
from dataclasses import dataclass

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import WebDriverException

DISAPPEAR_TIMEOUT_S = 8.0   # separately bounded wait after the single click
POLL_INTERVAL_S = 0.5

_ONBOARDING_TEXT = re.compile(r"this is the developer menu", re.IGNORECASE)
_RUNTIME_VERSION = re.compile(r"^Runtime version:\s*\S+", re.IGNORECASE)
CONTINUE_XPATH = ("//android.widget.TextView[@text='Continue']"
                  "/parent::*[@clickable='true']")
CLOSE_XPATH = "//*[@content-desc='Close']/parent::*[@clickable='true']"
_PANEL_SIGNALS = ("Go home", "Reload", "TOOLS", "Fast Refresh", "Open DevTools")


class ExpoOverlayError(WebDriverException):
    """The Expo overlay blocked the app and could not be dismissed safely."""


@dataclass(frozen=True)
class OverlayEvidence:
    onboarding_text: bool = False
    runtime_version: bool = False
    close_labels: int = 0          # elements with content-desc exactly "Close"
    close_clickable: int = 0       # of those, with a clickable parent
    continue_labels: int = 0       # TextViews labelled exactly "Continue"
    continue_clickable: int = 0    # of those, with a clickable parent (the sheet's button)
    panel_signals: int = 0         # distinct dev-menu panel labels (Go home, Reload, TOOLS, ...)

    @property
    def close_control(self) -> bool:
        return self.close_labels > 0

    @property
    def onboarding(self) -> bool:
        """Onboarding explanation + Continue + at least one more Expo-sheet signal."""
        return (self.onboarding_text and self.continue_labels > 0
                and (self.runtime_version or self.close_control))

    @property
    def panel(self) -> bool:
        """The full Expo developer-menu panel: runtime version, Close and >= 2 panel labels."""
        return self.runtime_version and self.close_control and self.panel_signals >= 2

    @property
    def present(self) -> bool:
        return self.onboarding or self.panel

    @property
    def variant(self) -> str:
        return "onboarding" if self.onboarding else "dev-menu-panel"

    @property
    def covering(self) -> bool:
        """Any Expo overlay text at all (used to confirm disappearance and to classify)."""
        return self.onboarding_text or self.panel

    @property
    def unambiguous(self) -> bool:
        if self.onboarding:
            return self.continue_labels == 1 and self.continue_clickable == 1
        return self.panel and self.close_labels == 1 and self.close_clickable == 1

    @property
    def action(self) -> str:
        return "Continue" if self.onboarding else "Close"

    def describe(self) -> str:
        return (f"onboarding_text={self.onboarding_text} runtime_version={self.runtime_version} "
                f"close_labels={self.close_labels} close_clickable={self.close_clickable} "
                f"continue_labels={self.continue_labels} continue_clickable={self.continue_clickable} "
                f"panel_signals={self.panel_signals}")


def inspect_hierarchy(source: str | None) -> OverlayEvidence | None:
    """Evidence from a UiAutomator2 hierarchy; None when it cannot be parsed."""
    if not source:
        return None
    try:
        root = ET.fromstring(source)
    except ET.ParseError:
        return None
    parents = {child: parent for parent in root.iter() for child in parent}
    onboarding = runtime = False
    closes = close_clickable = labels = clickable = 0
    panel = set()
    for node in root.iter():
        text = (node.get("text") or "").strip()
        desc = (node.get("content-desc") or "").strip()
        parent = parents.get(node)
        parent_clickable = parent is not None and parent.get("clickable") == "true"
        if text and _ONBOARDING_TEXT.search(text):
            onboarding = True
        if text and _RUNTIME_VERSION.match(text):
            runtime = True
        for label in (text, desc):
            if label in _PANEL_SIGNALS:
                panel.add(label)
        if desc == "Close":
            closes += 1
            close_clickable += parent_clickable
        if text == "Continue" and (node.get("class") or node.tag).endswith("TextView"):
            labels += 1
            clickable += parent_clickable
    return OverlayEvidence(onboarding, runtime, closes, close_clickable, labels, clickable, len(panel))


def _source(driver) -> str | None:
    try:
        return driver.page_source
    except WebDriverException:
        return None


def dismiss_if_present(driver, evidence: OverlayEvidence, *, clock: Callable[[], float] = time.monotonic,
                       sleep: Callable[[float], None] = time.sleep) -> str:
    """Click the overlay's unique Continue (onboarding) or Close (dev-menu panel) control once.

    Returns a one-line report. Raises ExpoOverlayError when the screen is ambiguous (no click),
    the click fails, or that variant is still visible after DISAPPEAR_TIMEOUT_S (no second click).
    Continuing from onboarding opens Expo's dev-menu panel; that is a separate overlay handled by its own call.
    """
    if not evidence.unambiguous:
        raise ExpoOverlayError(f"Expo overlay is ambiguous; no click made ({evidence.describe()})")
    try:
        targets = driver.find_elements(AppiumBy.XPATH, CONTINUE_XPATH if evidence.onboarding else CLOSE_XPATH)
        if len(targets) != 1:
            raise ExpoOverlayError(
                f"expected exactly one {evidence.action} control, found {len(targets)}; no click made")
        targets[0].click()
    except ExpoOverlayError:
        raise
    except WebDriverException as error:
        raise ExpoOverlayError(f"Expo overlay {evidence.action} click failed: {type(error).__name__}: {error}") from error
    started = clock()
    while True:
        current = inspect_hierarchy(_source(driver))
        if current is not None and not (current.onboarding_text if evidence.onboarding else current.panel):
            return f"dismissed via {evidence.action}; overlay gone after {clock() - started:.1f}s"
        if clock() - started >= DISAPPEAR_TIMEOUT_S:
            raise ExpoOverlayError(
                f"Expo overlay still visible {DISAPPEAR_TIMEOUT_S}s after {evidence.action} click "
                f"(hierarchy {'unavailable' if current is None else current.describe()})")
        sleep(POLL_INTERVAL_S)

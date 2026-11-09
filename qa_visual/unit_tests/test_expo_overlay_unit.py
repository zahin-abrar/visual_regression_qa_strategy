"""Expo developer-menu onboarding: strict recognition, one bounded dismissal, exact marker still required."""

from __future__ import annotations

from unittest.mock import Mock, patch

import pytest
from selenium.common.exceptions import TimeoutException, WebDriverException

from visualqa import android, expo_overlay as eo, launch_diagnostics as ld, scenario_launch as sl

pytestmark = pytest.mark.unit
PKG = "de.volksverpetzer.app"
ID = "breaking_news"


def sheet(*, continues=1, onboarding=True, runtime=True, close=True, clickable=True):
    body = ""
    if runtime:
        body += '<android.widget.TextView text="Runtime version: exposdk:57.0.0" clickable="false" />'
    if close:
        body += '<android.view.View content-desc="Close" clickable="false" />'
    if onboarding:
        body += '<android.widget.TextView text="This is the developer menu. It gives you access to tools." />'
    for _ in range(continues):
        body += (f'<android.view.View clickable="{str(clickable).lower()}">'
                 '<android.widget.TextView text="Continue" clickable="false" />'
                 '<android.widget.Button text="" /></android.view.View>')
    return f"<hierarchy><android.widget.FrameLayout>{body}</android.widget.FrameLayout></hierarchy>"


def panel(*, closes=1, runtime=True, labels=("Go home", "Reload", "TOOLS", "Fast Refresh")):
    body = '<android.widget.TextView text="Runtime version: exposdk:57.0.0" />' if runtime else ""
    for _ in range(closes):
        body += ('<android.view.View clickable="true"><android.view.View content-desc="Close" />'
                 '<android.widget.Button /></android.view.View>')
    body += "".join(f'<android.view.View content-desc="{label}" />' for label in labels)
    return f"<hierarchy>{body}</hierarchy>"


FEED = '<hierarchy><android.widget.TextView text="Lade Feed..." /></hierarchy>'
APP_CONTINUE = ('<hierarchy><android.view.View clickable="true"><android.widget.TextView text="Continue" />'
                '</android.view.View></hierarchy>')


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class Fake:
    """Driver whose screen and marker evolve with (fake) time and clicks."""

    def __init__(self, clock, *, screens, marker_after=None, click_error=None, clicks_remove=True,
                 source_error=False, targets=1):
        self.clock, self.screens, self.marker_after = clock, screens, marker_after
        self.click_error, self.clicks_remove, self.source_error, self.targets = (
            click_error, clicks_remove, source_error, targets)
        self.clicks = 0
        self.cleared = False
        self.marker_visible_at_start = False
        self.session_id = "s"

    @property
    def page_source(self):
        if self.source_error:
            raise WebDriverException("instrumentation not running")
        if self.cleared:
            return FEED
        xml = FEED
        for start, value in self.screens:
            if self.clock.now >= start:
                xml = value
        return xml

    def _overlay_covering(self):
        if self.cleared:
            return False
        xml = FEED
        for start, value in self.screens:
            if self.clock.now >= start:
                xml = value
        evidence = eo.inspect_hierarchy(xml)
        return bool(evidence and evidence.covering)

    def find_elements(self, by, value):
        if value.startswith("qa-scenario:"):
            if self.marker_visible_at_start:
                return [object()]
            ok = (self.marker_after is not None and self.clock.now >= self.marker_after
                  and not self._overlay_covering())
            return [object()] if ok else []
        if value in (eo.CONTINUE_XPATH, eo.CLOSE_XPATH):
            element = Mock()

            def click():
                self.clicks += 1
                if self.click_error:
                    raise self.click_error
                if self.clicks_remove:
                    self.cleared = True
            element.click.side_effect = click
            return [element] * self.targets
        return []


def wait(driver, clock):
    return sl.wait_for_scenario_identity(driver, ID, clock=clock, sleep=clock.sleep)


def test_evidence_present_and_unambiguous():
    evidence = eo.inspect_hierarchy(sheet())
    assert evidence.present and evidence.unambiguous


def test_ordinary_app_continue_button_is_not_the_overlay():
    assert not eo.inspect_hierarchy(APP_CONTINUE).present
    assert not eo.inspect_hierarchy(sheet(onboarding=False)).present
    assert not eo.inspect_hierarchy(sheet(runtime=False, close=False)).present  # one extra signal required


def test_unparseable_or_empty_hierarchy_is_not_evidence():
    assert eo.inspect_hierarchy("<hierarchy") is None and eo.inspect_hierarchy(None) is None


def test_duplicate_continue_controls_are_ambiguous_and_not_clicked():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet(continues=2))], targets=2)
    with pytest.raises(eo.ExpoOverlayError, match="ambiguous"):
        wait(driver, clock)
    assert driver.clicks == 0


def test_non_clickable_continue_is_ambiguous_and_not_clicked():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet(clickable=False))])
    with pytest.raises(eo.ExpoOverlayError, match="ambiguous"):
        wait(driver, clock)
    assert driver.clicks == 0


def test_driver_reports_multiple_targets_no_click():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet())], targets=2)
    with pytest.raises(eo.ExpoOverlayError, match="exactly one"):
        wait(driver, clock)
    assert driver.clicks == 0


def test_overlay_dismissed_once_then_marker_found():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet())], marker_after=0)
    wait(driver, clock)
    assert driver.clicks == 1


def test_overlay_absent_no_interaction():
    clock = Clock()
    driver = Fake(clock, screens=[(0, FEED)], marker_after=3)
    wait(driver, clock)
    assert driver.clicks == 0


def test_marker_already_present_no_dismissal():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet())])
    driver.marker_visible_at_start = True
    wait(driver, clock)
    assert driver.clicks == 0


def test_late_appearing_overlay_is_dismissed():
    clock = Clock()
    driver = Fake(clock, screens=[(0, FEED), (20, sheet())], marker_after=20)
    wait(driver, clock)
    assert driver.clicks == 1 and clock.now >= 20


def test_click_failure_is_reported_and_not_retried():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet())], click_error=WebDriverException("stale"))
    with pytest.raises(eo.ExpoOverlayError, match="click failed"):
        wait(driver, clock)
    assert driver.clicks == 1


def test_overlay_remaining_after_click_fails_within_bounded_wait_without_second_click():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet())], clicks_remove=False)
    with pytest.raises(eo.ExpoOverlayError, match="still visible"):
        wait(driver, clock)
    assert driver.clicks == 1
    assert clock.now <= eo.DISAPPEAR_TIMEOUT_S + 3


def test_dismissed_but_marker_never_appears_times_out_with_original_message_and_bounded():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet())], marker_after=None)
    with pytest.raises(TimeoutException,
                       match="Exact active scenario identity qa-scenario:breaking_news was not exposed") as caught:
        wait(driver, clock)
    assert driver.clicks == 1
    assert any("dismissed via Continue" in n for n in caught.value.__notes__)
    assert clock.now <= sl.SCENARIO_WAIT_S + sl.MAX_DISMISSAL_EXTENSION_S + 1


def test_plain_timeout_without_overlay_keeps_45_second_budget():
    clock = Clock()
    driver = Fake(clock, screens=[(0, FEED)], marker_after=None)
    with pytest.raises(TimeoutException):
        wait(driver, clock)
    assert sl.SCENARIO_WAIT_S <= clock.now < sl.SCENARIO_WAIT_S + 1


def test_overlay_reappearing_after_dismissal_is_not_clicked_again():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet())])
    original = Fake.page_source.fget

    def flaky(self):  # the sheet comes back some seconds after the click
        if self.cleared and self.clock.now > 6:
            return sheet()
        return original(self)

    with patch.object(Fake, "page_source", property(flaky)):
        with pytest.raises(eo.ExpoOverlayError, match="reappeared"):
            wait(driver, clock)
    assert driver.clicks == 1


def test_hierarchy_lookup_failure_does_not_click_and_marker_wait_continues():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet())], marker_after=2, source_error=True)
    driver.screens = [(0, FEED)]  # marker not covered (hierarchy is unreadable, so no overlay decision)
    wait(driver, clock)
    assert driver.clicks == 0


def test_marker_lookup_failure_propagates_when_app_session_dies():
    clock = Clock()
    driver = Mock()
    driver.page_source = FEED
    driver.find_elements.side_effect = WebDriverException("app process exited")
    with pytest.raises(WebDriverException, match="app process exited"):
        wait(driver, clock)


def test_timeout_during_dismissal_interaction_is_reported():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet())], click_error=TimeoutException("click timed out"))
    with pytest.raises(eo.ExpoOverlayError, match="click failed"):
        wait(driver, clock)


def test_app_exits_during_dismissal_surfaces_from_marker_lookup():
    clock = Clock()
    driver = Fake(clock, screens=[(0, sheet())])
    real = driver.find_elements

    def find(by, value):
        if value.startswith("qa-scenario:") and driver.clicks:
            raise WebDriverException("app process exited during dismissal")
        return real(by, value)

    driver.find_elements = find
    with pytest.raises(WebDriverException, match="app process exited"):
        wait(driver, clock)


def test_classification_names_expo_overlay_and_other_screens_stay_independent():
    state, _ = ld.classify(expected=ID, process_running=True, foreground=PKG, package=PKG,
                           hierarchy=sheet(), logcat="")
    assert state == "expo-dev-menu-overlay"
    state, _ = ld.classify(expected=ID, process_running=True, foreground=PKG, package=PKG,
                           hierarchy=FEED, logcat="")
    assert state == "marker-absent-unknown-screen"


def test_overlay_failure_keeps_diagnostics_original_exception_and_allure_attachments(monkeypatch, tmp_path):
    from unit_tests.test_launch_diagnostics_unit import fake_adb, fake_driver

    driver = fake_driver(source=sheet(continues=2))
    driver.find_elements.return_value = []
    monkeypatch.setattr(android.webdriver, "Remote", Mock(return_value=driver))
    monkeypatch.delenv("VVP_QA_LAUNCH_URL", raising=False)
    monkeypatch.setenv("VVP_ANDROID_PACKAGE", PKG)
    with patch.object(ld, "adb", fake_adb()), patch("visualqa.allure_report.attach_launch_diagnostics") as attach:
        with pytest.raises(eo.ExpoOverlayError, match="ambiguous"):
            android.make_driver(ID, diagnostics_dir=tmp_path)
    context = (tmp_path / "launch-context.txt").read_text()
    assert "classification: expo-dev-menu-overlay" in context
    assert "continue_labels=2" in context and "ExpoOverlayError" in context
    assert (tmp_path / "failure-screen.png").is_file() and (tmp_path / "hierarchy.xml").is_file()
    assert attach.call_count == 1
    driver.quit.assert_called_once()


def test_wait_budgets_are_bounded_and_scenario_selection_unchanged():
    assert eo.DISAPPEAR_TIMEOUT_S <= 10 and sl.SCENARIO_WAIT_S == 45 and sl.MAX_DISMISSAL_EXTENSION_S <= 10
    assert sl.SUPPORTED_SCENARIOS == {"long_headline", "breaking_news", "dark_article", "no_image", "empty_feed"}


def test_full_dev_menu_panel_is_dismissed_once_through_its_own_close_control():
    assert eo.inspect_hierarchy(panel()).unambiguous
    clock = Clock()
    driver = Fake(clock, screens=[(0, panel())], marker_after=0)
    wait(driver, clock)
    assert driver.clicks == 1


def test_ordinary_app_close_button_is_not_treated_as_expo_overlay():
    app_close = ('<hierarchy><android.view.View clickable="true"><android.view.View content-desc="Close" />'
                 '</android.view.View></hierarchy>')
    assert not eo.inspect_hierarchy(app_close).present
    assert not eo.inspect_hierarchy(panel(runtime=False)).present
    assert not eo.inspect_hierarchy(panel(labels=("Reload",))).present


def test_duplicate_close_controls_on_panel_are_ambiguous_and_not_clicked():
    clock = Clock()
    driver = Fake(clock, screens=[(0, panel(closes=2))], targets=2)
    with pytest.raises(eo.ExpoOverlayError, match="ambiguous"):
        wait(driver, clock)
    assert driver.clicks == 0


def test_dev_menu_panel_classified_as_expo_overlay_not_generic_error():
    state, _ = ld.classify(expected=ID, process_running=True, foreground=PKG, package=PKG,
                           hierarchy=panel(), logcat="")
    assert state == "expo-dev-menu-overlay"


class Staged:
    """Real Expo flow: onboarding sheet -> (Continue) -> dev-menu panel -> (Close) -> app."""

    def __init__(self, clock, screens, *, marker_at_stage=None):
        self.clock, self.screens, self.marker_at_stage = clock, screens, marker_at_stage
        self.stage = 0
        self.clicked = []
        self.session_id = "s"

    @property
    def page_source(self):
        return self.screens[min(self.stage, len(self.screens) - 1)]

    def find_elements(self, by, value):
        if value.startswith("qa-scenario:"):
            return [object()] if self.stage == self.marker_at_stage else []
        element = Mock()
        element.click.side_effect = lambda: (self.clicked.append(value), setattr(self, "stage", self.stage + 1))
        return [element]


def test_onboarding_continue_then_dev_menu_panel_close_then_marker():
    clock = Clock()
    driver = Staged(clock, [sheet(), panel(), FEED], marker_at_stage=2)
    wait(driver, clock)
    assert driver.clicked == [eo.CONTINUE_XPATH, eo.CLOSE_XPATH]


def test_second_stage_failure_is_reported_and_each_control_clicked_at_most_once():
    clock = Clock()
    driver = Staged(clock, [sheet(), panel()], marker_at_stage=99)  # Close does not remove the panel
    driver.screens = [sheet(), panel(), panel(), panel()]
    with pytest.raises(eo.ExpoOverlayError):
        wait(driver, clock)
    assert driver.clicked.count(eo.CONTINUE_XPATH) == 1 and driver.clicked.count(eo.CLOSE_XPATH) == 1

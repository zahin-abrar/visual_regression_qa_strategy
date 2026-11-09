"""Scenario-launch failure evidence: bounded, best effort, never masks the original error."""

from __future__ import annotations

import time
from unittest.mock import Mock, patch

import pytest
from selenium.common.exceptions import TimeoutException, WebDriverException

from visualqa import android, launch_diagnostics as ld

pytestmark = pytest.mark.unit
PKG = "de.volksverpetzer.app"
URL = "exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=breaking_news"
FEED = '<hierarchy><node content-desc="Startseite" /></hierarchy>'


def fake_adb(*, pid="4242", screencap=b"\x89PNGadb", dump="<hierarchy dump/>", logcat="I/ReactNativeJS: ok\n",
             fail=()):
    """Stand-in for launch_diagnostics.adb; ``fail`` names commands that return an error."""
    calls = []

    def run(args, timeout_s=ld.ADB_TIMEOUT_S, binary=False):
        calls.append(args)
        key = args[1] if args[0] in ("shell", "exec-out") else args[0]
        if key in fail:
            return None, f"adb {key}: timed out after {timeout_s}s"
        if args[:2] == ["shell", "pidof"]:
            return (pid, None) if pid else (None, "adb shell pidof: exit 1: ")
        if args[:2] == ["exec-out", "screencap"]:
            return screencap, None
        if args[:2] == ["exec-out", "uiautomator"]:
            return dump, None
        if args[0] == "logcat":
            return logcat, None
        if args[:3] == ["shell", "dumpsys", "window"]:
            return f"  mCurrentFocus=Window{{1 u0 {PKG}/{PKG}.MainActivity}}\n", None
        return "  topResumedActivity=ActivityRecord{x u0 de.volksverpetzer.app/.MainActivity}\n", None

    run.calls = calls
    return run


def fake_driver(*, screenshot=b"\x89PNGappium", source=FEED, state=4):
    driver = Mock(session_id="sess-1")
    if isinstance(screenshot, BaseException):
        driver.get_screenshot_as_png.side_effect = screenshot
    else:
        driver.get_screenshot_as_png.return_value = screenshot
    if isinstance(source, BaseException):
        type(driver).page_source = property(lambda self: (_ for _ in ()).throw(source))
    else:
        driver.page_source = source
    driver.query_app_state.return_value = state
    return driver


def run_capture(tmp_path, driver, adb_fake, error=None):
    if error is None:
        try:
            raise TimeoutException("Exact active scenario identity qa-scenario:breaking_news was not exposed")
        except TimeoutException as raised:
            error = raised
    with patch.object(ld, "adb", adb_fake), patch("visualqa.allure_report.attach_launch_diagnostics") as attach:
        folder, summary = ld.capture(driver, scenario="breaking_news", package=PKG, launch_url=URL,
                                     error=error, folder=tmp_path / "diag")
    return folder, summary, attach


def test_failure_screen_hierarchy_state_logcat_and_context_written(tmp_path):
    folder, summary, attach = run_capture(tmp_path, fake_driver(), fake_adb())
    names = sorted(p.name for p in folder.iterdir())
    assert names == ["app-state.txt", "failure-screen.png", "hierarchy.xml", "launch-context.txt", "logcat.txt"]
    assert (folder / "failure-screen.png").read_bytes() == b"\x89PNGappium"
    context = (folder / "launch-context.txt").read_text()
    assert "expected identity: qa-scenario:breaking_news" in context
    assert "qa_scenario=['breaking_news'] metro_host=['127.0.0.1:8081']" in context
    assert "TimeoutException" in context and "Traceback" in context
    assert summary.startswith("marker-absent-unknown-screen")
    assert sorted(p.name for p in attach.call_args.args[0]) == names


def test_appium_screenshot_failure_falls_back_to_adb_screencap(tmp_path):
    folder, _, _ = run_capture(tmp_path, fake_driver(screenshot=WebDriverException("socket hang up")), fake_adb())
    assert (folder / "failure-screen.png").read_bytes() == b"\x89PNGadb"
    assert "appium screenshot: WebDriverException" in (folder / "diagnostic-errors.txt").read_text()


def test_page_source_failure_falls_back_to_uiautomator_dump(tmp_path):
    folder, summary, _ = run_capture(tmp_path, fake_driver(source=WebDriverException("instrumentation died")),
                                     fake_adb())
    assert (folder / "hierarchy.xml").read_text() == "<hierarchy dump/>"
    assert "appium page source" in (folder / "diagnostic-errors.txt").read_text()


def test_hierarchy_unavailable_when_both_sources_fail(tmp_path):
    folder, summary, _ = run_capture(tmp_path, fake_driver(source=WebDriverException("x")),
                                     fake_adb(fail=("uiautomator",)))
    assert summary.startswith("hierarchy-unavailable")
    assert not (folder / "hierarchy.xml").exists()


def test_hanging_driver_call_is_bounded(tmp_path, monkeypatch):
    monkeypatch.setattr(ld, "DRIVER_TIMEOUT_S", 0.3)
    driver = fake_driver()
    driver.get_screenshot_as_png.side_effect = lambda: time.sleep(5)
    started = time.monotonic()
    folder, _, _ = run_capture(tmp_path, driver, fake_adb())
    assert time.monotonic() - started < 3
    assert "timed out after 0.3s" in (folder / "diagnostic-errors.txt").read_text()
    assert (folder / "failure-screen.png").read_bytes() == b"\x89PNGadb"


def test_adb_subprocess_timeout_is_reported_not_raised(monkeypatch):
    import sys
    monkeypatch.setattr(ld, "_adb_base", lambda: [sys.executable])
    out, err = ld.adb(["-c", "import time; time.sleep(5)"], timeout_s=0.5)
    assert out is None and "timed out after 0.5s" in err


def test_logcat_failure_does_not_mask_anything(tmp_path):
    folder, summary, _ = run_capture(tmp_path, fake_driver(), fake_adb(fail=("logcat",)))
    assert not (folder / "logcat.txt").exists()
    assert "logcat:" in (folder / "diagnostic-errors.txt").read_text()
    assert summary.startswith("marker-absent-unknown-screen")


@pytest.mark.parametrize(("kwargs", "expected"), [
    (dict(process_running=False, hierarchy=FEED, logcat=""), "app-process-absent"),
    (dict(process_running=True, hierarchy='<n text="Development servers"/>', logcat=""), "dev-client-screen"),
    (dict(process_running=True, hierarchy='<n content-desc="qa-scenario:long_headline"/>', logcat=""), "wrong-marker"),
    (dict(process_running=True, hierarchy='<n content-desc="qa-scenario:breaking_news"/>', logcat=""), "marker-present"),
    (dict(process_running=True, hierarchy='<n text="QA scenario unavailable: x"/>', logcat=""), "qa-selection-rejected"),
    (dict(process_running=True, hierarchy=None, logcat=""), "hierarchy-unavailable"),
    (dict(process_running=True, hierarchy=FEED, logcat=""), "marker-absent-unknown-screen"),
])
def test_classification(kwargs, expected):
    state, _ = ld.classify(expected="breaking_news", foreground=PKG, package=PKG, **kwargs)
    assert state == expected


def test_native_crash_is_reported_with_absent_process():
    crash = "F/libc: Fatal signal 11 (SIGSEGV), code 2 (SEGV_ACCERR) tid 7812 (mqt_v_js), pid 7761 (ksverpetzer.app)"
    state, why = ld.classify(expected="no_image", process_running=False, foreground=None, package=PKG,
                             hierarchy=FEED, logcat=crash)
    assert state == "app-process-absent" and "crash signature" in why
    state, _ = ld.classify(expected="no_image", process_running=True, foreground=PKG, package=PKG,
                           hierarchy=FEED, logcat=crash)
    assert state == "crash-signature"


def test_missing_process_detected_from_pidof(tmp_path):
    _, summary, _ = run_capture(tmp_path, fake_driver(), fake_adb(pid=""))
    assert summary.startswith("app-process-absent")


def test_sanitized_url_drops_unrelated_query_data():
    assert ld.sanitize_launch_url("vvpapp:///home?qa_scenario=x&token=secret") == (
        "vvpapp:///home qa_scenario=['x'] metro_host=[]")
    assert ld.sanitize_launch_url(None) == "<none>"


def test_make_driver_timeout_before_yield_captures_and_keeps_original(monkeypatch, tmp_path):
    from visualqa import scenario_launch

    driver = fake_driver()
    monkeypatch.setattr(android.webdriver, "Remote", Mock(return_value=driver))
    monkeypatch.delenv("VVP_QA_LAUNCH_URL", raising=False)
    monkeypatch.setenv("VVP_ANDROID_PACKAGE", PKG)
    primary = TimeoutException("Exact active scenario identity qa-scenario:breaking_news was not exposed")
    monkeypatch.setattr(scenario_launch, "launch_scenario", Mock(side_effect=primary))
    with patch.object(ld, "adb", fake_adb()), patch("visualqa.allure_report.attach_launch_diagnostics"):
        with pytest.raises(TimeoutException) as caught:
            with android.android_session("breaking_news", tmp_path):
                pytest.fail("must not yield")
    assert caught.value is primary
    folder = tmp_path / "launch-diagnostics" / "breaking_news"
    assert (folder / "failure-screen.png").is_file() and (folder / "hierarchy.xml").is_file()
    assert any("Launch diagnostics (marker-absent-unknown-screen" in n for n in primary.__notes__)
    # Diagnostics run before cleanup, while the session still exists.
    assert driver.get_screenshot_as_png.call_count == 1
    driver.terminate_app.assert_called_with(PKG)
    driver.quit.assert_called_once()


def test_diagnostics_crash_is_a_note_not_the_failure(monkeypatch, tmp_path):
    from visualqa import scenario_launch

    monkeypatch.setattr(android.webdriver, "Remote", Mock(return_value=fake_driver()))
    monkeypatch.delenv("VVP_QA_LAUNCH_URL", raising=False)
    primary = TimeoutException("identity not exposed")
    monkeypatch.setattr(scenario_launch, "launch_scenario", Mock(side_effect=primary))
    with patch("visualqa.launch_diagnostics.capture", side_effect=RuntimeError("diag boom")):
        with pytest.raises(TimeoutException) as caught:
            android.make_driver("breaking_news", diagnostics_dir=tmp_path)
    assert caught.value is primary
    assert any("diag boom" in n for n in primary.__notes__)


def test_dev_launcher_activity_in_foreground_is_classified_as_dev_client():
    state, _ = ld.classify(expected="breaking_news", process_running=True, package=PKG, hierarchy=FEED, logcat="",
                           foreground=f"mCurrentFocus=Window{{x u0 {PKG}/expo.modules.devlauncher.launcher.errors.DevLauncherErrorActivity}}")
    assert state == "dev-client-screen"

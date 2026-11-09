"""Bounded, best-effort evidence when a scenario cold launch fails before the test body runs.

Called from ``make_driver`` while the Appium session and app are still alive. Every step has a
time limit, failures are recorded instead of raised, and the original exception always remains
the test failure. Files go to ``<artifacts>/launch-diagnostics/<scenario>/`` (inside the
uploaded ``visual-evidence`` scope) and are attached to the current Allure test when active.
"""

from __future__ import annotations

import os
import re
import subprocess
import threading
import time
import traceback
from collections.abc import Callable
from pathlib import Path
from urllib.parse import parse_qs, urlparse

DRIVER_TIMEOUT_S = 20
ADB_TIMEOUT_S = 15
LOGCAT_LINES = 3000
MAX_TEXT_BYTES = 400_000

# Markers in an Android UI hierarchy (UiAutomator2 page source or uiautomator dump).
_SCENARIO_MARKER = re.compile(r"qa-scenario:([A-Za-z0-9_]+)")
_QA_UNAVAILABLE = re.compile(r"qa-scenario-(invalid|unsupported)|QA scenario unavailable")
_DEV_CLIENT = re.compile(
    r"Development (Build|servers)|expo-development-client|Fetch development servers|"
    r"Enter URL manually|There was a problem loading the project|DevLauncher",
    re.IGNORECASE,
)
_ERROR_SCREEN = re.compile(r"Render Error|Uncaught Error|LogBox|Unable to load script|Reload JS|Dismiss",
                           re.IGNORECASE)
_LOGCAT_INTEREST = re.compile(
    r"ReactNativeJS|qa-scenario|AndroidRuntime|FATAL|Fatal signal|DEBUG\s*:|libc\s*:|"
    r"ActivityTaskManager: (START|Displayed)|ActivityManager: (Start proc|Process|Killing)|"
    r"ReactHost|DevLauncher|devlauncher|ANR in"
)


def sanitize_launch_url(url: str | None) -> str:
    """Scheme, host and path plus the qa_scenario values and the Metro host of ``url=`` only."""
    if not url:
        return "<none>"
    try:
        parsed = urlparse(url)
        query = parse_qs(parsed.query, keep_blank_values=True)
        metro = [urlparse(v).netloc or "<unparseable>" for v in query.get("url", [])]
        return (f"{parsed.scheme}://{parsed.netloc}{parsed.path} "
                f"qa_scenario={query.get('qa_scenario', [])} metro_host={metro}")
    except ValueError:
        return "<unparseable>"


def bounded(fn: Callable[[], object], timeout_s: float) -> tuple[object | None, str | None]:
    """Run ``fn`` in a daemon thread; return (value, None) or (None, error/timeout description)."""
    box: dict[str, object] = {}

    def run() -> None:
        try:
            box["value"] = fn()
        except BaseException as error:  # recorded, never raised
            box["error"] = f"{type(error).__name__}: {error}"

    worker = threading.Thread(target=run, daemon=True)
    worker.start()
    worker.join(timeout_s)
    if worker.is_alive():
        return None, f"timed out after {timeout_s}s"
    if "error" in box:
        return None, str(box["error"])
    return box.get("value"), None


def _adb_base() -> list[str]:
    return [os.environ.get("ADB", "adb"), "-s", os.environ.get("VVP_ANDROID_UDID", "emulator-5554")]


def adb(args: list[str], timeout_s: float = ADB_TIMEOUT_S, binary: bool = False) -> tuple[bytes | str | None, str | None]:
    try:
        done = subprocess.run(_adb_base() + args, capture_output=True, timeout=timeout_s,
                              stdin=subprocess.DEVNULL, check=False)
    except subprocess.TimeoutExpired:
        return None, f"adb {' '.join(args)}: timed out after {timeout_s}s"
    except OSError as error:
        return None, f"adb {' '.join(args)}: {error}"
    if done.returncode != 0:
        return None, f"adb {' '.join(args)}: exit {done.returncode}: {done.stderr.decode(errors='replace')[:300]}"
    return (done.stdout if binary else done.stdout.decode(errors="replace")), None


def classify(*, expected: str, process_running: bool | None, foreground: str | None,
             package: str, hierarchy: str | None, logcat: str | None) -> tuple[str, str]:
    """(state, explanation) from the evidence; 'unknown' when it does not decide."""
    crash = bool(logcat and re.search(
        rf"Fatal signal \d+.*\(.*{re.escape(package[-15:])}\)|>>> {re.escape(package)} <<<|"
        rf"Process {re.escape(package)} \(pid \d+\) has died", logcat))
    if process_running is False:
        return ("app-process-absent",
                "app process not running" + ("; crash signature in logcat (see logcat.txt)" if crash else ""))
    if hierarchy is None:
        return "hierarchy-unavailable", "UI hierarchy could not be captured (Appium/instrumentation problem?)"
    found = sorted(set(_SCENARIO_MARKER.findall(hierarchy)))
    if expected in found:
        return "marker-present", f"qa-scenario:{expected} is present in the captured hierarchy"
    if found:
        return "wrong-marker", f"found qa-scenario marker(s) {found}, expected {expected}"
    if _QA_UNAVAILABLE.search(hierarchy):
        return "qa-selection-rejected", "app shows 'QA scenario unavailable' (invalid/unsupported launch selection)"
    if _DEV_CLIENT.search(hierarchy) or (foreground and "devlauncher" in foreground.lower()):
        return "dev-client-screen", "Expo development-client screen visible; app UI not reached"
    if _ERROR_SCREEN.search(hierarchy):
        return "error-overlay", "React Native error/LogBox overlay visible"
    if foreground and package not in foreground:
        return "other-app-foreground", f"foreground is {foreground}, not {package}"
    if crash:
        return "crash-signature", "crash signature in logcat although the app process is running"
    return ("marker-absent-unknown-screen",
            "app UI present but no qa-scenario marker (normal feed, unexpected route, or marker not exposed); "
            "see failure-screen.png and hierarchy.xml")


def _write(folder: Path, name: str, data: bytes | str) -> Path:
    path = folder / name
    if isinstance(data, str):
        data = data.encode("utf-8", errors="replace")
    path.write_bytes(data[-MAX_TEXT_BYTES:] if not name.endswith(".png") else data)
    return path


def capture(driver, *, scenario: str, package: str, launch_url: str | None,
            error: BaseException, folder: Path) -> tuple[Path, str]:
    """Collect evidence; returns (folder, one-line summary). Never raises."""
    problems: list[str] = []
    written: list[Path] = []
    try:
        folder.mkdir(parents=True, exist_ok=True)
        for old in folder.iterdir():  # evidence from an earlier run must not be mistaken for this one
            if old.is_file():
                old.unlink()

        png, err = bounded(driver.get_screenshot_as_png, DRIVER_TIMEOUT_S)
        if err:
            problems.append(f"appium screenshot: {err}")
            png, err = adb(["exec-out", "screencap", "-p"], binary=True)
            if err:
                problems.append(f"adb screencap fallback: {err}")
        if png:
            written.append(_write(folder, "failure-screen.png", png))

        hierarchy, err = bounded(lambda: driver.page_source, DRIVER_TIMEOUT_S)
        if err:
            problems.append(f"appium page source: {err}")
            dumped, err = adb(["exec-out", "uiautomator", "dump", "/dev/tty"], timeout_s=25)
            if err:
                problems.append(f"uiautomator dump fallback: {err}")
            hierarchy = dumped or None
        if hierarchy:
            written.append(_write(folder, "hierarchy.xml", str(hierarchy)))

        app_state, err = bounded(lambda: driver.query_app_state(package), DRIVER_TIMEOUT_S)
        if err:
            problems.append(f"query_app_state: {err}")
        pid, err = adb(["shell", "pidof", package])
        process_running = None if err and "exit 1" not in err else bool(pid and str(pid).strip())
        if err and "exit 1" not in err:
            problems.append(f"pidof: {err}")
        focus, err = adb(["shell", "dumpsys", "window", "displays"], timeout_s=20)
        if err:
            problems.append(f"dumpsys window: {err}")
        focus_lines = [line.strip() for line in str(focus or "").splitlines()
                       if "mCurrentFocus" in line or "mFocusedApp" in line][:4]
        foreground = focus_lines[0] if focus_lines else None
        activity, err = adb(["shell", "dumpsys", "activity", "activities"], timeout_s=20)
        if err:
            problems.append(f"dumpsys activity: {err}")
        resumed = [line.strip() for line in str(activity or "").splitlines()
                   if "ResumedActivity" in line][:4]
        written.append(_write(folder, "app-state.txt", "\n".join([
            f"package: {package}",
            f"appium query_app_state: {app_state}",
            f"pidof: {str(pid or '').strip() or '<none>'}",
            *focus_lines, *resumed,
        ]) + "\n"))

        logcat, err = adb(["logcat", "-d", "-v", "time", "-t", str(LOGCAT_LINES)], timeout_s=20)
        if err:
            problems.append(f"logcat: {err}")
        if logcat:
            relevant = "\n".join(line for line in str(logcat).splitlines() if _LOGCAT_INTEREST.search(line))
            written.append(_write(folder, "logcat.txt", relevant + "\n"))

        state, why = classify(expected=scenario, process_running=process_running, foreground=foreground,
                              package=package, hierarchy=str(hierarchy) if hierarchy else None,
                              logcat=str(logcat) if logcat else None)
        written.append(_write(folder, "launch-context.txt", "\n".join([
            f"expected scenario: {scenario}",
            f"expected identity: qa-scenario:{scenario}",
            f"observed identities: {sorted(set(_SCENARIO_MARKER.findall(str(hierarchy or ''))))}",
            f"classification: {state}",
            f"explanation: {why}",
            f"launch url (sanitized): {sanitize_launch_url(launch_url)}",
            f"session id: {getattr(driver, 'session_id', '?')}",
            f"captured at (UTC): {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
            "original exception:",
            "".join(traceback.format_exception(error)),
        ])))
    except Exception as unexpected:  # the diagnostics themselves must never replace the failure
        problems.append(f"diagnostic collection aborted: {type(unexpected).__name__}: {unexpected}")
        state, why = "unknown", "diagnostic collection aborted"
    if problems:
        try:
            written.append(_write(folder, "diagnostic-errors.txt", "\n".join(problems) + "\n"))
        except OSError:
            pass
    _attach(written)
    return folder, f"{state}: {why}"


def _attach(paths: list[Path]) -> None:
    try:
        from visualqa import allure_report
        allure_report.attach_launch_diagnostics(paths)
    except Exception:  # Allure is optional; never mask the original failure
        pass

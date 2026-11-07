"""The Android-specific Appium driver and selectors are isolated here."""

from __future__ import annotations

import os
from pathlib import Path

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import WebDriverException


def make_driver(scenario: str | None = None):
    """Create a session; with ``scenario`` the app is cold-launched into that QA scenario."""
    package_name = os.environ.get("VVP_ANDROID_PACKAGE", "de.volksverpetzer.app")
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = os.environ.get("VVP_ANDROID_DEVICE", "Pixel_10")
    options.udid = os.environ.get("VVP_ANDROID_UDID", "emulator-5554")
    options.app_package = package_name
    options.app_activity = os.environ.get("VVP_ANDROID_ACTIVITY", ".MainActivity")
    # Metro + the installed Expo development build must already be available.
    # Preserve activation compatibility unless explicit cold-launch mode is selected.
    options.no_reset = True
    options.set_capability("appium:autoLaunch", False)
    options.set_capability("appium:newCommandTimeout", 90)
    launch_url = None
    if scenario is not None:
        from visualqa.scenario_launch import resolve_launch_url
        # Resolve (and reject conflicting overrides) before opening a session.
        launch_url = resolve_launch_url(scenario)
    else:
        launch_url = os.environ.get("VVP_QA_LAUNCH_URL")
    driver = webdriver.Remote(os.environ.get("VVP_APPIUM_URL", "http://127.0.0.1:4723"), options=options)
    try:
        if launch_url:
            from visualqa.scenario_launch import launch_scenario
            launch_scenario(driver, package_name, launch_url)
        else:
            # Compatibility path: existing Metro environment selection/activation.
            driver.activate_app(package_name)
            from visualqa.scenario_launch import wait_for_scenario_identity
            wait_for_scenario_identity(driver)
    except Exception:
        try:
            if launch_url:
                driver.terminate_app(package_name)
        finally:
            driver.quit()
        raise
    return driver


def save_diagnostics(driver, folder: Path):
    folder.mkdir(parents=True, exist_ok=True)
    try:
        (folder / "failure-full-screen.png").write_bytes(driver.get_screenshot_as_png())
    except WebDriverException as err:
        (folder / "screenshot-error.txt").write_text(str(err), encoding="utf-8")
    try:
        (folder / "failure-page-source.xml").write_text(driver.page_source, encoding="utf-8")
    except WebDriverException as err:
        (folder / "page-source-error.txt").write_text(str(err), encoding="utf-8")

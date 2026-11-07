"""Opt-in Android cold launch; scenario identity must precede card readiness."""

from urllib.parse import parse_qs, urlparse

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait


def wait_for_scenario_identity(driver, scenario="long_headline"):
    # Scenario identity precedes component-specific readiness.
    WebDriverWait(driver, 45).until(
        lambda current: current.find_elements(AppiumBy.ACCESSIBILITY_ID, f"qa-scenario:{scenario}"),
        message=f"Exact active scenario identity qa-scenario:{scenario} was not exposed",
    )


def launch_scenario(driver, package_name: str, url: str):
    selection = parse_qs(urlparse(url).query, keep_blank_values=True).get("qa_scenario")
    if not selection or len(selection) != 1 or selection[0] not in {"long_headline", "breaking_news", "dark_article", "no_image", "empty_feed"}:
        raise ValueError("Visual capture supports only explicit long_headline, breaking_news, dark_article, no_image or empty_feed selections")
    driver.terminate_app(package_name)
    driver.execute_script("mobile: deepLink", {
        "url": url, "package": package_name, "waitForLaunch": True,
    })
    # This marker is outside the card and does not assert that its media is ready.
    wait_for_scenario_identity(driver, selection[0])

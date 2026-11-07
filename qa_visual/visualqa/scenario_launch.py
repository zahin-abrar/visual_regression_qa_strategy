"""Opt-in Android cold launch; scenario identity must precede card readiness."""

import os
from urllib.parse import parse_qs, quote, urlparse

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

SUPPORTED_SCENARIOS = frozenset({"long_headline", "breaking_news", "dark_article", "no_image", "empty_feed"})
DEV_CLIENT_LINK = "exp+vvpapp://expo-development-client/"


def build_launch_url(scenario: str, host: str = "127.0.0.1", port: str = "8081") -> str:
    """Expo development-client deep link that selects ``scenario`` before the feed mounts."""
    if scenario not in SUPPORTED_SCENARIOS:
        raise ValueError(f"Unsupported QA scenario {scenario!r}")
    metro = quote(f"http://{host}:{port}", safe="")
    return f"{DEV_CLIENT_LINK}?url={metro}&qa_scenario={scenario}"


def resolve_launch_url(scenario: str, env=None) -> str:
    """Launch URL for the scenario a test declares.

    Optional overrides: VVP_METRO_HOST / VVP_METRO_PORT (defaults 127.0.0.1:8081).
    A full VVP_QA_LAUNCH_URL is still accepted for compatibility, but only if it
    selects exactly the declared scenario; a stale or conflicting value fails.
    """
    env = os.environ if env is None else env
    override = env.get("VVP_QA_LAUNCH_URL")
    if override:
        selected = parse_qs(urlparse(override).query, keep_blank_values=True).get("qa_scenario")
        if selected != [scenario]:
            raise ValueError(
                f"VVP_QA_LAUNCH_URL selects {selected!r} but the test declares qa_scenario {scenario!r}; "
                "unset VVP_QA_LAUNCH_URL (no longer required) or make it match"
            )
        return override
    return build_launch_url(scenario, env.get("VVP_METRO_HOST", "127.0.0.1"), env.get("VVP_METRO_PORT", "8081"))


def wait_for_scenario_identity(driver, scenario="long_headline"):
    # Scenario identity precedes component-specific readiness.
    WebDriverWait(driver, 45).until(
        lambda current: current.find_elements(AppiumBy.ACCESSIBILITY_ID, f"qa-scenario:{scenario}"),
        message=f"Exact active scenario identity qa-scenario:{scenario} was not exposed",
    )


def launch_scenario(driver, package_name: str, url: str):
    selection = parse_qs(urlparse(url).query, keep_blank_values=True).get("qa_scenario")
    if not selection or len(selection) != 1 or selection[0] not in SUPPORTED_SCENARIOS:
        raise ValueError("Visual capture supports only explicit long_headline, breaking_news, dark_article, no_image or empty_feed selections")
    driver.terminate_app(package_name)
    driver.execute_script("mobile: deepLink", {
        "url": url, "package": package_name, "waitForLaunch": True,
    })
    # This marker is outside the card and does not assert that its media is ready.
    wait_for_scenario_identity(driver, selection[0])

"""Opt-in Android cold launch; scenario identity must precede card readiness."""

import os
import time
from urllib.parse import parse_qs, quote, urlparse

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException

from visualqa import expo_overlay

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


SCENARIO_WAIT_S = 45
MARKER_POLL_S = 0.5
OVERLAY_CHECK_EVERY_S = 1.5
MAX_DISMISSAL_EXTENSION_S = 10


def wait_for_scenario_identity(driver, scenario="long_headline", *, clock=time.monotonic, sleep=time.sleep):
    """Wait for the exact ``qa-scenario:<id>`` accessibility identity (45 s, unchanged).

    While waiting, the Expo developer-menu onboarding sheet is recognised (hierarchy evidence only) and
    dismissed at most once per overlay variant (onboarding sheet, then the dev-menu panel it opens); the time spent dismissing extends the wait by at most
    MAX_DISMISSAL_EXTENSION_S. Dismissal never counts as activation: the exact marker is still required.
    """
    message = f"Exact active scenario identity qa-scenario:{scenario} was not exposed"
    deadline = clock() + SCENARIO_WAIT_S
    last_overlay_check = None
    report = None
    handled = set()
    extended = 0.0
    while True:
        if driver.find_elements(AppiumBy.ACCESSIBILITY_ID, f"qa-scenario:{scenario}"):
            return
        now = clock()
        if now >= deadline:
            error = TimeoutException(message)
            error.add_note(f"Expo onboarding overlay: {report or 'not observed (no dismissal attempted)'}")
            raise error
        if last_overlay_check is None or now - last_overlay_check >= OVERLAY_CHECK_EVERY_S:
            last_overlay_check = now
            try:
                evidence = expo_overlay.inspect_hierarchy(expo_overlay._source(driver))
                if evidence is not None and evidence.present:
                    if evidence.variant in handled:
                        raise expo_overlay.ExpoOverlayError(
                            f"Expo overlay reappeared after it was dismissed ({evidence.describe()})")
                    step = expo_overlay.dismiss_if_present(driver, evidence, clock=clock, sleep=sleep)
                    handled.add(evidence.variant)
                    report = f"{report}; {step}" if report else step
                    deadline += min(clock() - now, max(0, MAX_DISMISSAL_EXTENSION_S - extended))
                    extended += min(clock() - now, max(0, MAX_DISMISSAL_EXTENSION_S - extended))
                    continue
            except expo_overlay.ExpoOverlayError as error:
                error.add_note(f"scenario wait for qa-scenario:{scenario}; overlay report: {report or 'none'}")
                raise
        sleep(MARKER_POLL_S)


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

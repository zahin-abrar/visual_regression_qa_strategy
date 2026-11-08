from unittest.mock import Mock

import pytest

from visualqa.scenario_launch import SUPPORTED_SCENARIOS, build_launch_url, launch_scenario, resolve_launch_url


@pytest.mark.unit
def test_default_launch_url_matches_documented_dev_client_link():
    assert resolve_launch_url("breaking_news", env={}) == (
        "exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=breaking_news"
    )


@pytest.mark.unit
@pytest.mark.parametrize("scenario", sorted(SUPPORTED_SCENARIOS))
def test_built_url_is_accepted_by_launcher_for_its_own_scenario(scenario):
    driver = Mock()
    driver.find_elements.return_value = [object()]
    launch_scenario(driver, "package", resolve_launch_url(scenario, env={}))
    driver.find_elements.assert_called_once_with("accessibility id", f"qa-scenario:{scenario}")


@pytest.mark.unit
def test_metro_host_and_port_overrides():
    url = resolve_launch_url("no_image", env={"VVP_METRO_HOST": "10.0.2.2", "VVP_METRO_PORT": "19000"})
    assert url == "exp+vvpapp://expo-development-client/?url=http%3A%2F%2F10.0.2.2%3A19000&qa_scenario=no_image"


@pytest.mark.unit
def test_matching_full_url_override_is_kept():
    override = build_launch_url("dark_article", port="8082")
    assert resolve_launch_url("dark_article", env={"VVP_QA_LAUNCH_URL": override}) == override


@pytest.mark.unit
@pytest.mark.parametrize("stale", ["long_headline", "breaking_news&qa_scenario=empty_feed", ""])
def test_conflicting_full_url_override_fails_clearly(stale):
    env = {"VVP_QA_LAUNCH_URL": f"exp+vvpapp://expo-development-client/?qa_scenario={stale}"}
    with pytest.raises(ValueError, match="test declares qa_scenario 'empty_feed'"):
        resolve_launch_url("empty_feed", env=env)


@pytest.mark.unit
def test_unknown_scenario_rejected():
    with pytest.raises(ValueError, match="Unsupported"):
        build_launch_url("offline")


@pytest.mark.unit
def test_launch_checks_identity_after_termination_and_deep_link():
    driver = Mock()
    driver.find_elements.return_value = [object()]
    launch_scenario(driver, "package", "vvpapp:///home?qa_scenario=long_headline")
    assert [call[0] for call in driver.mock_calls] == [
        "terminate_app", "execute_script", "find_elements",
    ]
    driver.find_elements.assert_called_once_with("accessibility id", "qa-scenario:long_headline")


@pytest.mark.unit
@pytest.mark.parametrize("query", ["", "qa_scenario=unknown", "qa_scenario=none", "qa_scenario=long_headline&qa_scenario=empty_feed"])
def test_unsupported_capture_rejected_before_launch(query):
    driver = Mock()
    with pytest.raises(ValueError, match="only explicit"):
        launch_scenario(driver, "package", f"vvpapp:///home?{query}")
    assert not driver.mock_calls

@pytest.mark.unit
def test_breaking_launch_verifies_its_own_identity():
    driver = Mock()
    driver.find_elements.return_value = [object()]
    launch_scenario(driver, "package", "vvpapp:///home?qa_scenario=breaking_news")
    driver.find_elements.assert_called_once_with("accessibility id", "qa-scenario:breaking_news")


@pytest.mark.unit
def test_dark_launch_verifies_its_own_identity():
    driver = Mock()
    driver.find_elements.return_value = [object()]
    launch_scenario(driver, "package", "vvpapp:///home?qa_scenario=dark_article")
    driver.find_elements.assert_called_once_with("accessibility id", "qa-scenario:dark_article")


@pytest.mark.unit
def test_no_image_launch_verifies_its_own_identity():
    driver = Mock()
    driver.find_elements.return_value = [object()]
    launch_scenario(driver, "package", "vvpapp:///home?qa_scenario=no_image")
    driver.find_elements.assert_called_once_with("accessibility id", "qa-scenario:no_image")


@pytest.mark.unit
def test_empty_feed_launch_verifies_its_own_identity():
    driver = Mock()
    driver.find_elements.return_value = [object()]
    launch_scenario(driver, "package", "vvpapp:///home?qa_scenario=empty_feed")
    assert [call[0] for call in driver.mock_calls] == [
        "terminate_app", "execute_script", "find_elements",
    ]
    driver.find_elements.assert_called_once_with("accessibility id", "qa-scenario:empty_feed")

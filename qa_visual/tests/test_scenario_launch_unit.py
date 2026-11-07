from unittest.mock import Mock

import pytest

from visualqa.scenario_launch import launch_scenario


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
@pytest.mark.parametrize("query", ["", "qa_scenario=unknown", "qa_scenario=empty_feed", "qa_scenario=long_headline&qa_scenario=long_headline"])
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

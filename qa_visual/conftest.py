"""Scenario declaration shared by visual tests; root pytest.ini sets imports."""

import pytest


@pytest.fixture
def qa_scenario(request: pytest.FixtureRequest) -> str:
    """The QA scenario a test declares with ``@pytest.mark.qa_scenario("<id>")``."""
    from visualqa.scenario_launch import SUPPORTED_SCENARIOS

    marker = request.node.get_closest_marker("qa_scenario")
    if marker is None or len(marker.args) != 1:
        pytest.fail('Visual tests must declare exactly one @pytest.mark.qa_scenario("<id>")')
    scenario = marker.args[0]
    if scenario not in SUPPORTED_SCENARIOS:
        pytest.fail(f"Unsupported qa_scenario {scenario!r}; expected one of {sorted(SUPPORTED_SCENARIOS)}")
    return scenario

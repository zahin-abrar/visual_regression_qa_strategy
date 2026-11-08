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


@pytest.fixture(autouse=True)
def _allure_scenario_evidence(request: pytest.FixtureRequest):
    """Allure labels and current-run failure diagnostics; no effect without --alluredir."""
    marker = request.node.get_closest_marker("qa_scenario")
    if marker is None or len(marker.args) != 1:
        yield
        return
    import os
    import time

    from visualqa import allure_report
    from visualqa.visual_check import ROOT

    profile = os.environ.get("VVP_GOLDEN_PROFILE", "pixel10-api37")
    started_ns = time.time_ns()
    allure_report.label_visual_test(request.node, marker.args[0], profile)
    try:
        yield
        allure_report.attach_failure_diagnostics(ROOT / "artifacts" / "android" / profile, started_ns)
    finally:
        allure_report.set_active(False)

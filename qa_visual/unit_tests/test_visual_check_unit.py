"""Artifact safety, tolerance policy and session cleanup without a device."""

import json
from unittest.mock import Mock

import pytest
from PIL import Image

from visualqa import android, visual_check
from visualqa.visual_check import VisualArtifacts

pytestmark = pytest.mark.unit


def test_profile_paths_and_invalid_profile(monkeypatch, tmp_path):
    monkeypatch.setattr(visual_check, "ROOT", tmp_path)
    monkeypatch.setenv("VVP_GOLDEN_PROFILE", "test-profile")
    artifacts = VisualArtifacts.for_scenario("dark_article")
    assert artifacts.actual == tmp_path / "artifacts/android/test-profile/dark_article.actual.png"
    assert artifacts.baseline == tmp_path / "baselines/android/test-profile/dark_article.png"
    monkeypatch.setenv("VVP_GOLDEN_PROFILE", "../escape")
    with pytest.raises(pytest.fail.Exception, match="VVP_GOLDEN_PROFILE"):
        VisualArtifacts.for_scenario("dark_article")


def test_missing_reference_keeps_capture_without_creating_golden(tmp_path):
    artifacts = VisualArtifacts(tmp_path, "sample", tmp_path / "missing.png")
    Image.new("RGB", (2, 2)).save(artifacts.actual)
    with pytest.raises(pytest.fail.Exception, match="Golden missing"):
        artifacts.compare()
    assert artifacts.actual.is_file()
    assert not artifacts.baseline.exists()
    assert not artifacts.path("comparison.json").exists()


@pytest.mark.parametrize("use_overrides, passed", [(False, False), (True, True)])
def test_environment_tolerance_is_explicit_and_reference_unchanged(
    monkeypatch, tmp_path, use_overrides, passed
):
    artifacts = VisualArtifacts(tmp_path, "sample", tmp_path / "baseline.png")
    Image.new("RGB", (2, 2), (0, 0, 0)).save(artifacts.baseline)
    original = artifacts.baseline.read_bytes()
    Image.new("RGB", (2, 2), (13, 0, 0)).save(artifacts.actual)
    monkeypatch.setenv("VVP_CHANNEL_TOLERANCE", "20")
    monkeypatch.setenv("VVP_MAX_CHANGED_RATIO", "0.002")
    result = artifacts.compare(use_environment_tolerances=use_overrides)
    assert result.passed is passed
    assert result.channel_tolerance == (20 if use_overrides else 12)
    assert result.max_changed_ratio == 0.002
    assert artifacts.baseline.read_bytes() == original
    assert artifacts.path("diff.png").is_file()
    assert json.loads(artifacts.path("comparison.json").read_text())["passed"] is passed


def test_context_hierarchy_and_metadata_keep_existing_names(tmp_path):
    artifacts = VisualArtifacts(tmp_path, "sample", tmp_path / "baseline.png")
    driver = Mock(page_source="<hierarchy/>")
    driver.get_screenshot_as_png.return_value = b"context"
    artifacts.save_context(driver)
    artifacts.save_hierarchy(driver)
    artifacts.save_metadata({"scenario": "sample", "session": "test-session"})
    assert artifacts.path("context.png").read_bytes() == b"context"
    assert artifacts.path("hierarchy.xml").read_text() == "<hierarchy/>"
    assert json.loads(artifacts.path("capture.json").read_text())["session"] == "test-session"


def _raise_recorded(error, tracebacks):
    try:
        raise error
    except BaseException:
        tracebacks.append(error.__traceback__)
        raise


def _assert_original_traceback(error, original):
    current = error.__traceback__
    while current is not None and current is not original:
        current = current.tb_next
    assert current is original, "Original traceback frame was lost"


@pytest.mark.parametrize("secondary", [(), ("diagnostics",), ("termination",), ("quit",),
                                       ("termination", "quit"), ("diagnostics", "termination", "quit")])
def test_session_preserves_body_failure(monkeypatch, tmp_path, secondary):
    driver = Mock()
    diagnostics = Mock()
    calls = Mock()
    calls.attach_mock(diagnostics, "diagnostics")
    calls.attach_mock(driver.terminate_app, "terminate")
    calls.attach_mock(driver.quit, "quit")
    monkeypatch.setattr(android, "make_driver", Mock(return_value=driver))
    monkeypatch.setattr(android, "save_diagnostics", diagnostics)
    monkeypatch.setenv("VVP_ANDROID_PACKAGE", "test.package")
    for name, operation in [("diagnostics", diagnostics), ("termination", driver.terminate_app),
                            ("quit", driver.quit)]:
        if name in secondary:
            operation.side_effect = RuntimeError(f"{name} failed")
    primary = AssertionError("original fixture failure")
    traces = []
    with pytest.raises(AssertionError) as caught:
        with android.android_session("dark_article", tmp_path):
            _raise_recorded(primary, traces)
    assert caught.value is primary
    _assert_original_traceback(primary, traces[0])
    assert [call[0] for call in calls.mock_calls] == ["diagnostics", "terminate", "quit"]
    diagnostics.assert_called_once_with(driver, tmp_path)
    driver.terminate_app.assert_called_once_with("test.package")
    notes = getattr(primary, "__notes__", [])
    assert len(notes) == len(secondary)
    for name, note in zip(secondary, notes):
        assert f"RuntimeError: {name} failed" in note
        assert "Traceback" in note


@pytest.mark.parametrize("secondary", [(), ("termination",), ("quit",), ("termination", "quit")])
def test_session_reports_cleanup_failure_after_success(monkeypatch, tmp_path, secondary):
    driver = Mock()
    diagnostics = Mock()
    monkeypatch.setattr(android, "make_driver", Mock(return_value=driver))
    monkeypatch.setattr(android, "save_diagnostics", diagnostics)
    errors = {name: RuntimeError(f"{name} failed") for name in secondary}
    traces = []
    if "termination" in secondary:
        driver.terminate_app.side_effect = lambda _: _raise_recorded(errors["termination"], traces)
    if "quit" in secondary:
        driver.quit.side_effect = lambda: _raise_recorded(errors["quit"], traces)

    def exercise():
        with android.android_session("dark_article", tmp_path) as current:
            assert current is driver

    if secondary:
        with pytest.raises(RuntimeError) as caught:
            exercise()
        assert caught.value is errors[secondary[0]]
        _assert_original_traceback(caught.value, traces[0])
        notes = getattr(caught.value, "__notes__", [])
        assert len(notes) == len(secondary) - 1
        if len(secondary) == 2:
            assert "RuntimeError: quit failed" in notes[0]
    else:
        exercise()
    assert [call[0] for call in driver.mock_calls] == ["terminate_app", "quit"]
    diagnostics.assert_not_called()


def test_session_preserves_body_on_diagnostic_filesystem_failure(monkeypatch, tmp_path):
    driver = Mock()
    monkeypatch.setattr(android, "make_driver", Mock(return_value=driver))
    # A file cannot serve as the diagnostic output directory; exercise real mkdir failure.
    output = tmp_path / "not-a-directory"
    output.write_text("keep", encoding="utf-8")
    primary = AssertionError("body failed")
    with pytest.raises(AssertionError) as caught:
        with android.android_session("dark_article", output):
            raise primary
    assert caught.value is primary
    assert "diagnostic collection" in primary.__notes__[0]
    assert "FileExistsError" in primary.__notes__[0]
    assert output.read_text() == "keep"
    driver.terminate_app.assert_called_once()
    driver.quit.assert_called_once()


@pytest.mark.parametrize("primary", [pytest.fail.Exception("pytest failure"), KeyboardInterrupt()])
def test_session_preserves_base_exception(monkeypatch, tmp_path, primary):
    driver = Mock()
    monkeypatch.setattr(android, "make_driver", Mock(return_value=driver))
    monkeypatch.setattr(android, "save_diagnostics", Mock(side_effect=RuntimeError("diagnostics")))
    with pytest.raises(type(primary)) as caught:
        with android.android_session("dark_article", tmp_path):
            raise primary
    assert caught.value is primary
    assert "diagnostics" in primary.__notes__[0]
    driver.terminate_app.assert_called_once()
    driver.quit.assert_called_once()


def test_session_driver_creation_failure_is_primary(monkeypatch, tmp_path):
    from visualqa import scenario_launch

    primary = RuntimeError("Remote construction failed")
    traces = []
    remote = Mock(side_effect=lambda *args, **kwargs: _raise_recorded(primary, traces))
    monkeypatch.setattr(android.webdriver, "Remote", remote)
    monkeypatch.setattr(scenario_launch, "resolve_launch_url", Mock(return_value="mock://scenario"))
    cleanup = Mock()
    diagnostics = Mock()
    monkeypatch.setattr(android, "_cleanup_driver", cleanup)
    monkeypatch.setattr(android, "save_diagnostics", diagnostics)
    with pytest.raises(RuntimeError) as caught:
        with android.android_session("dark_article", tmp_path):
            pytest.fail("Must not yield a driver")
    assert caught.value is primary
    _assert_original_traceback(primary, traces[0])
    remote.assert_called_once()
    cleanup.assert_not_called()
    diagnostics.assert_not_called()


@pytest.mark.parametrize("legacy", [False, True])
@pytest.mark.parametrize("secondary", [(), ("termination",), ("quit",), ("termination", "quit")])
def test_make_driver_preserves_launch_failure(monkeypatch, legacy, secondary):
    from visualqa import scenario_launch

    driver = Mock()
    monkeypatch.setattr(android.webdriver, "Remote", Mock(return_value=driver))
    monkeypatch.setattr(scenario_launch, "resolve_launch_url", Mock(return_value="mock://scenario"))
    monkeypatch.delenv("VVP_QA_LAUNCH_URL", raising=False)
    monkeypatch.setenv("VVP_ANDROID_PACKAGE", "test.package")
    primary = RuntimeError("original launch failure")
    traces = []
    launch = Mock(side_effect=lambda *args: _raise_recorded(primary, traces))
    monkeypatch.setattr(scenario_launch, "launch_scenario", launch)
    if legacy:
        driver.activate_app = launch
    calls = Mock()
    calls.attach_mock(launch, "launch")
    calls.attach_mock(driver.terminate_app, "terminate")
    calls.attach_mock(driver.quit, "quit")
    for name, operation in [("termination", driver.terminate_app), ("quit", driver.quit)]:
        if name in secondary:
            operation.side_effect = RuntimeError(f"{name} failed")
    with pytest.raises(RuntimeError) as caught:
        android.make_driver(None if legacy else "dark_article")
    assert caught.value is primary
    _assert_original_traceback(primary, traces[0])
    assert [call[0] for call in calls.mock_calls] == ["launch", "terminate", "quit"]
    driver.terminate_app.assert_called_once_with("test.package")
    notes = getattr(primary, "__notes__", [])
    assert len(notes) == len(secondary)
    for name, note in zip(secondary, notes):
        assert f"RuntimeError: {name} failed" in note
        assert "Traceback" in note

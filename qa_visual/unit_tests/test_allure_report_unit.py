"""Allure evidence helpers: only current-run files are attached."""

from __future__ import annotations

import os
import time
from unittest.mock import patch

import pytest
from allure_commons.types import AttachmentType

from visualqa import allure_report
from visualqa.image_diff import Comparison
from visualqa.visual_check import VisualArtifacts

pytestmark = pytest.mark.unit


@pytest.fixture(autouse=True)
def _active_reporting():
    allure_report.set_active(True)
    yield
    allure_report.set_active(False)

RESULT = Comparison(True, (1, 1), (1, 1), 0, 1, 0.0, 0.002, 12, True)


def _attached(mock_file) -> list[str]:
    return [call.kwargs["name"] for call in mock_file.call_args_list]


def test_stale_file_is_not_attached(tmp_path) -> None:
    stale = tmp_path / "failure-full-screen.png"
    stale.write_bytes(b"x")
    old = time.time() - 3600
    os.utime(stale, (old, old))
    with patch("allure.attach.file") as attach:
        assert not allure_report.attach_if_fresh(stale, "n", AttachmentType.PNG, time.time_ns())
    attach.assert_not_called()


def test_fresh_file_is_attached_with_type(tmp_path) -> None:
    fresh = tmp_path / "a.json"
    fresh.write_text("{}")
    with patch("allure.attach.file") as attach:
        assert allure_report.attach_if_fresh(fresh, "metrics", AttachmentType.JSON, time.time_ns() - 10**9)
    assert attach.call_args.kwargs["attachment_type"] is AttachmentType.JSON


def test_comparison_attaches_only_current_artifacts_and_labels_reference(tmp_path) -> None:
    baseline = tmp_path / "ref.png"
    baseline.write_bytes(b"ref")
    artifacts = VisualArtifacts(tmp_path, "s", baseline)
    old = time.time() - 3600
    for suffix in ("actual.png", "context.png"):
        artifacts.path(suffix).write_bytes(b"old")
        os.utime(artifacts.path(suffix), (old, old))
    object.__setattr__(artifacts, "started_ns", time.time_ns() - 10**9)
    artifacts.path("diff.png").write_bytes(b"new")
    with patch("allure.attach.file") as attach, patch("allure.dynamic.parameter"):
        allure_report.attach_comparison(artifacts, RESULT, intentional_reference=True)
    names = _attached(attach)
    assert names == [
        "Intentionally INCORRECT reference (demo, not an approved golden)",
        "Visual diff (changed pixels in red)",
    ]


def test_missing_golden_attaches_only_fresh_actual(tmp_path) -> None:
    artifacts = VisualArtifacts(tmp_path, "s", tmp_path / "none.png", started_ns=time.time_ns() - 10**9)
    artifacts.actual.write_bytes(b"a")
    with patch("allure.attach.file") as attach:
        allure_report.attach_missing_golden(artifacts)
    assert _attached(attach) == ["Actual native element screenshot"]


def test_inactive_reporting_attaches_nothing(tmp_path) -> None:
    artifacts = VisualArtifacts(tmp_path, "s", tmp_path / "ref.png", started_ns=time.time_ns() - 10**9)
    artifacts.actual.write_bytes(b"a")
    allure_report.set_active(False)
    with patch("allure.attach.file") as attach, patch("allure.dynamic.parameter") as param:
        allure_report.attach_comparison(artifacts, RESULT, intentional_reference=False)
        allure_report.attach_missing_golden(artifacts)
    attach.assert_not_called()
    param.assert_not_called()


def test_failure_diagnostics_attach_only_current_files(tmp_path) -> None:
    old = time.time() - 3600
    stale = tmp_path / "failure-full-screen.png"
    stale.write_bytes(b"old")
    os.utime(stale, (old, old))
    (tmp_path / "failure-page-source.xml").write_text("<a/>")
    with patch("allure.attach.file") as attach:
        allure_report.attach_failure_diagnostics(tmp_path, time.time_ns() - 10**9)
    assert _attached(attach) == ["Failure page source"]

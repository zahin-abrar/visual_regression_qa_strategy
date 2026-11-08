"""Failed visual comparisons retain a unique, current-run-only evidence package."""

from __future__ import annotations

import json
import os
import time
from unittest.mock import patch

import pytest
from PIL import Image

from visualqa import failure_evidence
from visualqa.visual_check import VisualArtifacts

pytestmark = pytest.mark.unit

PAST = time.time_ns() - 10**9


def _artifacts(tmp_path, *, baseline_color=(0, 0, 0), actual_color=(255, 0, 0)) -> VisualArtifacts:
    artifacts = VisualArtifacts(tmp_path, "sample", tmp_path / "baseline.png", started_ns=PAST)
    Image.new("RGB", (4, 4), baseline_color).save(artifacts.baseline)
    Image.new("RGB", (4, 4), actual_color).save(artifacts.actual)
    return artifacts


def _packages(tmp_path):
    return sorted((tmp_path / "failures").glob("*-sample-*"))


def test_failed_comparison_retains_complete_package_and_keeps_failure(tmp_path):
    artifacts = _artifacts(tmp_path)
    artifacts.path("capture.json").write_text(json.dumps({"session": "abc-123"}))
    artifacts.path("hierarchy.xml").write_text("<h/>")
    artifacts.path("context.png").write_bytes(b"ctx")
    result = artifacts.compare()
    assert result.passed is False  # assertion semantics unchanged: caller still decides
    (package,) = _packages(tmp_path)
    for name in ("actual.png", "reference.png", "diff.png", "comparison.json",
                 "capture.json", "hierarchy.xml", "context.png", "manifest.json"):
        assert (package / name).is_file(), name
    manifest = json.loads((package / "manifest.json").read_text())
    assert manifest["reason"] == "visual comparison failed"
    assert manifest["scenario"] == "sample"
    assert manifest["appium_session_id"] == "abc-123"
    assert manifest["comparison"]["passed"] is False
    assert manifest["comparison"]["changed_pixels"] == 16
    assert set(manifest["files_sha256"]) >= {"actual.png", "reference.png", "diff.png"}
    assert manifest["collection_problems"] == []
    assert (package / "reference.png").read_bytes() == artifacts.baseline.read_bytes()


def test_passing_comparison_retains_nothing(tmp_path):
    artifacts = _artifacts(tmp_path, actual_color=(0, 0, 0))
    assert artifacts.compare().passed is True
    assert not (tmp_path / "failures").exists()


def test_each_failure_gets_its_own_directory_and_earlier_evidence_survives(tmp_path):
    artifacts = _artifacts(tmp_path)
    artifacts.compare()
    (first,) = _packages(tmp_path)
    first_actual = (first / "actual.png").read_bytes()
    Image.new("RGB", (4, 4), (0, 255, 0)).save(artifacts.actual)  # next run overwrites fixed names
    artifacts.compare()
    packages = _packages(tmp_path)
    assert len(packages) == 2 and first in packages
    assert (first / "actual.png").read_bytes() == first_actual


def test_stale_run_files_are_not_retained(tmp_path):
    artifacts = _artifacts(tmp_path)
    stale = artifacts.path("hierarchy.xml")
    stale.write_text("<old/>")
    old = time.time() - 3600
    os.utime(stale, (old, old))
    object.__setattr__(artifacts, "started_ns", time.time_ns() - 10**9 // 2)
    Image.new("RGB", (4, 4), (255, 0, 0)).save(artifacts.actual)
    artifacts.compare()
    (package,) = _packages(tmp_path)
    assert not (package / "hierarchy.xml").exists()


def test_missing_golden_retains_partial_package_and_still_fails(tmp_path):
    artifacts = VisualArtifacts(tmp_path, "sample", tmp_path / "missing.png", started_ns=PAST)
    Image.new("RGB", (2, 2)).save(artifacts.actual)
    with pytest.raises(pytest.fail.Exception, match="Golden missing"):
        artifacts.compare()
    (package,) = _packages(tmp_path)
    assert (package / "actual.png").is_file() and not (package / "reference.png").exists()
    assert json.loads((package / "manifest.json").read_text())["reason"] == "golden missing"


def test_copy_failure_is_recorded_and_does_not_mask_the_visual_result(tmp_path):
    artifacts = _artifacts(tmp_path)
    real_copy = failure_evidence.shutil.copy2

    def flaky(source, target, *a, **k):
        if str(source).endswith("diff.png"):
            raise PermissionError("locked")
        return real_copy(source, target, *a, **k)

    with patch.object(failure_evidence.shutil, "copy2", flaky):
        result = artifacts.compare()
    assert result.passed is False
    (package,) = _packages(tmp_path)
    manifest = json.loads((package / "manifest.json").read_text())
    assert any("diff.png" in p for p in manifest["collection_problems"])
    assert (package / "actual.png").is_file()


def test_unusable_evidence_directory_warns_but_never_raises(tmp_path):
    artifacts = _artifacts(tmp_path)
    (tmp_path / "failures").write_text("a file where the directory should be")
    with pytest.warns(UserWarning, match="could not be retained"):
        result = artifacts.compare()
    assert result.passed is False
    with pytest.warns(UserWarning):
        assert failure_evidence.retain(artifacts, reason="x") is None

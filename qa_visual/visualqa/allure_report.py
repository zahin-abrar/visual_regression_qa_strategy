"""Optional Allure evidence helpers; inert unless pytest runs with --alluredir.

Only files modified at or after ``since_ns`` are attached, so generated artifacts
left over from earlier runs are never presented as evidence for the current test.
"""

from __future__ import annotations

from pathlib import Path

import allure
import pytest
from allure_commons.types import AttachmentType

INTENTIONAL_SUITE = "Intentional reference-mismatch demonstration (not an app regression)"
NORMAL_SUITE = "Android visual regression"
# True only while a qa_scenario test runs, so unit tests that exercise the
# comparison helpers do not add screenshots to the visual report.
_active = False


def set_active(value: bool) -> None:
    global _active
    _active = value


def attach_if_fresh(path: Path, name: str, kind: AttachmentType, since_ns: int) -> bool:
    """Attach ``path`` only if this execution produced it."""
    if path.is_file() and path.stat().st_mtime_ns >= since_ns:
        allure.attach.file(str(path), name=name, attachment_type=kind)
        return True
    return False


def label_visual_test(node: pytest.Item, scenario: str, profile: str) -> None:
    """Human-readable identity for a scenario test; intentional demos are labelled as such."""
    set_active(True)
    intentional = node.get_closest_marker("intentional_failure") is not None
    # allure-pytest resets the title (and description) from the test function / markers
    # when the call phase starts, so dynamic.title/description set here would be lost.
    # The display-name attribute is the plugin's own storage for @allure.title.
    node.obj.__allure_display_name__ = node.name.removeprefix("test_").replace("_", " ")
    allure.dynamic.parent_suite(INTENTIONAL_SUITE if intentional else NORMAL_SUITE)
    allure.dynamic.parameter("scenario", scenario)
    allure.dynamic.parameter("platform", "Android (Appium UiAutomator2)")
    allure.dynamic.parameter("golden_profile", profile)
    if intentional:
        allure.dynamic.tag("intentional-reference-mismatch-demo")
        node.add_marker(pytest.mark.allure_description(
            "INTENTIONAL reference-mismatch demonstration. The real breaking_news UI is "
            "captured and compared with a deliberately incorrect reference "
            "(demo_assets/intentional_mismatch_breaking_news.png). A failure here is the "
            "expected outcome and is NOT an application regression."
        ))


def attach_comparison(artifacts, result, *, intentional_reference: bool) -> None:
    """Attach evidence for one comparison; ``artifacts`` is a VisualArtifacts."""
    if not _active:
        return
    since = artifacts.started_ns
    allure.dynamic.parameter("changed_pixels", result.changed_pixels)
    allure.dynamic.parameter("total_pixels", result.total_pixels)
    allure.dynamic.parameter("changed_ratio", f"{result.changed_ratio:.6%}")
    allure.dynamic.parameter("allowed_ratio", f"{result.max_changed_ratio:.3%}")
    allure.dynamic.parameter("channel_tolerance", result.channel_tolerance)
    allure.dynamic.parameter("size_match", result.size_match)
    ref_name = (
        "Intentionally INCORRECT reference (demo, not an approved golden)"
        if intentional_reference else "Approved golden"
    )
    png = AttachmentType.PNG
    # The reference is a committed file, not a run artifact: always attach it.
    if artifacts.baseline.is_file():
        allure.attach.file(str(artifacts.baseline), name=ref_name, attachment_type=png)
    attach_if_fresh(artifacts.actual, "Actual native element screenshot", png, since)
    attach_if_fresh(artifacts.path("diff.png"), "Visual diff (changed pixels in red)", png, since)
    attach_if_fresh(artifacts.path("context.png"), "Full-screen context (diagnostic only)", png, since)
    attach_if_fresh(artifacts.path("comparison.json"), "Comparison metrics", AttachmentType.JSON, since)
    attach_if_fresh(artifacts.path("capture.json"), "Capture metadata", AttachmentType.JSON, since)
    attach_if_fresh(artifacts.path("hierarchy.xml"), "UI hierarchy", AttachmentType.XML, since)


def attach_missing_golden(artifacts) -> None:
    if not _active:
        return
    attach_if_fresh(artifacts.actual, "Actual native element screenshot", AttachmentType.PNG, artifacts.started_ns)
    attach_if_fresh(artifacts.path("context.png"), "Full-screen context (diagnostic only)", AttachmentType.PNG, artifacts.started_ns)


def attach_failure_diagnostics(folder: Path, since_ns: int) -> None:
    """Driver diagnostics written by android_session during THIS execution only."""
    attach_if_fresh(folder / "failure-full-screen.png", "Failure full-screen diagnostic", AttachmentType.PNG, since_ns)
    attach_if_fresh(folder / "failure-page-source.xml", "Failure page source", AttachmentType.XML, since_ns)
    for name in ("screenshot-error.txt", "page-source-error.txt"):
        attach_if_fresh(folder / name, name, AttachmentType.TEXT, since_ns)

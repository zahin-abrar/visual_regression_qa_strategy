"""Shared artifact paths and comparison support; tests own UI assertions."""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from visualqa import allure_report, failure_evidence
from visualqa.image_diff import Comparison, compare_png, write_result

if TYPE_CHECKING:
    from appium.webdriver.webdriver import WebDriver

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class VisualArtifacts:
    """One capture's existing profile-specific paths; never writes a baseline."""

    output: Path
    prefix: str
    baseline: Path
    # Evidence older than this was not produced by the current test (Allure only).
    started_ns: int = field(default_factory=time.time_ns, compare=False)

    @classmethod
    def for_scenario(cls, scenario: str, *, baseline: Path | None = None) -> VisualArtifacts:
        profile = os.environ.get("VVP_GOLDEN_PROFILE", "pixel10-api37")
        if not re.fullmatch(r"[a-z0-9_-]+", profile):
            pytest.fail("VVP_GOLDEN_PROFILE must contain only lowercase letters, digits, _ and -")
        output = ROOT / "artifacts" / "android" / profile
        output.mkdir(parents=True, exist_ok=True)
        reference = baseline if baseline is not None else ROOT / "baselines" / "android" / profile / f"{scenario}.png"
        return cls(output, scenario, reference)

    def path(self, suffix: str) -> Path:
        return self.output / f"{self.prefix}.{suffix}"

    @property
    def actual(self) -> Path:
        return self.path("actual.png")

    def save_context(self, driver: WebDriver) -> None:
        """Full screen is diagnostic only; components capture native elements."""
        self.path("context.png").write_bytes(driver.get_screenshot_as_png())

    def save_hierarchy(self, driver: WebDriver) -> None:
        self.path("hierarchy.xml").write_text(driver.page_source, encoding="utf-8")

    def save_metadata(self, metadata: dict[str, object]) -> None:
        self.path("capture.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    def compare(self, *, use_environment_tolerances: bool = False) -> Comparison:
        """Compare after capture; retain the caller's existing tolerance policy."""
        assert self.actual.is_file() and self.actual.stat().st_size > 0
        if not self.baseline.is_file():
            allure_report.attach_missing_golden(self)
            failure_evidence.retain(self, reason="golden missing")
            pytest.fail(
                f"Golden missing. An ACTUAL native screenshot was saved at {self.actual}. "
                "Review it and make a second capture to check stability before human approval. "
                f"Expected reference: {self.baseline}. No baseline is approved automatically."
            )
        if use_environment_tolerances:
            result = compare_png(
                self.baseline, self.actual, self.path("diff.png"),
                channel_tolerance=int(os.environ.get("VVP_CHANNEL_TOLERANCE", "12")),
                max_changed_ratio=float(os.environ.get("VVP_MAX_CHANGED_RATIO", "0.002")),
            )
        else:
            result = compare_png(self.baseline, self.actual, self.path("diff.png"))
        write_result(result, self.path("comparison.json"))
        # Attach before the caller's final assertion so failures keep their evidence.
        allure_report.attach_comparison(
            self, result, intentional_reference=self.baseline.is_relative_to(ROOT / "demo_assets")
        )
        if not result.passed:
            failure_evidence.retain(self, result, reason="visual comparison failed")
        return result

    def failure_message(self, result: Comparison) -> str:
        return (
            f"Visual regression: changed={result.changed_pixels}/{result.total_pixels} "
            f"({result.changed_ratio:.3%}), allowed={result.max_changed_ratio:.3%}; "
            f"same_size={result.size_match}. Review {self.actual}, {self.baseline}, "
            f"{self.path('diff.png')}, {self.path('comparison.json')}. "
            "Do NOT auto-regenerate the golden."
        )

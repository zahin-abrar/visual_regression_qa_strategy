"""Retain a unique, immutable evidence package for every failed visual comparison.

The fixed-name artifacts in ``artifacts/android/<profile>/`` are overwritten by the next
run. This module copies the current run's evidence into
``<output>/failures/<UTC timestamp>-<prefix>-<pid>/`` and never raises: a problem while
collecting evidence is recorded and warned about, so the original visual failure stays
the primary result.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import sys
import warnings
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

# (suffix of <prefix>.<suffix>, name inside the package); only files written by THIS test run.
_RUN_FILES = (
    ("actual.png", "actual.png"),
    ("diff.png", "diff.png"),
    ("comparison.json", "comparison.json"),
    ("capture.json", "capture.json"),
    ("hierarchy.xml", "hierarchy.xml"),
    ("context.png", "context.png"),
)
# Driver diagnostics written by android_session when the session body failed.
_DIAGNOSTICS = ("failure-full-screen.png", "failure-page-source.xml")
_ENV_PREFIX = "VVP_"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _unique_dir(root: Path, prefix: str) -> Path:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    base = f"{stamp}-{prefix}-{os.getpid()}"
    root.mkdir(parents=True, exist_ok=True)
    for n in range(100):
        candidate = root / (base if n == 0 else f"{base}-{n}")
        try:
            candidate.mkdir()
            return candidate
        except FileExistsError:
            continue
    raise FileExistsError(f"No unique evidence directory under {root}")


def retain(artifacts, result=None, *, reason: str) -> Path | None:
    """Copy this run's evidence; return the package directory or ``None`` on failure."""
    try:
        return _retain(artifacts, result, reason)
    except Exception as error:  # evidence must never mask the primary failure
        warnings.warn(f"Visual failure evidence could not be retained: {error!r}", stacklevel=2)
        return None


def _retain(artifacts, result, reason: str) -> Path:
    package = _unique_dir(artifacts.output / "failures", artifacts.prefix)
    since = artifacts.started_ns
    problems: list[str] = []
    files: dict[str, str] = {}

    def copy(source: Path, name: str, *, always: bool = False) -> None:
        try:
            if source.is_file() and (always or source.stat().st_mtime_ns >= since):
                shutil.copy2(source, package / name)
                files[name] = _sha256(package / name)
        except Exception as error:
            problems.append(f"{name}: {error!r}")

    copy(artifacts.baseline, "reference.png", always=True)  # committed file, not a run artifact
    for suffix, name in _RUN_FILES:
        copy(artifacts.path(suffix), name)
    for name in _DIAGNOSTICS:
        copy(artifacts.output / name, name)

    session = None
    try:
        capture = artifacts.path("capture.json")
        if capture.is_file() and capture.stat().st_mtime_ns >= since:
            session = json.loads(capture.read_text(encoding="utf-8")).get("session")
    except Exception as error:
        problems.append(f"capture.json parse: {error!r}")

    manifest = {
        "reason": reason,
        "scenario": artifacts.prefix,
        "test": os.environ.get("PYTEST_CURRENT_TEST"),
        "retained_at_utc": datetime.now(timezone.utc).isoformat(),
        "run_started_utc": datetime.fromtimestamp(since / 1e9, timezone.utc).isoformat(),
        "reference_source": str(artifacts.baseline),
        "comparison": asdict(result) if result is not None else None,
        "appium_session_id": session,
        "appium_note": "Appium server logs are external; locate this session id in the server log.",
        "environment": {
            "platform": platform.platform(),
            "python": sys.version.split()[0],
            **{k: v for k, v in sorted(os.environ.items()) if k.startswith(_ENV_PREFIX)},
        },
        "files_sha256": files,
        "collection_problems": problems,
    }
    (package / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    print(f"\n[visual-evidence] retained failure evidence: {package}")
    return package

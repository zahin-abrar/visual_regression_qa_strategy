#!/usr/bin/env python3
"""Validate a previous build run before its APK is reused by the visual workflow.

Checks (all must pass): numeric run id; run belongs to this repository; run is the
Android build workflow; run completed successfully; the artifact exists and is not
expired; the source commit is an ancestor of the commit under test and no
APK/visual-affecting file changed between them. Workflow-only and documentation
changes do not invalidate the APK. Uses the `gh` CLI with the built-in GITHUB_TOKEN.
Pure functions are importable for local testing.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

BUILD_WORKFLOW_PATH = ".github/workflows/android-build.yml"
ARTIFACT_NAME = "android-debug-apk-x86_64"

# Paths whose change makes a previously built APK / its visual comparison not comparable.
INCOMPATIBLE_PREFIXES = (
    "app/",                        # application source, fixtures, native config, lockfile
    "qa_visual/baselines/",        # approved golden references
    "qa_visual/demo_assets/",
    "qa_visual/visualqa/",         # capture, comparison thresholds, failure evidence
    "qa_visual/tests/",            # scenario definitions
)
INCOMPATIBLE_FILES = ("qa_visual/conftest.py", "qa_visual/requirements.txt", "pytest.ini")
# Documentation-only exceptions (never affect the APK or comparison).
DOC_SUFFIXES = (".md",)


class Rejected(Exception):
    """The source run or its artifact cannot be used; message is user-facing."""


def validate_run_id(value):
    if not re.fullmatch(r"[1-9][0-9]{5,19}", value or ""):
        raise Rejected(f"source_run_id must be a numeric GitHub run ID (digits only), got {value!r}")
    return value


def validate_run(run, repo):
    full = (run.get("repository") or {}).get("full_name")
    head = (run.get("head_repository") or {}).get("full_name")
    if full != repo or head != repo:
        raise Rejected(f"run belongs to {full!r} (head repository {head!r}), not {repo!r}")
    path = (run.get("path") or "").split("@")[0]
    if path != BUILD_WORKFLOW_PATH:
        raise Rejected(f"run is workflow {path!r}, expected {BUILD_WORKFLOW_PATH!r}")
    if run.get("status") != "completed" or run.get("conclusion") != "success":
        raise Rejected(f"run status={run.get('status')!r} conclusion={run.get('conclusion')!r}; a completed, successful build is required")
    if not re.fullmatch(r"[0-9a-f]{40}", run.get("head_sha") or ""):
        raise Rejected("run has no valid head_sha")
    return run["head_sha"]


def find_artifact(artifacts, now=None):
    now = now or datetime.now(timezone.utc)
    matches = [a for a in artifacts if a.get("name") == ARTIFACT_NAME]
    if not matches:
        names = ", ".join(a.get("name", "?") for a in artifacts) or "none"
        raise Rejected(f"artifact {ARTIFACT_NAME!r} not found on the source run (artifacts: {names})")
    art = matches[0]
    expires = art.get("expires_at")
    if art.get("expired") or (expires and datetime.fromisoformat(expires.replace("Z", "+00:00")) <= now):
        raise Rejected(f"artifact {ARTIFACT_NAME!r} has expired ({expires}); run the Android build workflow again and use the new run ID")
    if not art.get("size_in_bytes"):
        raise Rejected(f"artifact {ARTIFACT_NAME!r} is empty")
    return art


def incompatible_changes(paths):
    bad = []
    for p in paths:
        p = p.strip()
        if not p or p.endswith(DOC_SUFFIXES):
            continue
        if p.startswith(INCOMPATIBLE_PREFIXES) or p in INCOMPATIBLE_FILES:
            bad.append(p)
    return bad


def gh_json(endpoint):
    out = subprocess.run(["gh", "api", endpoint], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def git(*args):
    return subprocess.run(["git", *args], capture_output=True, text=True)


def check_commits(source_sha, current_sha):
    if git("cat-file", "-e", f"{source_sha}^{{commit}}").returncode != 0:
        raise Rejected(f"source commit {source_sha} is not in this checkout's history (different branch?); rebuild the APK from this revision")
    if git("merge-base", "--is-ancestor", source_sha, current_sha).returncode != 0:
        raise Rejected(f"source commit {source_sha} is not an ancestor of {current_sha}; rebuild the APK from this revision")
    diff = git("diff", "--name-only", f"{source_sha}..{current_sha}")
    if diff.returncode != 0:
        raise Rejected(f"cannot diff {source_sha}..{current_sha}: {diff.stderr.strip()}")
    return diff.stdout.splitlines()


def main():
    repo, current = os.environ["GITHUB_REPOSITORY"], os.environ["GITHUB_SHA"]
    run_id = validate_run_id(os.environ.get("SOURCE_RUN_ID", ""))
    run = gh_json(f"repos/{repo}/actions/runs/{run_id}")
    source_sha = validate_run(run, repo)
    art = find_artifact(gh_json(f"repos/{repo}/actions/runs/{run_id}/artifacts?per_page=100").get("artifacts", []))
    changed = check_commits(source_sha, current)
    bad = incompatible_changes(changed)
    if bad:
        raise Rejected("APK/visual inputs changed since the source build; rebuild the APK. Changed files:\n  " + "\n  ".join(bad))
    lines = [
        "### Source APK provenance", "",
        "| Item | Value |", "| --- | --- |",
        f"| Source build run | [{run_id}]({run.get('html_url')}) |",
        f"| Source build commit | `{source_sha}` |",
        f"| Visual workflow commit | `{current}` |",
        f"| Artifact | `{ARTIFACT_NAME}` ({art['size_in_bytes']} bytes, expires {art.get('expires_at')}) |",
        f"| Files changed since source commit | {len(changed)} (none APK- or visual-affecting; {len(changed) - len(bad)} workflow/doc/other) |",
    ]
    text = "\n".join(lines) + "\n"
    print(text)
    for var, value in (("GITHUB_STEP_SUMMARY", text),):
        if os.environ.get(var):
            with open(os.environ[var], "a", encoding="utf-8") as fh:
                fh.write(value + "\n")
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as fh:
            fh.write(f"source_sha={source_sha}\n")


if __name__ == "__main__":
    try:
        main()
    except Rejected as exc:
        print("::error title=Source APK rejected::" + str(exc).replace(chr(10), "%0A"))
        sys.exit(1)
    except subprocess.CalledProcessError as exc:
        print(f"::error title=GitHub API call failed::{exc.stderr.strip() if exc.stderr else exc}")
        sys.exit(1)

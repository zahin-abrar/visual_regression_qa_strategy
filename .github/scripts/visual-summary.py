#!/usr/bin/env python3
"""Advisory visual-test summary for GitHub. Reads pytest's JUnit XML; never changes the exit code."""
import os
import sys
import xml.etree.ElementTree as ET

rc = os.environ.get("PYTEST_RC", "?")
expected = int(os.environ.get("EXPECTED_VISUAL", "5"))
junit = sys.argv[1]
notes = []
passed = failed_cmp = failed_other = errors = skipped = 0
rows = []
try:
    for case in ET.parse(junit).getroot().iter("testcase"):
        name = case.get("name", "?")
        bad = case.find("failure")
        err = case.find("error")
        if bad is not None:
            msg = (bad.get("message") or "") + (bad.text or "")
            short = (bad.get("message") or "")[:160]
            if "Visual regression:" in msg or "Golden missing" in msg:
                failed_cmp += 1
                rows.append((name, "COMPARISON MISMATCH", short))
            else:
                failed_other += 1
                rows.append((name, "FAILED, not a comparison (likely infrastructure)", short))
        elif err is not None:
            errors += 1
            rows.append((name, "ERROR (setup/infrastructure)", (err.get("message") or "")[:160]))
        elif case.find("skipped") is not None:
            skipped += 1
        else:
            passed += 1
except (OSError, ET.ParseError) as exc:
    notes.append(f"> No usable JUnit report ({exc}). pytest did not complete; see the infrastructure logs artifact.")

executed = passed + failed_cmp + failed_other + errors
out = [f"## Android visual regression (ADVISORY; pytest exit code {rc})", "",
       "These results do not block the workflow. A mismatch is **unresolved**: it may be Linux/CI emulator drift "
       "against the Windows-reviewed goldens or a real regression. Goldens and thresholds are never changed automatically.",
       ""] + notes
out += [f"| Passed | Comparison mismatch | Other failure | Error | Skipped | Not executed (of {expected}) |",
        "| --- | --- | --- | --- | --- | --- |",
        f"| {passed} | {failed_cmp} | {failed_other} | {errors} | {skipped} | {max(expected - executed - skipped, 0)} |"]
if rows:
    out += ["", "| Test | Classification | Message |", "| --- | --- | --- |"]
    out += [f"| `{n}` | {c} | {m.replace('|', '/')} |" for n, c, m in rows]
if rc == "0" and passed == expected:
    out.append("\nAll expected visual tests passed in this environment.")
elif rc != "0":
    out.append("\n**Advisory failure.** Artifacts: `visual-evidence` (actual/reference/diff/metadata), "
               "`visual-allure-report`, `visual-allure-results`, `visual-infra-logs`.")
text = "\n".join(out) + "\n"
print(text)
path = os.environ.get("GITHUB_STEP_SUMMARY")
if path:
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(text)

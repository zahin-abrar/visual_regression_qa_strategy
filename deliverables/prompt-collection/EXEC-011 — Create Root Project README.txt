# EXEC-011 — Create Root Project README

**Project:** `D:\Projects\visual_regression_qa_strategy`  
**Phase:** EXECUTION  
**Previous task:** EXEC-010 — PASS

## Objective

Create a concise, professional root-level `README.md` that serves as the entry point for the Axel Springer mobile screenshot-testing take-home submission.

Preserve the existing detailed `qa_visual/README.md`.

Do not duplicate the entire runner documentation.

## Step 1 — Inspect the repository

Read:

- Root `AGENTS.md`, if present
- Existing root `README.md`, if present
- `qa_visual/README.md`
- `docs/AGENT_TASK_HISTORY.md`
- Existing relevant project documents and artifact paths

Confirm the implemented capabilities, test results and actual file locations.

Do not invent missing deliverables.

## Step 2 — Create or update root README

Use these sections:

### Project overview

Explain that this repository demonstrates a maintainable Android/iOS screenshot-testing strategy using a real React Native news application.

Clearly distinguish the **executed Android prototype** from the **proposed cross-platform strategy**.

### What has been demonstrated

Summarize verified evidence:

- Real Volksverpetzer application.
- Deterministic long-headline fixture.
- Native Android Appium/UiAutomator2 capture.
- Minimal Python/pytest Screen Object and Component Object architecture.
- Human-reviewed golden baseline.
- Two byte-identical repeat captures.
- Passing local visual regression test.
- Diff and comparison-metric artifacts.

Do not claim committed Git history, passing CI, iOS execution or deliberate failing-regression evidence unless separately verified.

### Architecture overview

Describe the responsibilities of:

- `app/`
- `qa_visual/`
- Screen and Component Objects
- Android driver/session setup
- Pillow comparison utility
- Device-specific golden references

Keep this concise and link to the runner README for implementation details.

### Quick start

Provide the minimal commands to run the Android visual test once the emulator, development app, fixture-enabled Metro and Appium server are ready.

Use the existing verified Python command.

Link to `qa_visual/README.md` for the full prerequisites, environment setup, golden workflow and troubleshooting.

### Documentation

Link to the cross-platform strategy and AI prompt disclosure only if their intended paths can be confirmed.

If these deliverables aren't finalized, use accurate pending status rather than a broken link.

### Results and limitations

Summarize the verified local PASS and main constraints.

### Attribution and license

Identify the original Volksverpetzer application and its upstream project, preserving existing attribution and licensing information.

Do not assert license permissions without checking the actual repository files.

## Step 3 — Verify the documentation

Check that:

1. The root README matches the actual repository.
2. Every included relative link resolves, or any pending document is clearly marked.
3. All execution claims match recorded evidence.
4. The original employer challenge PDF is not included or linked as public repository content.
5. Private `.project-private/` content is not exposed.
6. The detailed runner README remains available and unchanged.

## Restrictions

- Modify only the root `README.md` and task history.
- Do not modify the app, tests, framework or golden.
- Do not create or regenerate screenshots.
- Do not run Appium sessions.
- Do not install dependencies.
- Do not initialize Git.
- Do not publish the repository.
- Do not begin the strategy document in this task.
- Do not automatically proceed to EXEC-012.

## Task history

Append EXEC-011 to `docs/AGENT_TASK_HISTORY.md`, including verification results and files changed.

## Completion report

Return:

1. EXEC-011 status: PASS / FAIL / BLOCKED
2. Root README sections created
3. Links and commands checked
4. Attribution/license findings
5. Files changed
6. Remaining submission gaps
7. Recommended next smallest task

**Stop after EXEC-011. Await review and authorization.**
# EXEC-010 — Verify and Complete Demo Reproduction README

**Project:** `D:\Projects\visual_regression_qa_strategy`  
**Phase:** EXECUTION  
**Previous task:** EXEC-009 — PASS

## Objective

Review and improve the existing documentation so another engineer can understand how to prepare, run, inspect and intentionally update the Android visual regression test.

Document only the architecture and procedures actually implemented.

The README must distinguish verified commands from setup or regeneration procedures that have not been executed end-to-end.

**This is a documentation task, not a framework development task.**

## Step 1 — Inspect the implemented workflow

Read:

- Root `AGENTS.md`, if present
- `docs/AGENT_TASK_HISTORY.md`
- Root README, if present
- `qa_visual/README.md`
- `qa_visual/requirements.txt`
- Existing pytest configuration
- Driver/session configuration
- Screen and Component Objects
- Fixture activation logic in `app/`
- Golden and artifact paths
- Image-comparison implementation

Identify the exact implemented commands and requirements.

Do not assume previous experimental commands are the correct final workflow.

## Step 2 — Complete the README

Update `qa_visual/README.md` to document:

### Purpose and scope

- Real Volksverpetzer React Native application.
- Android Appium/UiAutomator2 screenshot-testing demonstration.
- Deterministic `long_headline` scenario.
- Minimal POM with `HomeScreen` and `ArticleCard`.
- Independent Pillow-based comparison utility.
- Actual verified scope: Android only; no executed iOS tests or CI pipeline.

### Environment

Document the versions verified during execution:

- Python 3.13.1
- Appium 3.3.0
- UiAutomator2 7.1.2
- Appium-Python-Client 5.2.4
- pytest 8.4.2
- Pillow 11.3.0
- Android emulator Pixel_10, API 37
- Emulator configuration: 1080 × 2424, 420 dpi, approximately 4 GB RAM

Document any additional required environment values from actual runner configuration.

Do not imply that these are the only compatible versions.

### Installation and startup

Provide clear Windows PowerShell instructions for:

1. Required Android and Java tooling.
2. Preparing the emulator.
3. Starting the development application with `EXPO_PUBLIC_QA_SCENARIO=long_headline`.
4. Starting the existing Appium server using `appium.cmd`.
5. Creating the Python virtual environment.
6. Installing pinned dependencies.

Distinguish installation/build commands already verified in task history from those not re-executed during this task.

Do not rebuild or reinstall the app merely to document setup.

### Running tests

Document exact commands for:

- Unit tests.
- Test collection.
- The single Android visual integration test.

Use the existing `.venv` and test configuration.

### Golden image workflow

Explain:

- Where golden images live.
- Why the approved golden is platform/device-specific.
- How screenshots are captured.
- How actual and golden images are compared.
- The configured per-channel tolerance and maximum changed-pixel ratio.
- How human review and approval work.
- How to propose and deliberately promote an updated baseline.

Include a reproducible, explicit **manual regeneration/promotion procedure** using the actual runner and verified baseline path.

Make it clear that regeneration requires reviewing the newly captured PNG before replacement.

Do not present automatic golden overwriting as an acceptable workflow.

Label any regeneration commands that have not themselves been executed end-to-end as documented procedures rather than verified successful operations.

### Failure artifacts

Explain where to find:

- Actual PNG
- Full-screen context PNG
- Difference PNG
- Comparison JSON

Explain the distinction between a visual test failure and a missing or unapproved baseline.

### Limitations

Document the known current constraints:

- One Android fixture scenario.
- No native iOS execution.
- No verified CI pipeline.
- Android parent-element locator depends on the current accessibility hierarchy.
- Snapshot consistency depends on the pinned rendering environment.
- Golden is present locally but repository commit status is not yet verified.

## Step 3 — Documentation verification

Verify that:

1. Referenced files and directories exist.
2. Documented CLI arguments and pytest commands match the implementation.
3. All relative working directories are correct.
4. The baseline path matches the actual test.
5. The README doesn't claim unimplemented capabilities.
6. The original private employer challenge PDF is not referenced as a file to publish.

Use read-only inspection commands.

Do not run a new Appium integration test unless there is a compelling documentation discrepancy; report that discrepancy instead.

## Acceptance criteria

EXEC-010 is PASS when:

- README describes the verified working demo.
- Installation, execution and baseline-review procedures are clear.
- Unit and visual test commands match existing implementation.
- Baseline regeneration is explicitly human-controlled.
- Artifacts and troubleshooting are documented.
- Unverified setup steps are identified honestly.
- No application, test, comparator, baseline or environment changes occur.

## Restrictions

- Do not modify framework or application source code.
- Do not modify existing golden images.
- Do not execute baseline regeneration.
- Do not create new screenshots.
- Do not install dependencies.
- Do not alter Appium or emulator configuration.
- Do not initialize Git.
- Do not start CI setup.
- Do not write the strategy document in this task.
- Do not automatically proceed to EXEC-011.

## Task history

Append EXEC-010 to:

`docs/AGENT_TASK_HISTORY.md`

Record:

- Status: PASS / FAIL / BLOCKED
- Documentation files modified
- Implemented commands and paths checked
- Verification commands and results
- Any documentation claims that remain unverified
- Remaining blockers
- Recommended next smallest task

Preserve all previous entries.

## Completion report

Return:

1. EXEC-010 status
2. README sections updated
3. Commands and paths verified
4. Baseline regeneration and review procedure
5. Any untested setup instructions
6. Files changed
7. Remaining documentation gaps
8. Recommended next task

**Stop after EXEC-010. Await review and authorization.**

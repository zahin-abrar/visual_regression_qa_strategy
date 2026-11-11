# EVAL-001 closure (HEAD at start 79126a9) - private, not committed

## Status
Development and CI troubleshooting FROZEN. No further visual runs, APK rebuilds, goldens, thresholds, fixtures or app changes.

## Requirement-to-evidence audit
| ID | Status | Evidence |
|---|---|---|
| R01 | Met | deliverables/strategy.md + strategy.pdf (3 pages, regenerated with Chrome headless; page rendering not visually proofread, no PDF rasteriser available) |
| R02 | Met | strategy s1/s4 (hybrid; Appium+pytest chosen; Paparazzi/Roborazzi/swift-snapshot-testing alternatives) |
| R03 | Met | __DEV__ fixture provider in app/, deep-link qa_scenario seam, Appium only drives; reference/patches + NOTICE |
| R04 | Met | 5 PNGs in qa_visual/baselines/android/pixel10-api37, README approval flow, strategy s6 |
| R05 | Partly | strategy s7 + 2 manual advisory workflows. No PR trigger / not a required check (P2, deliberate) |
| R06 | Met (written), partly demonstrated | pinned emulator/image, cold-launch isolation, tiering s7/s8; flake episodes recorded |
| R07 | Met | local 5/5 zero px; GitHub: run 42620071563 breaking_news pass; full suite 4/5 |
| R08 | Mostly | banner, long-headline teaser, dark, no-image, empty state. No paywalled/premium example (P2; listed in nightly matrix) |
| R09 | Met | goldens committed |
| R10 | Met, not re-executed here | README/qa_visual README commands last run in earlier EXEC items; workflow steps proven on GitHub; not re-run in EVAL-001 (instructed not to) |
| R11 | P1 open | deliverables/ai_prompt_disclosure.md is an agent DRAFT; human must compile/verify from all conversations |
| R12 | Met | strategy s5, s8 |
| E01 | Met | intentional_failure demo (92.41% changed) |
| E02 | Met | 5 variants (long German headline, no image, dark, empty) |
| E03 | Below | walkthrough |

## Findings
- P0: none found. No employer PDF, secrets, evidence ZIPs or debug logs are tracked (git ls-files scan clean; app/.env.sample holds only APP and EXPO_NO_TELEMETRY).
- P1: (1) Full suite not green: no_image native SIGSEGV unresolved; disclosed in README and strategy; do not attempt a fix now. (2) AI disclosure draft needs human completion (30-60 min). (3) NOTICE.md: brand-asset permissions unresolved, keep repo private or remove/replace assets before public use (1-2 h). (4) Commits authored with a personal Gmail address (decision pending); history holds an earlier sanitized, partial docs/ai_prompts_used.md.
- P2: no PR trigger; no paywall example; strategy.pdf not visually proofread; ten untracked upstream app/ entries must never be added (no `git add -A`); full-suite run ID unrecorded; recent commits carry a Co-Authored-By trailer.

## Frozen evidence index
- APK build run 42616325655 (commit d48e8d7); artifact expires about 2026-11-16.
- Isolated visual run 42620071563 (commit d48e8d7), visual_scope=breaking_news: PASS, 0 changed px.
- Full-suite run on the same APK: run ID UNCONFIRMED. pytest 4 passed, 1 failed, 130 deselected, 296.55 s. breaking_news 1028x493, dark_article 1028x1237, empty_feed 1028x309, long_headline 1028x1237: all 0 px. no_image broken (TimeoutException): process died with SIGSEGV SEGV_ACCERR on mqt_v_js at about 17:38:51Z in libreactnative.so MountingCoordinator::pullTransaction, 16 KB image (google/sdk_gphone16k_x86_64, CE2A.260420.051.A2). An earlier run showed a similar crash. NOT a passing suite.
- Commit 79126a9 added visual_scope=no_image; the isolated no_image run was NOT executed (GitHub platform errors); cause unproven.
- Pytest results are advisory (continue-on-error); job status is not test status.
- Local evidence stays in .local-evidence/ (ignored, untouched).

## Known limitations / follow-ups
Android only; manual advisory CI; dev client + Metro, not a release build; Expo dev-menu overlay dismissed by the runner; Linux-vs-Windows golden match shown for 4 scenarios only; no_image crash; brand assets; no paywall scenario. Follow-ups (not started): isolated no_image run when GitHub is healthy; release-like build; PR trigger with a 1-2 scenario smoke; iOS pilot.

## 3-5 minute walkthrough
1. (30 s) Problem: AI-assisted builds arrive faster than manual visual QA; need cheap, trustworthy PR feedback.
2. (60 s) Choice: hybrid. Here Appium+pytest drives a real React Native app (reusable across platforms) with a fixture seam inside the app, because Appium is a driver, not a mock. Fast component snapshots where the stack allows.
3. (60 s) Show: five scenarios by deep link, marker check, Pillow comparison, per-platform goldens; run one test; show the intentional-failure diff.
4. (60 s) CI: build workflow, reuse APK, emulator, Metro/Appium, artifacts. Real result: 4 of 5 pixel-exact on GitHub.
5. (45 s) Honesty: no_image native crash unresolved, advisory CI, no iOS run, brand-asset caveat.
6. (30 s) Rollout: pilot, ownership, measure, then gate.

## Likely interview questions
1. How do you know the fixture replaces live data in the real UI? - Dev-only provider maps synthetic articles through the app's real WordPress mapping into Feed/ArticlePost; identity marker verified before capture; four scenarios match pixel for pixel on a different OS host.
2. Why Appium rather than Paparazzi/swift-snapshot-testing? - Cross-platform reuse and real-app integration; component snapshots recommended where the stack fits (they do not render RN). Cost: slower, emulator flake.
3. The full suite failed on GitHub; is it green? - No. 4 pass pixel-exact; no_image crashed natively before capture; cause unproven (fixture, order, 16 KB image, resources); the isolating run was prepared but blocked by platform errors. Not fixed, not gating.
4. How do you govern goldens and flakiness? - Per platform/profile PNGs, human approval via PR, never auto-regenerate, no retries on pixel mismatch, separate infra from visual failures, quarantine with owner and deadline.
5. How would you roll this out and measure value? - Pilot a few high-risk components on one profile, advisory first, then small PR smoke plus nightly matrix; measure feedback time, false positives, escaped visual defects, flake rate, cost; no invented savings.

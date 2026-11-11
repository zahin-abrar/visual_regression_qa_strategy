> **CURRENT STATUS (2026-11-01): The human has approved `vvp_app` + the test-only fixture fetcher + Appium/pytest + one Android scenario. Phase is EXECUTION. Older OPEN statements below are historical; see the latest section at the bottom.**

# Current state and agent handoff

> **Latest authorized direction:** `vvp_app` FIRST for bounded PLANNING feasibility (2026-11-01); implementation, mocking and runner remain **unapproved**. See the latest session addendum at the end of this complete file. Previous JetNews-first suggestions are superseded as *spike priority*, not erased.

**Last updated:** 2026-11-01 — post-scaffold architecture discussion incorporated.
**Phase:** PLANNING — **start with SUT finalization and mocking strategy**.
**Next fixed event:** Tue 2026-11-03, 14:00 CET interview/demo.
**Decision owner:** Human candidate. **Host environment:** Windows is user-reported; exact installed Android emulator, SDK, Java/Node/Flutter/Python/Appium setup **unverified**.

## Confirmed employer facts (original PDF)

- 1–3 page strategy for both Android + iOS, runnable screenshot demo on **at least one platform** using real UI with deterministic mocked data, included golden PNGs, README, prompt log, and ideally failing visual diff.
- Small owned sample app or open-source adaptation allowed; actual employer codebase not provided.
- Both off-device snapshots and **Appium/Maestro + local emulators / device cloud + visual diff** explicitly permitted. Mocking via test-build fixture replacement **or** local stub server. Cloud **not required**.

## User goals and discussion-derived direction (not final implementation approval)

- **Interview insight:** AI-assisted development speeds up builds; QA manually revalidating frequent builds becomes a bottleneck.
- Prefer CI-friendly, scalable tests, **shared automation core**, fewer duplicate Android/iOS suites; platform-specific code is acceptable when more efficient.
- **Appium + Python/pytest** is a leading candidate because it supports shared scenarios and real device rendering, but mock-data injection is a distinct concern and runtime/CI costs must be considered.
- **Hybrid** production strategy likely strongest (many fast component snapshots + smaller Appium screen journeys), although the demo needs only a narrow verified slice.
- Prefer local Android emulator+CI as practical demo target; iOS written architecture with macOS runner. Nothing has been compiled or tested.

## Required order for new project planning

1. **SUT candidate evaluation and finalization:** compare **JetNews** and **Volksverpetzer `vvp_app`** with exact build/data seams; use **Now in Android** as reference, owned sample as fallback. See `docs/05_SUT_SELECTION.md`. Time-box spikes and choose by injection feasibility.
2. **Mock-data design:** assess fixture repository/test build vs mock API, prove how named scenario reaches **real** rendered UI, pin assets/time; see `docs/06_MOCKING_STRATEGY.md`.
3. **Toolchain/CI decision:** choose Appium+pytest vs native snapshot route after SUT/mock evidence, establish Android runnable slice, goldens, diff and practical CI; see `docs/02_DECISIONS.md` and `docs/07_ARCHITECTURE_CI.md`.

Do **not** start with open-ended option generation or assume SUT/toolchain are locked. Do not spend excessive time on multiple third-party repositories with deadline imminent.

## Current decisions / pending human approvals

| Decision | State |
|---|---|
| Lightweight Planning → Execution → Evaluation + handoff/logging | User-directed; framework in place |
| SUT | **OPEN** (JetNews vs Volksverpetzer; fallback owned sample) |
| Mock injection architecture and scenario control | **OPEN** |
| Demo platform / automation runner | **OPEN** (Appium preferred for evaluation, not approved) |
| Minimal verified screens/tests and CI scope | **OPEN** |
| Repo/publication destination | **OPEN**; no employer PDF in public repo |

## Evidence register

| Item | State | Source |
|---|---|---|
| Employer challenge PDF | PRESENT | `reference/QA_Manager_Challenge_Screenshot_Testing.pdf` |
| Requirements and planning docs | UPDATED | `docs/01_REQUIREMENTS.md`, `05_SUT_SELECTION.md`, `06_MOCKING_STRATEGY.md`, `07_ARCHITECTURE_CI.md` |
| SUT source/build/toolchain verified | **NOT DONE** | None |
| Mock reached real UI | **NOT DONE** | None |
| Working test, screenshots, comparison, diff | **NOT DONE** | `demo/` placeholder |
| CI green run | **NOT DONE** | None |
| Strategy | **NOT STARTED** | `deliverables/` placeholder |
| AI prompts disclosure | REGISTER UPDATED | `docs/04_AI_PROMPT_LOG.md` |

## Last completed work

Reviewed original PDF and latest planning discussion; reorganized decisions to **SUT → mocking → test runner → CI**, captured throughput/scalability motivation and shared-core/platform-adapter principles, updated phase/project prompts and generated consolidated context. This was **documentation only**, not a technical proof.

## Next agent actions

1. Apply `prompts/01_PLANNING.md`: compare SUTs and locate actual data seams; record command/evidence, ask only for machine facts that are indispensable.
2. Evaluate fixture injection/mock API with the candidate; show 2–3 options and request human approval of coupled SUT + mock + runner decision.
3. Once approved, move into a single Android vertical slice and prioritize running golden/diff evidence. Keep AI prompt log current.

End each session with exact changes, commands/results, blockers, next 1–3 actions and new human decisions. Do not invent CI screenshots or builds.


---

## Session addendum — 2026-11-01, read-only feasibility research

**Phase:** PLANNING. **Tier A approvals:** None. **Implementation:** Not started. **Source-of-truth updates prepared:** `02_DECISIONS.md`, `03_HANDOFF.md`, `04_AI_PROMPT_LOG.md`, `05_SUT_SELECTION.md`, `06_MOCKING_STRATEGY.md`, `07_ARCHITECTURE_CI.md` (this revised set must be manually substituted for existing Project Sources; creating these files in chat does not update Project Sources).

### Work completed / evidence

- Re-read original four-page employer PDF and 01_REQUIREMENTS, 02_DECISIONS, 03_HANDOFF, 05_SUT_SELECTION, 06_MOCKING_STRATEGY, 07_ARCHITECTURE_CI and 01_PLANNING.
- Online read-only repository review: JetNews README shows independent Gradle project and pre-existing static data/test commands; `FakePostsRepository.kt` confirms `PostsRepository` injection and 800 ms fake delay plus predictable every-fifth-request failure; `HomeScreens.kt` shows existing `PostCardTop`/`PostCardSimple` real rendering. No `testTag` text found in inspected home UI file. JetNews code license Apache-2.0, asset review remains open.
- Online `vvp_app` README confirms Expo/TypeScript, Node 24+, pnpm, development and APK build modes; GitHub indicates MIT code license. Exact article-fetch seam, selectors and independent asset rights not proven. Repository public page displayed `prerelease` branch when viewed, requiring commit pinning on checkout.
- Official Android/Appium documentation checked for Compose `testTagsAsResourceId` / `mapTestTagToResourceId` possibility.
- **No app cloned/built/started. No fixture injected. No golden/actual/diff/CI result.** Shell `git ls-remote https://github.com/android/compose-samples.git HEAD` was attempted in the assistant's isolated container and failed `Could not resolve host: github.com`; that is a limitation of the assistant sandbox, **not a result about the user's Windows environment**. Public source review used web browsing.

### Conditional architectural recommendation — awaiting human

1. **SUT:** JetNews, because real UI and existing fake data repository are source-confirmed. `vvp_app` stays conditional challenger. Owned minimal app remains deadline fallback.
2. **Mock:** test-only fixed PostsRepository/PostsFeed and scenario selector; strip delay/every-fifth failure for screenshot mode; pin all assets/environment; do not assume premium/breaking UI exists.
3. **Runner:** Appium + Python/pytest only if host emulator and launch control/IDs are quick to verify; otherwise native Compose screenshot tests (Roborazzi/Paparazzi, choose one) for fastest reliable proof. Broader production hybrid strategy; separate iOS written path.

### Next three actions

1. Obtain approval **only for bounded local feasibility spike** as specified in revised `05_SUT_SELECTION.md`; check host prerequisites and JetNews source/build/real screen. Stop on blockers instead of spending the remaining deadline on infrastructure.
2. Present one combined SUT + mock + runner + CI-minimum approval gate using actual results, with the owned app fallback available.
3. If approved, begin EXECUTION: real fixture → existing UI → PNG → committed golden → verify/diff; README/strategy/prompts, then evaluate. Reserve interview rehearsal time.

**Do not ask for already settled strategy preferences.** Machine prerequisite state and installed tools are not known. The next agent must not infer a working SUT/CI from these research findings.

---

## Latest work session — 2026-11-01: `vvp_app`-first feasibility spike

**Phase:** PLANNING. **Human authorized:** bounded SUT/mock feasibility spike with `vvp_app` priority, **not** implementation or a runner choice.

### Completed in this session

1. Reconfirmed prior authoritative employer PDF/docs and the human's explicit `vvp_app` prioritization. Re-examined public `https://github.com/Volksverpetzer/vvp_app` README and repository root: Expo/TypeScript, Node 24+, pnpm, `pnpm install` / `pnpm start` / `pnpm android`, `.env` requirement, `APP` variants, EAS development/local build profiles. The root lists `.env.sample` whereas README points to `.env.example`; inspect the actual tracked file before using either.
2. Public F-Droid listing for the distributed Android app describes a network dependency on `volksverpetzer-app.de` without user-configurable service selection; source-level app base URL, authentication, caching and possible DI/provider seam **still unverified**. This increases the risk of assuming that a mock HTTP server can be used without adapting code. GitHub says MIT for code; logos/photos/editorial content and dependencies need separate review. A real published Android app exists, but this is **not** proof that our checkout builds on Windows.
3. Official Maestro docs confirm that React Native `testID` supports stable selectors and that Maestro supplies screenshot capture and `assertScreenshot`; Appium+pytest remains another open candidate. Existing `vvp_app` `testID`s have **not** been inspected.
4. Attempted `git ls-remote https://github.com/Volksverpetzer/vvp_app.git HEAD` in assistant's sandbox: `Could not resolve host: github.com`. Public web GitHub root accessible; direct `/tree/prerelease/src` and source-file URLs returned cache misses. **No source clone, app build, emulator launch, fixture UI proof, PNG, golden/diff, or CI job in this session.** Sandbox network failure is not evidence about the user's Windows PC.
5. Prepared complete replacement versions of six source-of-truth docs, including 04_AI_PROMPT_LOG. These are downloadable artifacts; **Project Sources are not silently modified**.

### Current evidence status and blockers

| Gate | Evidence | State |
|---|---|---|
| vvp code access, version | Public root/README read; exact checkout SHA not obtained | PARTIAL |
| Real feed card → data boundary | Not retrieved from GitHub; must trace after Windows checkout or uploaded source archive | BLOCKED / OPEN |
| Windows Android toolchain | Versions, emulator, Java/SDK/Node/pnpm unknown | OPEN |
| `vvp_app` Android native build/render | Not run | NOT VERIFIED |
| Fixture provider or mock HTTP | No injection; no scenario selector | OPEN |
| Stable target `testID` / readiness | RN capability documented, app-specific values unknown | OPEN |
| Golden/actual/diff and green CI | None | NOT DONE |

### Next actions, no repeated approval

1. Run the **vvp-first, 90-minute cap** Windows readiness/source tracing steps in `05_SUT_SELECTION.md`. Pin `git rev-parse HEAD`; inspect `src/` for exact screen/hook/query/API client; confirm source-independent fixture injection feasibility, JS assets and existing `testID`; attempt Android launch only if prerequisites available. Ask the human for the command output or zipped public-source checkout when necessary; do **not** claim assistant has accessed their PC.
2. Use results to decide whether to keep `vvp_app`, switch to JetNews (existing repository seam already identified) or owned minimal app before spending the deadline. Reconcile mock approach with target SUT; consider Appium/pytest vs Maestro **only after mock feasibility**.
3. Request once the combined SUT/mock/runner/CI scope approval before EXECUTION. Then narrow to one real fixture → UI → PNG → golden → diff, plus strategy, README and AI prompt record. Reserve time for interview rehearsal.

**Completion claim:** Public research and documents updated only; no native screenshot demo or passing CI demonstrated.


---

## Latest checkpoint — 2026-11-01: actual Windows host evidence (user supplied)

**Phase:** PLANNING. **Human authorization:** `vvp_app`-FIRST bounded feasibility; no implementation or Appium/Maestro approval.

### Verified from PowerShell output (candidate's PC)

| Probe | Exact result | Interpretation |
|---|---|---|
| `git clone --branch prerelease --single-branch https://github.com/Volksverpetzer/vvp_app.git` | Successful checkout | Source now available on host |
| `git rev-parse HEAD` | `8b421753a17a18cd648447319adcca61a288f97f` | Record this commit when tracing/archiving |
| `node --version` | `v22.12.0` | Below README Node `24.x+` requirement; do not yet attempt unsupported install/build as proof |
| `pnpm --version` | Initially not found; after `npm install -g pnpm`, `12.11.2` | pnpm exists, but project `packageManager` and lockfile fit not checked |
| `adb devices -l` | Empty | ADB command available, no online device |
| `emulator.exe -list-avds` | `Pixel_10` | AVD configured, **not** proven to boot |

### Unverified and not claimed

- Actual `src/` article data call chain, fixture-provider seam, endpoint override, selectors, `.env` requirements, package-manager pin, JDK/SDK readiness, emulator boot, app build/install/run, offline isolation, actual native screenshot, golden, visual diff, CI and iOS.
- No app code changes were requested/authorized; do not characterize the clone or global pnpm install as app implementation.

### Immediate next steps (no fresh approval needed)

1. Source-only inspection at exact SHA: `.nvmrc`, `package.json` `engines`/`packageManager` and scripts, `pnpm-lock.yaml` header, `.env*` filenames (not contents), tracked source-level feed → model/hook/query/client flow and `testID`/readiness. Prefer `git archive --format=zip --output ..\vvp_app_prerelease_8b42175_source.zip HEAD` + upload for precise inspection without exposing `.git`, untracked `.env` or installed deps.
2. Inventory host prerequisites (`java -version`, `adb version`, Android SDK/JDK vars). Bring runtime to the declared Node 24 release and use project-pinned pnpm version if necessary. Then boot existing Pixel_10 and validate `adb devices -l`; only attempt package install/build when suitable. Stop quickly on hard blockers.
3. After one verified source chain and build feasibility, present one combined human approval choice SUT + mock + runner + minimum CI; keep JetNews/owned fallback and time-box.

**AI disclosure:** planning/checkpoint recorded in revised `04_AI_PROMPT_LOG.md`; documents are downloadable replacement artifacts and must be manually substituted in ChatGPT Project Sources.


---

## Latest checkpoint — 2026-11-01: uploaded pinned `vvp_app` archive inspected

**Phase:** PLANNING; **approved:** bounded `vvp_app`-first feasibility **only**; **not approved:** final SUT, mock implementation, Appium/Maestro, CI rollout. Source archive inspected at SHA `8b421753a17a18cd648447319adcca61a288f97f` (user's archived HEAD). No source in working checkout was edited by the assistant.

### Candidate's actual Windows evidence

- `git status --short` empty. `.nvmrc` contains `24`. `package.json` specifies `engines.node=24.x`, `packageManager=pnpm@12.11.2`; lockfile header pins pnpm 12.11.2. Host Node `22.12.0` **does not meet project engine**; installed pnpm `12.11.2` **does match**.
- `Get-ChildItem -Name .env*`: only `.env.sample`; `git ls-files .env`: no output. README mentions `.env.example` but actual tracked template is `.env.sample`. Avoid exposing or committing local `.env`.
- Host JDK Java `11.0.24`, `JAVA_HOME=C:\Program Files\Java\jdk-11`; `ANDROID_HOME=C:\Users\abrar\AppData\Local\Android\Sdk`. Installed RN `0.86.3` targets JDK 17 (official React Native docs). Pixel_10 AVD exists but hasn't booted; `adb devices -l` has no connected devices.

### Archived source: concrete real-UI call chain

`config/volksverpetzer.config.ts` enables primary+secondary WordPress and social feeds → `src/app/(tabs)/home.tsx` chooses `FeedFetcher[feed]` based on `contentSettings` → `src/screens/Home/fetchers/FeedFetcher.ts` creates WordPress-specific fetchers via `WordPressFetcher.createFetchers(WordPressAPI.create(entry.handle))` → `src/helpers/network/WordPressAPI.ts` GET `/wp-json/wp/v2/posts` using a site-specific URL → `src/screens/Home/fetchers/WordPressFetcher.ts` maps response to `Post` containing `ArticlePost` → `src/screens/Home/components/Feed.tsx` calls `FetcherUtilities.fetchAndProcessPosts` and renders `GenericPost` → `src/components/posts/GenericPost.tsx` renders the **existing real** `ArticlePost` card (`src/components/posts/ArticlePost.tsx`). Tests already cover component/fetcher but Jest tests mock the rendered image, so they are not native screenshot proof.

**Critical nuance:** `src/helpers/apiUrl.ts` FOSS-only HTTPS URL override controls auxiliary `ServerAPI`, not these separate WordPress feed clients. For screenshot feed, a **test-only injected fetcher/provider** is the leading design, not an assumed existing WireMock URL override. `ArticlePost` separately fetches featured-media metadata, may animate placeholder GIF and display view/reading counters; announcements, onboarding and multiple feeds also require deterministic disabling/reset in test mode. Existing `testID="article-progress-bar"` is present, but no unique ready/card test ID established. Code MIT; image/text/brand rights not proven.

### Verified / proposed / missing

- **Verified:** pinned tracked source readable, complete article-feed code trace, injection point feasible at interface level, package/runtime constraints, MIT code license, host SDK/AVD paths; only source-level feasibility, **not** implementation.
- **Proposed:** SUT `vvp_app`, test-only fixture feed adapter (synthetic long-headline scenario), real `ArticlePost` unchanged, stable test ID/ready marker, controlled media and side effects; alternative WordPress mock HTTP with new test-only client URL seam. Appium/pytest versus Maestro remains OPEN.
- **Missing:** Node 24 and JDK 17 environment, emulator boot, `pnpm install --frozen-lockfile`, `pnpm android` native build, fixture selection and rendering, screenshot PNG/golden/visual diff, CI green run and native iOS evidence.

### Next three actions, within the already-authorized PLANNING spike

1. On candidate Windows host switch Node to 24.x and use JDK 17 (verify `node -v`, `java -version`, `JAVA_HOME`; check prerequisites without assuming installed versions). Boot `Pixel_10`; verify `adb devices -l` and Android boot status.
2. Once versions corrected, use tracked `.env.sample` privately as `.env` if required, `pnpm install --frozen-lockfile`, then `pnpm android` on connected emulator. Save first failure or native on-screen success and versions. **These are feasibility checks, not app implementation.** Stop quickly if dependencies/native build present a major blocker.
3. With runtime evidence, present **one coupled human approval**: `vvp_app` + in-app fixture provider + Appium/pytest or Maestro + narrow CI scope; otherwise JetNews/owned fallback. Only then transition to EXECUTION and create the real fixture → native UI → actual/golden/diff slice. Update AI prompt log and interview documentation. Do not claim screenshot or green CI before actual proof.

**Document update delivery:** complete revised Markdown files are downloadable copies and must manually replace the matching ChatGPT Project Sources files; these aren't automatically synchronized.

---

## Latest work-session handoff — 2026-11-01: bounded QA fixture patch ready, Windows runtime verification pending

**Phase:** PLANNING / authorized bounded `vvp_app` mock feasibility spike. User has **not approved** final SUT, data injection architecture, Appium/Maestro runner, demo implementation scope or CI.

### New evidence from user (after previous source-archive handoff)

- Native `pnpm android` build/install succeeded per user's report. Pixel_10 Android API 37 emulator initially had unresponsive package-manager queries; emulator's saved state was cleared via genuine cold boot after killing an orphan emulator process.
- ADB health: `emulator-5554 device`, `adb shell getprop sys.boot_completed` → `1`, `adb shell pm path android` → `package:/system/framework/framework-res.apk`.
- `pnpm start --clear` launches Metro on port 8081. User confirmed the real Volksverpetzer home feed shows actual article cards/headlines on the emulator. **This is verified only through user observation, not by assistant-run app/screenshot.**
- Live feed caused HTTP 502 for `/proxy/instaFeed?account=pruefpunkt`, surfaced as an in-app dev toast. This is a visible nondeterminism risk, not a home WordPress UI blocker.
- User reviewed and approved proceeding with the specific narrow fixture-injection feasibility approach. No runner/SUT architecture gate approval.

### Assistant-prepared artifact — apply locally

- `vvp_qa_fixture.patch` (binary `git apply` patch) against `8b421753a17a18cd648447319adcca61a288f97f`; `README_APPLY_AND_VERIFY.md` provides exact PowerShell command sequence.
- Added `src/screens/Home/fixtures/qaScenario.ts` and `qaFeed.ts`, a generated 1200×615 local PNG, and conditional changes to home, the real article card and notification-related startup effects. Only `__DEV__` + `EXPO_PUBLIC_QA_SCENARIO=long_headline` activates the fixture.
- Uses `WordPressFetcher.mapArticleToPost` → `Feed` → `GenericPost` → `ArticlePost` (real React Native view), fixed synthetic text/date/author; no WordPress/Instagram home feed calls. Existing production behavior is unchanged when scenario is disabled by construction, **but not runtime-verified**. Limited root notification/changelog effects suppressed. Other app-wide network calls not fully audited.
- Test readiness `testID` is conditionally emitted after bundled image `onLoad`; driver visibility remains unverified.
- **Assistant-side checks passed:** patch `git apply --check` and apply on freshly extracted source archive; PNG hash matched; TS/TSX syntax/transpilation for all six modified/new TS files. **No package dependencies/native build available in assistant sandbox**; no full type-check, fixture screenshot, repeated capture, golden, diff, CI or iOS claim.

### Commands to run on candidate's Windows machine

```powershell
cd D:\Projects\axel-springer-assignment\vvp_app
# Ensure source HEAD is still the pinned commit, preserve any user modifications.
git rev-parse HEAD
git status --short
$patch = "$HOME\Downloads\vvp_qa_fixture.patch"   # Actual downloaded path
# Stop Metro first, keep Android emulator running.
git apply --check "$patch"
git apply "$patch"
pnpm check:ts
$env:EXPO_PUBLIC_QA_SCENARIO = 'long_headline'
pnpm start --clear
# Press a in Metro to open Android.
```

**Success signal:** user-shared emulator screenshot of real article card with `QA-FIXTUR...` headline + static `QA FIXTURE IMAGE` + date/author. Check for any 502 toast, Metro errors and `pnpm check:ts`. If failed, focus only on first failure before switching SUT or runner.

**Disable mode:** stop Metro → `Remove-Item Env:EXPO_PUBLIC_QA_SCENARIO -ErrorAction SilentlyContinue` → `pnpm start --clear`.

### Next gate

1. Collect actual patch apply / full TypeScript check / Metro / fixture-on-emulator results.
2. If successful, verify text A/B change and no social feed toast; decide whether a small screenshot runner is feasible and obtain one combined human approval for SUT/mock/runner/demo scope.
3. Then produce actual capture, golden and compare/diff + README and short strategy. No silent baseline regeneration. Keep interview deadline 2026-11-03 14:00 CET in focus.

**AI disclosure:** `04_AI_PROMPT_LOG.md` extended; replacement copy must be manually swapped into Project Sources. The generated patch is **not applied** to the user's Windows working checkout by assistant action.

---

## CURRENT handoff — 2026-11-01: PLANNING APPROVED → EXECUTION, runner package prepared

**Phase:** EXECUTION authorized; next fixed event 2026-11-03 14:00 CET. **Human approval:** Volksverpetzer + test-only fixture fetcher + Appium/Python pytest + exactly one Android `long_headline` screenshot regression scenario; Maestro only as time-boxed backup. This explicit approval supersedes earlier handoff sections marking choices open.

### Evidence from candidate's Windows PC

- Correct upstream Git SHA `8b421753a17a18cd648447319adcca61a288f97f` confirmed; `git safe.directory` exception resolved Windows repository ownership warning.
- `git apply --check` and `git apply` succeeded for the prepared `vvp_qa_fixture.patch`. Working-tree modified `src/app/(tabs)/home.tsx`, `src/app/_layout.tsx`, `src/components/posts/ArticlePost.tsx`, `src/hooks/useNotificationObserver.ts`; new `assets/images/qa/` and `src/screens/Home/fixtures/`.
- `pnpm check:ts` (tsc --noEmit) completed with exit success (no errors in PowerShell transcript).
- Emulator screenshot supplied by user shows the real Volksverpetzer header/search/navigation plus actual `ArticlePost` with synthetic `QA-FIXTUR:` multiline title, bundled `QA FIXTURE IMAGE`, fixed author/date/body. No error toast visible in supplied image. This proves fixture-to-UI for the one screen, not complete network isolation or repeatability.

### New assistant-created execution package (this session)

- `qa_visual/visualqa/android.py`: Appium UiAutomator2 driver + `qa-article-card-ready` and `qa-article-title` native selectors; explicit wait after local image load; diagnostics on failure. The existing installed development app + Metro fixture mode are required.
- `qa_visual/tests/test_long_headline.py`: actual native card PNG save, one Android baseline comparison, actual/diff/metrics artifacts; **intentional first-run failure if no approved golden**; never auto-accepts baseline.
- `qa_visual/visualqa/image_diff.py`: portable RGB comparator (RGB channel tolerance 12; maximum 0.2% changed pixels by default); reject size mismatches; red overlay diff PNG; machine-readable JSON.
- `qa_visual/tests/test_image_diff_unit.py`: four local unit checks, passed in assistant sandbox with Python 3.13 / pytest 9.0.2 / Pillow 12.3.0. These are comparator-only; user's pinned requirements are Appium-Python-Client 5.2.4, pytest 8.4.2, Pillow 11.3.0 (versions from PyPI); full installed dependencies not verified here.
- `qa_visual/README.md`: Windows commands, Appium bootstrap, `pytest -m unit/visual`, two-shot stability check, **manual** golden approval/commit, actual-code mutation causing intentional failing diff, diagnostics and iOS/CI boundary.
- Assistant-side Python `compileall` and unit tests can validate source only; **no** Appium server/emulator Windows access, device capture, golden, real failing diff, green CI or iOS execution is claimed.

### Next three actions

1. Extract `qa_visual/` directly into `D:\Projects\axel-springer-assignment\vvp_app`; on candidate Windows machine verify `py -3 --version` and Appium installation/UiAutomator2 doctor while keeping Metro fixture enabled and emulator ready.
2. Run `python -m pytest -m visual -v -s` per packaged README. Diagnose *first failure only*. Capture real `long_headline.actual.png`; repeat capture, inspect and manually accept approved `baselines/android/pixel10-api37/long_headline.png`; rerun passing test; make a deliberate fixture text change and observe failed diff.
3. Commit fixture source, automation, reviewed golden and README when verified; write 1–3-page Android/iOS strategy and cleaned AI prompt record. Add a CI workflow only if it can be verified/time-boxed; do not claim pipeline success from YAML alone.

**Blockers:** Python and Appium availability on user's host unknown; React Native `testID` visibility through UiAutomator2 unverified; Appium screenshot/card crop stability unverified; Android API 37 preview emulator previously had Package Manager hang after quick boot (cold boot fixed). If Appium remains blocked, document evidence and revisit already-approved Maestro fallback, not an unannounced runner pivot.

**Source-of-truth management:** This is a complete replacement Markdown file prepared in the assistant environment. Candidate must replace the existing `03_HANDOFF.md` Project Source manually; no files were modified on candidate's Windows PC by the assistant.

---

## 2026-11-01 — Repository foundation handoff (no migration executed yet)

**User request:** Rename outer folder `axel-springer-assignment` to neutral `visual_regression_qa_strategy`; rename nested `vvp_app` to sibling `app/`; keep Appium/pytest in `qa_visual/`; add token-efficient shared `AGENTS.md` plus a tiny `CLAUDE.md` import; preserve previously applied fixture patch locally; relocate old starter documentation safely; establish one Git root and GitHub remote. User clarified portfolio reuse and public neutrality; do not record that clarification as a prompt-used entry.

**Foundation proposal delivered:** One root Git repo containing `app/`, `qa_visual/`, `docs/`, `reference/patches/`, public README/agent guidance; ignored `.project-private/` for original employer PDF, the full source-of-truth documents and phase prompts. The prior `vvp_qa_fixture.patch` stays historical and must not be reapplied. App upstream Git metadata should be moved to an out-of-tree backup before root `git init`. GitHub private-first until third-party asset rights and public-doc review.

**Validated prior to migration:** the user reported successful original fixture patch application, `pnpm check:ts` exit 0, and real Android Pixel 10 fixture rendering. The prepared `qa_visual` comparator unit tests passed only in the assistant sandbox, **not** Appium on the user's Windows host.

**Not executed:** Windows folder renames; nested Git backup; root Git init/commit/push; new app paths in runner docs; post-move typecheck/native render; new appium run, golden, diff, CI. Do not claim success until the user or coding agent provides commands and output.

**Next actions:** run read-only parent Git preflight and status; back up; rename folders; preserve original Git metadata externally; copy local private docs/patch and agent guidance; update runner paths if copied; verify Android fixture again; inspect staged paths, create initial Git commit, private GitHub remote/push, and only then begin screenshot runner implementation. Retain final changes and evidence in this handoff.

## 2026-11-02 — EXEC-010 README checkpoint

Updated `qa_visual/README.md` against the implemented fixture gate, POM, driver, comparator, requirements, current baseline and artifact paths. Documented observed Python/Appium/UiAutomator2/emulator versions; corrected PowerShell setup and test commands; separated verified environment/test facts from clean-machine setup and regeneration procedures that were not re-run. Added a human-reviewed, backed-up, hash-checked manual golden promotion sequence. No Appium test or baseline operation was run for this documentation task. Updated the sanitized public AI prompt log and task history. Git status remains unverified.

## 2026-11-02 — EXEC-012 strategy checkpoint

Created `deliverables/strategy.md` (approximately 1,100 words, seven requested sections). Original brief confirms 1–3 pages; Markdown pagination is not rendered or claimed. Strategy grounds the proposed shared contracts/native component/Appium layers in EXEC-006–009 Android evidence, explicitly separates iOS and CI proposals, and discloses the single-scenario gap. Private source material is not linked or reproduced. Updated task history and sanitized public prompt disclosure. Root README still needs its pending-strategy status reconciled in a separately authorized task; it was outside this task's edit scope. No implementation, runtime, golden or Git changes.

## EXEC-013 checkpoint - 2026-11-02

Finalized the existing seven-section strategy with the approved human-controlled golden/CI policy, joint development/QA ownership of fixture contracts, and precise one-scenario Android evidence scope. Rendered `deliverables/strategy.md` to a two-page A4 `deliverables/strategy.pdf` using a temporary isolated ReportLab environment; opened metadata and page count with pypdfium2, rendered both pages and inspected them. Text and table are readable, with no clipping or overflow. The original challenge brief and detailed instructions specify 1-3 pages; “13 pages” was interpreted as malformed range wording. No app, runner, baseline, emulator, CI, or root README changes. Next: human review, then separately authorize any root README link/status update.

## EXEC-014 checkpoint - 2026-11-02

Updated the root README to link to the strategy PDF and editable Markdown. Generated and inspected a corrected two-page A4 candidate with clean final-section reference labels. All seven sections and the verified Android evidence are present; visual inspection found no clipping or overflow. The original `deliverables/strategy.pdf` is locked by another process; safe replacement attempts were denied, so it remains unchanged and `strategy.exec014.pdf` is retained as the verified candidate. Source brief and repository requirement call for 1-3 pages. No application, runner, baseline or CI changes. Next: release the PDF lock, promote the candidate and verify the official path.

## EXEC-014 completion - 2026-11-02

The user released the PDF lock; promoted the corrected candidate to `deliverables/strategy.pdf`. Final PDF is A4, two pages; both pages rendered and inspected. Text extraction confirms all seven sections, Android evidence and clean link labels without raw Markdown. Root README links to the PDF and editable Markdown; both paths exist. Original brief specifies 1-3 pages. No implementation, baseline or Git changes. Await human review; no Git packaging authorized.

## EXEC-016 — Local packaging checkpoint (2026-11-02)
- Initialized the root Git repository on `main` and created local commit `cb334e91a9225334f9e53db71ed414007c8df78f` from 500 explicitly staged, audited files.
- Added root ignore protection and current approved-baseline documentation. Golden SHA-256 verified as `E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629`.
- No private/generated paths or credential-pattern findings in the staged set. No remote or push; app asset redistribution clearance remains unverified.

## EXEC-017 — Post-commit verification checkpoint (2026-11-02)
- Verified HEAD `cb334e91a9225334f9e53db71ed414007c8df78f`, branch `main`, no remote, 500 committed files, and the approved golden SHA-256 from the committed Git blob. Strategy PDF remains the reviewed two-page document; documentation links and tracked deliverables resolve.
- Unit suite: 7 passed, 1 deselected (visual), exit 0. Android preflight is unavailable: ADB found no device; Appium and Metro endpoints refused connections. The single visual test was not started. No application, docs, test, baseline or history changes; local task records appended only.

## EXEC-017R — Android demo runtime restored (2026-11-02)
- Started existing Pixel_10 via process-local `ANDROID_AVD_HOME` because shell `HOME` was empty; the AVD cold-booted after rejecting an incompatible saved renderer snapshot. No wipe/reset was performed. Emulator is online/booted with the app installed.
- Fixture-enabled Metro and Appium 3.3.0/UiAutomator2 7.1.2 are running. The single visual pytest execution passed; fixture title assertion passed and comparison was 0/1,271,636 changed pixels at the existing tolerance. Golden SHA-256 remains `E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629`.
- Runtime remains up for the PyCharm walkthrough. HEAD unchanged; no remote or tracked modifications. Only ignored screenshot/metrics artifacts and local task records were updated.

## EXEC-016B — Submission metadata cleanup (2026-11-02)
- Committed six reviewed app/QA format-ignore configs, README corrections for committed baseline tracking and `.env.sample`, and narrow agent-file ignore rules.
- Follow-up commit: `ae07a0a7cbfae8be329d2e1a63d32ede575f32c9` (parent `cb334e91a9225334f9e53db71ed414007c8df78f`). Exact 10-file audit passed; no secret/generated paths, code, tests or golden changes. No hook, remote or push.
- Golden SHA-256 remains approved value. No tracked worktree changes.

## 2026-11-06 - Profile architecture explanation
- Inspected test_long_headline.py, Android driver, screen/component objects and image comparator. Verified that VVP_GOLDEN_PROFILE selects baseline/artifact directories only; driver configuration is independent. Explained validation and capture/comparison flow. No runtime tests or implementation changes.


## EXEC-020 - Runtime scenario foundation - 2026-11-07T12:45:56+01:00
Status: BLOCKED (independent implementation and unit checks complete; native evidence unavailable).
Initial/final Git: main, ae07a0a7cbfae8be329d2e1a63d32ede575f32c9, no remotes/staged changes. Preserved pre-existing docs/ai_prompts_used.md modification and all unrelated untracked paths. No commit/push/install.
Changed app: src/screens/Home/fixtures/qaScenario.ts (typed registry, validation/precedence, one-time frozen selection and legacy live flag); new QaLaunchGate.tsx (await initial URL before subtree mount, unavailable states, nonvisual exact identity); src/app/_layout.tsx (dev-only gate, release original root); src/app/+native-intent.tsx (guarded QA dev-client wrapper navigation only). Added scenario/gate tests and extended existing native-intent tests.
Changed runner: new visualqa/scenario_launch.py, optional VVP_QA_LAUNCH_URL in visualqa/android.py, exact identity wait before card readiness in both launch/legacy paths, cold-mode termination in existing test cleanup; new focused Python unit tests. qa_visual/README.md documents candidate commands and unverified status. No new scenario tests, UI, goldens or comparator changes.
Ordering: Router can parse URL independently; only after RN Linking.getInitialURL resolves and selection is frozen can RootLayout hooks/providers/Feed mount. Invalid/unsupported selection mounts no application subtree. Selected marker qa-scenario:long_headline is outside card; native accessibility exposure remains unverified. No URL listener, storage selection or mounted-feed switching.
Source evidence: installed Expo dev-launcher handles expo-development-client wrapper by retaining pending intent data before app launch; plain external app schemes can route to chooser from launcher mode. Guarded native-intent mapping takes explicit wrapper to /home; runtime must prove actual installed behavior.
Candidate launch (NOT executed): from qa_visual set VVP_QA_LAUNCH_URL to exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=long_headline, with adb reverse tcp:8081 tcp:8081 and existing Metro/Appium ready, then .\.venv\Scripts\python.exe -m pytest .\tests\test_long_headline.py -m visual -v -s. Driver terminates, deep-links, reads identity, then existing readiness/capture/comparison; cleanup terminates. Clear VVP_QA_LAUNCH_URL for compatibility activation. Change only outer qa_scenario for negative inspection. Do not change Metro environment between runs. No pm clear/wipe.
Commands/results:
- adb devices -l: exit 0, no devices. No listeners found on 8081/4723. Invoke-RestMethod http://127.0.0.1:4723/status and Invoke-WebRequest http://127.0.0.1:8081/status: each exit 1, Unable to connect to the remote server. Services not started.
- pnpm.cmd check:ts: exit 0, including final routing/tests.
- Initial pnpm invocation failed due sandbox access to pnpm store lock; approved tool escalation ran installed checks successfully, no installation.
- pnpm.cmd test --runInBand --coverage=false: exit 0, 180 suites passed, 1434 tests passed / 3 skipped, 1 snapshot passed, 93.798s. This broad run preceded the final wrapper-route correction. Console warnings/errors occurred in existing error-path and act tests; no suite failures.
- Final targeted pnpm.cmd test --runInBand --runTestsByPath __tests__/screens/Home/qaScenario.test.ts __tests__/screens/Home/QaLaunchGate.test.tsx __tests__/app/native-intent.test.ts --coverage=false: exit 0, 3 suites / 36 tests passed. Includes gate-before-child-effects, legacy fallback, validation, unsupported IDs, precedence, none, frozen selection, simulated fresh-JS isolation and release routing/gating. These are not device lifecycle or production-build execution.
- pnpm.cmd check: exit 1; cspell reports only pre-existing src/screens/Home/fixtures/qaFeed.ts:16:11 Unknown word (FIXTUR). Untouched fixture matches HEAD; combined command stopped before tsc, so tsc ran separately and passed. Spelling policy unchanged.
- Python pytest -m unit -q: final exit 0, 12 passed / 1 deselected. --collect-only -q: exit 0, 13 collected. No visual test executed.
- git diff --check: exit 0 (line-ending conversion warnings only). Existing fixture data, ArticlePost rendering, ArticleCard boundary implementation, comparator and baselines have no diff.
Golden SHA256 remains E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629. No new dimensions/comparison/repeat-capture evidence. Historical saved result is 1028x1237, 0/1271636 changed; not an EXEC-020 result.
Isolation: fresh process resets feed/pagination/scroll/in-flight work. Persistent theme/settings/badges/onboarding survive; no new persistence writes or data wipes. Existing SettingsProvider/BadgeProvider can write as before. Announcement/notification/article-effect suppressions reused for supported QA mode. No dark override, image-less/empty rendering or app-wide network guarantee. Release default bypass and ignored inputs tested at source/unit level only; release build not run.
Remaining: native wrapper delivery, navigation order, marker visibility, explicit-none/unknown/unsupported consecutive launches, fallback regression, two unchanged-golden captures, and constant-Metro-environment proof. CI portability: requires installed dev artifact, reachable Metro, appropriate adb reverse/device addressing and one device/port namespace per job; not standalone QA build evidence.
Next bounded EXEC-021: restore existing local runtime with authorization; verify this foundation's supported and negative cold launches, exact marker and two golden comparisons while Metro environment stays fixed. Stop on launcher/ordering failure; no four new scenario implementations or baseline promotions. Rollback only these task-specific changes while preserving unrelated work; restore legacy Metro selection. No blanket reset/clean.


## EXEC-021 - Native scenario-launch verification - 2026-11-07T13:18:45+01:00
Status: FAIL. Native launch/selection checks pass after a localized identity placement correction; both required visual comparisons fail against the unchanged approved golden. EXEC-020 acceptance remains open; do not start four new UI scenarios.
Initial/final repository: main, HEAD ae07a0a7cbfae8be329d2e1a63d32ede575f32c9. Initial tracked modifications: app/__tests__/app/native-intent.test.ts, app/src/app/+native-intent.tsx, app/src/app/_layout.tsx, app/src/screens/Home/fixtures/qaScenario.ts, docs/ai_prompts_used.md, qa_visual/README.md, qa_visual/tests/test_long_headline.py, qa_visual/visualqa/android.py. Initial untracked EXEC-020 gate/tests/helper and unrelated upstream configuration directories preserved. No staging/commit/remote/push.
Runtime preflight:
- adb devices -l: emulator-5554 device; getprop sys.boot_completed=1; API=37; ro.boot.qemu.avd_name=Pixel_10. MemTotal=4008496 kB, MemAvailable=1851164 kB at preflight. Installed app pm path succeeds; package versionName=2.5.5/versionCode=1/targetSdk=36. wm size=1080x2424, density=420, font_scale=1.0. Existing reverse mapping host-15 tcp:8081 tcp:8081 retained; no recreation/wipe/reinstall.
- IPv4 Python urllib GET http://127.0.0.1:8081/status: HTTP 200, packager-status:running. Android manifest request to same server: SDK57.0.0, projectRoot D:\Projects\visual_regression_qa_strategy\app, hostUri127.0.0.1:8081, Android/Hermes launch bundle. Actual development bundle has EXPO_PUBLIC_QA_SCENARIO with long_headline; later native fallback launch confirms active environment fixture. Metro PID26880 remains listening127.0.0.1:8081 before/after checks; Metro not restarted, scenario env not changed. Successful native rendering proves compatibility for exercised modules, not a complete native-dependency audit.
- Appium initially refused IPv4 connection. appium.cmd driver list --installed exit0: UiAutomator2 7.1.2. Started existing Appium with cmd.exe /c appium.cmd --address 127.0.0.1 --port 4723 via hidden Start-Process, logs debug-logs/exec021/appium.stdout.log and stderr.log. Server3.3.0 logs successful driver load; /status ready=true. Services left running.
- Some PowerShell process/socket inspection was denied in sandbox; native netstat and HTTP/ADB provided required evidence. Initial PowerShell HTTP Content was a byte array; decoded urllib response confirmed actual status. No escalation-based service reconfiguration occurred.
Localized defect and correction:
- First supported native inspection (exit1) rendered expected QA card but exact identity timed out; preserved before-marker-fix JSON/XML. Native hierarchy omitted marker at top0. Unknown-selection launch actually displayed qa-scenario-invalid and text 'QA scenario unavailable: unknown', proving URL delivery despite a separate temporary-probe ID lookup timeout.
- Only product-source correction in EXEC-021: app/src/screens/Home/fixtures/QaLaunchGate.tsx moves transparent1px marker from top0 to top64dp and adds zIndex1. No layout/fixture/card/comparator change. Native accessibility now exposes qa-scenario:long_headline at [0,168][3,171], outside card. Exact cause of top-edge omission is inferred system-bar/occlusion behavior, not independently traced.
- Temporary ignored inspection script now uses raw UiSelector resourceId lookup, matching the existing POM fallback; Appium auto-completed ID lookup had caused the initial unknown-probe timeout. No runner selector change was necessary. Before/after diagnostic evidence retained.
Launch contract and native evidence:
URL exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=long_headline. Commands: .\qa_visual\.venv\Scripts\python.exe debug-logs/exec021/inspect_launch.py <selection> from root for hierarchy-only inspection; driver.terminate_app then mobile:deepLink with url/package/waitForLaunch:true; cleanup terminates and quits. Android dumpsys activity showed outer qa_scenario=unknown preserved in MainActivity VIEW intent.
Postfix long_headline inspection exit0: exact identity verified before readiness; one ready marker and expected QA-FIXTUR title. Inner rect x26 y720 w1028 h1132; outer rect x26 y720 w1028 h1237 ([26,720][1054,1957]); complete lower padding/corners retained. Root gate source/unit tests prevent providers/feed mounting until initial selection; unavailable native hierarchy and explicit-none behavior provide runtime corroboration. No per-request instrumented startup trace or app-wide no-network guarantee claimed.
Negative/consecutive launches (same Metro environment):
- unknown exit0 after diagnostic lookup correction: rejected screen, identity0, ready0, fixture titles0; PID7348, final pid absent.
- empty_feed exit0: unsupported screen, identity0, ready0, fixture titles0; PID7647, final pid absent.
- none exit0: normal home mounted (Suche ...), identity0, ready0, fixture titles0; PID7968, final pid absent. No storage clearing.
- Subsequent supported visual run2 restored exact identity/readiness and fixture screenshot.
- Additional fallback hierarchy-only launch with wrapper URL without qa_scenario exit0: identity1, ready1, exact synthetic title, same card rectangles; PID8661, final pid absent. This confirms environment fallback remained enabled while none disabled it. No screenshot in inspection sessions.
App process termination destroys the JS runtime/in-memory feed/pagination/scroll/asynchronous work. Independent launches used fresh PIDs; no selection/feed carryover observed for these supported/nonready states. Persistent theme/settings/onboarding/badges survive; no global wipe or new storage writes added. Future theme/media/empty-feed implementations still need their own isolation checks. Warm/live scenario switching remains unsupported. Release gate has unit/source evidence only, no release build executed.
Visual executions (exactly two):
From qa_visual, set child-shell VVP_QA_LAUNCH_URL to URL above, then .\.venv\Scripts\python.exe -m pytest .\tests\test_long_headline.py -m visual -v -s. No Metro env change.
1. Session70b80dd8-59d2-439e-9e48-892c9ec6a392: exit1, 1failed16.99s. Capture1028x1237 RGBA; changed11640/1271636, ratio0.00915356281199966 (0.9153562812%), max0.002/channel12, comparison false.
2. Sessionc95db4eb-8536-47ec-b5be-2aace9a0a6fb after unknown/unsupported/none cold launches: exit1, 1failed19.68s. Same dimensions and exact same comparison metrics. Both lifecycle sequences terminate before launch/after capture.
Saved each actual/context/diff/comparison under qa_visual/artifacts/android/pixel10-api37/exec021-run1/ and exec021-run2/ (filenames long_headline.actual.png, long_headline.context.png, long_headline.diff.png, long_headline.comparison.json). Previous rolling evidence copied to exec021-prior-20261107-130812/. Logs and diagnostic JSON/XML under debug-logs/exec021/; all ignored.
Both actual PNG SHA256=6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC. Byte-identical and decoded-pixel-identical to each other, repeat changed pixels0. Compared to golden, all differences confined bbox(0,29,1028,527), within bundled image area; 16414 raw RGB pixels differ,11640 exceed12, max channel difference229. RGB region y530..1237 is pixel-identical, including text/metadata/summary/padding/corners. Baseline-vs-actual and full context inspected; card boundaries/content complete. Exact image-rasterization cause UNVERIFIED; do not change image rendering/data/golden to force green. Context also shows Expo tooling and push-token/Firebase warning outside crop; notification side effects are not fully isolated and require separate review.
Checks:
- pnpm.cmd check:ts exit0.
- pnpm.cmd test --runInBand --runTestsByPath __tests__/screens/Home/qaScenario.test.ts __tests__/screens/Home/QaLaunchGate.test.tsx __tests__/app/native-intent.test.ts --coverage=false: exit0,3suites36tests passed.
- pnpm.cmd test --runInBand --coverage=false: exit0,180suites,1438passed3skipped,1snapshot passed,41.519s. Logs debug-logs/exec021/app-tests.log.
- Python pytest -m unit -q: exit0,12passed1deselected; --collect-only -q exit0,13tests collected.
- pnpm.cmd check exit1: existing qaFeed.ts:16:11 Unknown word(FIXTUR); one cspell issue across242files. Combined check stops before TypeScript; independent TypeScript succeeds. Fixture unchanged.
Golden unchanged SHA256 E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629. No golden regeneration, thresholds, dependencies, native project or scenario UI modifications. git diff --check exit0, line-ending warnings only. Private docs and diagnostics remain ignored.
Recommendation: do NOT close EXEC-020 acceptance or begin four-scenario UI expansion. Authorize a bounded EXEC-022 image-region baseline-compatibility investigation: compare current native asset decoding/scaling and rendering profile with reviewed baseline evidence, without changing fixture/golden/thresholds. First establish root cause and request review if any rendering/native-build change is needed. Keep this failed repeatable evidence intact.


## EXEC-022 - Fixture-image mismatch investigation - 2026-11-07T13:32:33+01:00
Status: BLOCKED. Investigation produced useful image/layout evidence but did NOT establish a repeatable fix. Stop condition reached; all temporary application/test edits reverted to their pre-task contents. No baseline review/promotion justified. EXEC-020 acceptance remains open.
Initial/final Git: main, ae07a0a7cbfae8be329d2e1a63d32ede575f32c9. Same pre-existing modified/untracked list as EXEC-021; docs/ai_prompts_used.md and unrelated tooling preserved. No staging/commit/remote/push. Only retained EXEC-022 changes are ignored diagnostic scripts/images/metrics/logs and appended private handoff/prompt record. Existing EXEC-021 run1/run2 artifacts untouched.
Direct preserved-image analysis BEFORE new captures:
Inputs: approved golden and exec021-run1/long_headline.actual.png/diff.png. Difference bbox [0,29,1028,527) (x0..1027,y29..526); raw RGB differences16414; changed over existing RGB tolerance12=11640/1271636 (0.9153562812%); max channel difference229. High-count rows: y29=1018 changed pixels; y497=1028; y526=1028. Changes follow artwork edges/boundaries, not a uniform tint. Every RGB pixel at y530..1236 matches, including title, metadata, summary and bottom padding. At x20 golden dark top band includes row29, actual row29 is interpolated; golden bottom band includes row526, actual does not. Native hierarchy for initial runtime path: image [26,720][1054,1246], i.e.1028x526. The golden's source-image footprint is527px high. Detailed per-row/per-column distribution in debug-logs/exec022/image-analysis.json; existing native diff visually inspected. No altered/masked image used for comparison.
Pipeline inventory:
- app/assets/images/qa/fixture-cover.png is1200x615 RGB, SHA256 5CC957CB90BAC87218D5D81406B9056B8394B579318B498E70990C2D78B87570. Working bytes equal committed blob. Metro GET /assets/assets/images/qa/fixture-cover.png?platform=android&hash=unused returnedHTTP200 and exact same bytes/hash. No incomplete/replaced asset evidence.
- app/src/screens/Home/fixtures/qaScenario.ts gates development-only active long_headline and supplies qa-long-headline slug; qaFeed.ts supplies fixed WordPress-shaped article, _links={} and maps through WordPressFetcher.mapArticleToPost. Data/rendering files unchanged.
- app/src/components/posts/ArticlePost.tsx imports QaFixtureCover as bundled numeric asset; QA recognition requires active flag+slug. expo-image Image receives bundled asset (not remote imageUrl); no QA placeholder. onLoad sets qaCoverLoaded, exposing qa-article-card-ready. This is image-load readiness, not an explicit layout-settled guarantee.
- app/node_modules/expo-image/src/utils/resolveSources.tsx resolves numeric sources through React Native resolveAssetSource/Metro asset metadata. Native expo-image uses Glide; installed source default cache policy DISK, default allowDownscaling true, default ARGB_8888. Cold process destroys memory state but does not clear Glide disk cache; no cache purge performed.
- app/src/hooks/useFeedDimensions.ts derives window width minus horizontal padding capped at700dp. GlobalStyles DEFAULT_IMAGE_ASPECT_RATIO=0.5125 (615/1200). ArticlePost uses full-width image, height=width*0.5125, contentFit=cover. Fractional physical dimensions are expected at420dpi; source ratio at native width1028 would imply526.85px height before rounding.
- Installed expo-image Android ExpoImageView.kt/ExpoImageViewWrapper.kt and enums/ContentFit.kt apply cover matrix to actual native view width/height, center image, and configure drawable after load. Thus observed526-vs527 target geometry can explain edge resampling/cropping differences. Exact native rounding/layout scheduling mechanism not traced. Cached decoded bitmap dimensions not instrumented.
Runtime environment held constant:
Metro PID26880 listens IPv4 127.0.0.1:8081; /statusHTTP200 packager-status:running. Appium3.3.0 ready, existing UiAutomator2. Same emulator-5554 Pixel_10/API37,1080x2424,420dpi,font_scale1.0. No services restarted/env scenario changes. Source APK installed version2.5.5/versionCode1/targetSdk36; firstInstallTime and lastUpdateTime both2026-11-01 15:12:21 (before reviewed baseline). Native APK update is not an observed intervening change. Emulator actual GLES renderer Google SwiftShader, config gpu.mode auto/RAM4096. Historical software rendering was recorded; exact historical driver/build equivalence unverified. No rebuild/reinstall/GPU change/wipe.
Native runtime-selector vs environment-fallback captures (same Metro):
Command from root: .\qa_visual\.venv\Scripts\python.exe debug-logs/exec022/capture_paths.py runtime (then fallback). Each diagnostic terminates, deep-links, verifies exact identity BEFORE ArticleCard readiness/title, captures actual/context, reads hierarchy, captures an additional after-hierarchy card to test immediate settling, compares with existing utility, terminates and quits.
- runtime URL exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=long_headline: exit1,1028x1237,11640changed/0.915356%, image native1028x526. Its after-hierarchy capture is byte-identical. SHA E3302175F862DE653CA48A06D0F383F636451DFC89D32833001AD39F80FC3992; one raw pixel differs from EXEC-021 output (bbox743,190..744,191), threshold count same.
- fallback URL same wrapper WITHOUT qa_scenario: exit0,1028x1237,0changed/0%, image native1028x527 ([26,720][1054,1247]). Actual is byte-identical to golden (approved SHA), also unchanged after hierarchy. This proves golden is reproducible in the current environment at least once; does NOT prove fallback repeatability.
Artifacts under qa_visual/artifacts/android/pixel10-api37/exec022-runtime/ and exec022-fallback/; native launch JSON and hierarchy XML included. Immediate post-load screenshots do not drift on the observed hierarchy interval, so simple incomplete image loading is unsupported, but startup layout timing remains unresolved.
Bounded route experiments (not retained):
Source inspection found EXEC-020's QA branch in +native-intent.tsx rewrites wrapper to /home while installed Expo Router already unwraps development-client URLs via inner url. Hypothesis: bypassing normal route parsing caused different native geometry. Two candidates tested without image/content/style/threshold changes:
1. Return / instead of /home: original visual pytest exit1,16.66s; actual1028x1238. Comparator reports dimension mismatch;100% changed is its mismatch sentinel, not an assertion every overlapping pixel changed. Saved exec022-root-route-attempt/.
2. Remove QA rewrite, leave wrapper intact for Router: first original visual pytest exit0,16.47s,1028x1237,0changed, byte-identical golden; second independent cold-launch test exit1,16.97s,1028x1238 dimension mismatch. Saved exec022-fixed1/ and exec022-fixed2/; these directory names refer to a REJECTED candidate, NOT an accepted fix. Second actual SHA E3615A4B3599F701C288828A2086999B417CF7C2740AFDCC4B205549CC6EC963, identical to first root-route-attempt actual. Candidate outputs are not repeatable.
Exact pytest command (from qa_visual) for all three route experiments: set child-shell VVP_QA_LAUNCH_URL to explicit runtime URL above; .\.venv\Scripts\python.exe -m pytest .\tests\test_long_headline.py -m visual -v -s. Logs debug-logs/exec022/visual-fixed1.log (root candidate), visual-final1.log and visual-final2.log. Three pytest visual executions total; two after the final candidate. No failures hidden or thresholds changed.
IMPORTANT: Initial tentative category-A/sole-route-cause inference was disproved by the second capture under unchanged candidate code. Route/startup path influences observed geometry, but root cause is NOT established. Cannot classify exclusively A/B/C/D with present evidence. Ranked unresolved hypotheses: fractional-pixel layout/navigation startup timing (strongest; measured image/card geometry changes); shared startup-gate/root navigation interaction; native ExpoImage/Yoga size rounding or cached decode sizing (not traced); renderer differences (no verified intervening change). Source asset/content change, missing image and uniform color-shift explanations contradicted by evidence. Do not call golden obsolete.
Rollback and checks:
Restored initial /home QA branch and original native-intent test expectations using targeted edits, preserving all other work. No retained app/runner changes from EXEC-022. Final restored source pnpm.cmd check:ts exit0; focused pnpm.cmd test --runInBand --runTestsByPath __tests__/screens/Home/qaScenario.test.ts __tests__/screens/Home/QaLaunchGate.test.tsx __tests__/app/native-intent.test.ts --coverage=false exit0,3suites36tests. Both candidate sources also type/focused-test passed, which did not predict native repeatability. No runner edits; Python suite not rerun in this task (EXEC-021 results historical only). Existing FIXTUR spelling issue left untouched; combined spelling check not repeated. No broad suite repeated for these narrow source experiments. git diff --check exit0, line-ending warnings only.
Firebase warning classification: normal root Index.appOpenRoutine calls NotificationManager.refreshServer without awaiting it. Token acquisition can fail in development APK lacking configured Firebase; refreshServer catches/logs. Existing QA guards elsewhere do not cover every startup call. Warning outside card, no direct fixture-source/image-layout manipulation, and successful capture/zero comparison occurred despite warning. It is nonfatal for demonstrated init/capture; no evidence establishes it as mismatch cause. No notification work performed.
Golden before/after SHA E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629; bytes match committed blob. All pre-existing evidence preserved. Final services healthy and left running; test cleanup terminated app as specified.
Recommendation: continue targeted investigation with separately authorized development-only onLayout/window/physical-pixel telemetry around root, feed, image and card, including layout at ready/capture and controlled original/gated startup comparison. No rendering fix or golden replacement justified yet. Do not close visual blocker or begin additional scenarios. Instrument before modifying layout; preserve production behavior and approved reference.


## EXEC-023 - Instrumented layout/readiness diagnosis - 2026-11-07T13:45:23.810737+01:00
Status: BLOCKED for runtime-selection visual acceptance; bounded diagnostic complete. No safe correction established or retained. Recommend legacy environment fallback as demonstrated path; runtime selection experimental. No new scenarios, goldens, thresholds, production layout edits, navigation experiments, installs, native rebuilds, wipes, commits or pushes.
Initial/final: main, HEAD ae07a0a7cbfae8be329d2e1a63d32ede575f32c9, no remotes/staging. Initial/final git status --short identical (debug-logs/exec023/initial-status.txt and final-status.txt). Preserved all existing modified/untracked files, public prompt modification and EXEC-021/022 evidence. Golden working bytes equal committed blob; before/after SHA256 E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629.
Environment: existing emulator-5554 device, API37, boot1,1080x2424,420dpi,font_scale1.0, adb reverse host-15 tcp:8081 tcp:8081. Same existing Metro IPv4 /status=packager-status:running and Appium3.3.0 /status ready true before/after; no server restart/environment changes. No storage purge. Current memory/GPU not remeasured; prior EXEC022 details historical. App left available after final fallback pytest; emulator/services left running.
Temporary instrumentation: development-only structured ReactNativeJS console QA_LAYOUT JSON with event, Date.now milliseconds and data. Added helper qaLayoutProbe.ts and temporary probes in QaLaunchGate, +native-intent, root AppFrame, index startup routine, qaFeed fetcher, Feed, GenericPost/UiCard, ArticlePost/image wrapper/expo-image, TabScreenView, AnimatedHeader and home container (11 existing files). Logged selection/source, original wrapper URL, route segments, safe-area insets, window/PixelRatio, desired article width/height, local onLayout dimensions with scaled pixel values, image load source/cacheType, readiness-state activation. No new views/styles/readiness behavior. Native hierarchy and POM capture established absolute bounds. Source module numeric asset35 resolved to1200x615, same Metro asset URL/hash807fa1296684b522f27c621135cf2a4e, cacheType disk in all six runs. Metro asset hash is not file SHA256.
Capture instrumentation: ignored debug-logs/exec023/capture_paths.py uses unchanged ArticleCard/identity/comparator, terminates before/after, records host timing plus device timestamps in later runs, screenshots actual/context then hierarchy and second element screenshot. Device clock approximately56.9s behind host; correlated same-PID telemetry and device timestamp, NOT naive host-versus-device wall-clock subtraction. First runs use last PID matching wrapper/selection and session order; later runs record exact pid/device epoch. Full telemetry.log, filtered events.json, launch.json, hierarchy.xml, actual/after-hierarchy/context/diff/comparison JSON per folder. No arbitrary sleeps, no pixels transformed for comparisons. Source backups and probe text retained only ignored under debug-logs/exec023/.
Commands from root, alternating independent sessions:
.\qa_visual\.venv\Scripts\python.exe debug-logs/exec023/capture_paths.py MODE
MODE order: fallback1(exit0),runtime1(exit1),fallback2(exit0),runtime2(exit1),fallback3(exit0),runtime3(exit1). One initial and one post-hierarchy capture per session. Each exactly verified qa-scenario:long_headline before qa-article-card-ready and QA-FIXTUR: title. All actuals1028x1237 RGBA; outer card[26,720][1054,1957]. Each immediate post-hierarchy PNG byte-identical to first capture.
URLs: fallback exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081; runtime appends &qa_scenario=long_headline. Runtime +native-intent returns /home; fallback passes wrapper through installed Router unwrapping, mounts index startup routine and then dismissTo home. Gate resolves active launch/environment selection before fixture requests in both. Same bundled bytes and environment throughout.
Results: fallback1/2/3 all0/1271636 changed,0%,PASS and SHA approved golden (byte-identical to each other). Runtime1/2/3 all11640/1271636,ratio0.00915356281199966(0.9153562812%),FAIL vs max0.002; SHA6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC, all byte-identical. Image native bounds fallback[26,720][1054,1247]1028x527; runtime[26,720][1054,1246]1028x526. Main artifact folders qa_visual/artifacts/android/pixel10-api37/exec023-{fallback1,runtime1,fallback2,runtime2,fallback3,runtime3}/. Metrics summary debug-logs/exec023/summary.json. Card/full context intact; viewed fallback3 actual and runtime3 diff, complete content/corners and image-only red differences.
Side-by-side OBSERVED measurements:
Both window411.42857142857144x923.4285714285714dp, ratio2.625,fontScale1. Feed hook width391.42857142857144dp; desired height200.60714285714286dp (526.59375px). Actual onLayout width391.6190490722656dp (~1028px) in both. Fallback image200.76190185546875dp(~527px); runtime200.38095092773438dp(~526px). Safe top54.095237731933594dp(~142px), bottom24dp(~63px), same route eventually(tabs)/home. Image dimension differs BEFORE image-load and BEFORE readiness, not a new source selection after load.
Representative fallback3 same-PID sequence relative original native-intent event: selection+131ms; fixture-fetch+1197ms; frame2424px, tab/home2282px; article desired-state+1360ms; index-startup+1421ms; feed2282px+1436ms; card1238px+1446ms; image527px+1448ms; image-load+1636ms; ready-state+1670ms; route home+1993ms; card1237px+2006ms; feed2072px+2203ms then2009px+2247ms. Appium ready observation+3347ms, capture+3599ms. Image retained527px through container changes/capture. Fallback1/2 same image527 and card1238->1237 lifecycle.
Representative runtime3: selection+131ms; fixture-fetch+1165ms; route home+1188ms; frame2424px; tab/home initially2009px (transient tab/header events also report2282px); article desired-state+1355ms; feed2009px+1377ms; card1237px+1384ms; image526px+1386ms; image-load+1718ms; ready-state+1737ms; Appium ready+2813ms,capture+3392ms. No subsequent image/card resize events after ready. Runtime1/2 same526px image and1237px card. Header transient577.99996/394.00002px telemetry seen in BOTH modes; cannot uniquely attribute mismatch to header animation. Root/safe-area values match; first feed/card layout established at different navigation/container stage.
Supported conclusion: screenshot raster difference correlates exactly with measured native image-height difference, established during initial layout, not incomplete asset or simple capture-before-settle. Fallback readiness activation precedes final CARD/container layout, so image onLoad is not generally proof all card layout is stable; however actual Appium captures occur AFTER observed changes and runtime wrong geometry remains stable. Adding settled-layout readiness alone is not demonstrated to restore golden. No arbitrary delay or speculative readiness fix implemented.
Installed Yoga PixelGrid.cpp calculates rounded dimension as rounded absolute bottom minus rounded absolute top. Fractional geometry and startup path provide a plausible mechanism; raw Yoga ancestor pre-rounding positions/native invalidation NOT instrumented, so exact origin/rounding or caching-in-layout cause remains UNVERIFIED. Logs show rounded output, not raw Yoga inputs. Do not label fractional rounding the fully proven root cause or alter production sizing. Need explicit review for native/layout-level deeper work. No route redirect/pixel offset/remount experiments in this task.
Firebase: push-token errors occurred before/around initial layout in BOTH passing fallback and failing runtime. Warning nonfatal; source previously identified as startup token handling. No measured causal relationship with image dimensions. Left notification behavior untouched.
Probe removal/final verification: restored all11 files from exact pre-task byte backups, removed helper, saved temporary-probes.json ignored. Automated byte equality assertion passed; rg QA_LAYOUT|qaLayoutProbe app/src found no matches (expected rg exit1). No retained app/runner/test/README code changes from EXEC023. Only ignored diagnostic evidence plus appended private records.
Checks after removal:
- pnpm.cmd check:ts exit0 (also passed initial instrumented source). First sandbox pnpm failed ERR_PNPM_STORE_DIR_OPEN_OPERATION_LOCK at existing local pnpm-store-operation-locks/all-stores.lock; approved escalation ran existing checks, no installs.
- pnpm.cmd test --runInBand --runTestsByPath __tests__/screens/Home/qaScenario.test.ts __tests__/screens/Home/QaLaunchGate.test.tsx __tests__/app/native-intent.test.ts --coverage=false exit0,3suites36passed.
- from qa_visual .\.venv\Scripts\python.exe -m pytest -m unit -q exit0,12passed1deselected.
- git diff --check exit0, only LF/CRLF conversion warnings. Broad Jest/combined spelling check not rerun; pre-existing FIXTUR issue unchanged.
Final uninstrumented ORIGINAL test verification (ignored wrapper debug-logs/exec023/final_smoke.py calls pytest from qa_visual, preserves rolling prior evidence):
Command .\.venv\Scripts\python.exe -m pytest ./tests/test_long_headline.py -m visual -v -s.
Runtime VVP_QA_LAUNCH_URL explicit above:1failed19.08s,exit1,1028x1237,11640changed/0.915356%,same_size true; SHA E3302175F862DE653CA48A06D0F383F636451DFC89D32833001AD39F80FC3992. Raw one-pixel variation vs instrumented captures already seen historically; threshold metrics identical, do not claim byte identity between instrumented/uninstrumented runtime images. Artifacts exec023-final-runtime/ including pytest.log.
Fallback: unset child VVP_QA_LAUNCH_URL; adb shell am force-stop de.volksverpetzer.app (exit0); adb shell am start -W -a android.intent.action.VIEW -d fallbackURL -p de.volksverpetzer.app (exit0,COLD,MainActivity,1734ms), then same pytest activation command:1passed11.33s,exit0,1028x1237,0changed,byte-identical approved golden. Artifacts exec023-final-fallback/. Appium log confirms runtime session quit at1794055393716, fallback session requested1794055397767 (no overlapping Appium sessions). Previous rolling evidence saved exec023-prior-rolling/.
One ignored diagnostic-script creation attempt was accidentally executed via stdin without mode (IndexError/no file); corrected script creation before any native execution. This did not change application/source or produce a capture.
Remaining decision: keep supported demo on environment fallback (three independent cold launches plus final original pytest PASS), runtime experimental; do not close EXEC020 visual acceptance or start four new scenarios. Further native Yoga/navigation layout investigation requires bounded reviewed scope; no safe correction or baseline change justified by current evidence. Runtime-selection acceptance requiring2PASS is NOT met.


## EXEC-024 Checkpoint 1 - Candidate preparation - 2026-11-07T14:00:59.387110+01:00
Status: PREPARED / awaiting human baseline review. Migration NOT approved or completed; Checkpoint2 not executed.
Human authorized pursuing controlled legacy-to-runtime baseline migration and preparing a review packet only. Existing native investigation remains unresolved; no additional layout experiments.
Initial Git main/ae07a0a7cbfae8be329d2e1a63d32ede575f32c9; existing modified/untracked paths preserved. Read relevant decisions, expansion decision, latest handoff/prompt record, current screenshot/comparator/runner guide and preserved EXEC023 scripts/native artifacts. No Appium/emulator/Metro operations or new native captures/tests in this checkpoint.
Command .\qa_visual\.venv\Scripts\python.exe debug-logs/exec024/prepare_review.py exit0. Pillow verified PNG validity,full decoding,1028x1237RGBA, source/copy hashes, three independent runtime session hashes/identity/title/readiness and hierarchy/outerparent bounds. Representative source exec023-runtime3 actual.png,session58287e1a-b450-41ec-89aa-514afbdd1b07, hash6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC. Identical exec023-runtime1/runtime2 capture hashes and post-hierarchy screenshots. Native element screenshot provenance confirmed via saved diagnostic script + unchanged ArticleCard screenshot_as_png implementation, not screen crop.
Ignored review packet debug-logs/exec024/review/: original.approved.png,candidate.runtime.png,side-by-side.png,existing.diff.png,verified.diff.png,image-region-2x.png,candidate.context.png,metrics.json,REVIEW.md. Copies verified unchanged; composites/enlargement only diagnostic, never baseline input. Enlarged top region nearest-neighbor2x.
Metrics vs unchangedgolden: both1028x1237; runtime image526px vslegacy527px; outer[26,720][1054,1957]. RawRGB16414(1.2907781787%), over12 threshold11640(0.9153562812%),allowed0.2%,FAIL. RGBbbox[0,29,1028,527),maxchannel229; y530onward identical. Existing diff equals recomputed overlay pixels. Candidate visually inspected with side-by-side/enlargement/diff: no obvious missing artwork,unreadable text,substantive distortion or unrelatedUI; allheadline/metadata/summary/padding/corners present. Assessment supports PROPOSING candidate, not approval. 1px image-height/resampling is acknowledged, native cause unresolved.
Qualification: source three identical nativecaptures had temporary read-only probes; final uninstrumented EXEC023 runtime actual differs from candidate by1RGBpixel,maxchannel1,bbox743,190,744,191 below unchangedtolerance. Do not claim all runtime bytes identical. New reference native PASS and two-runverification remain unexecuted.
Intended migration: environmentfallback contract -> explicitruntime coldlaunch selection, retained identity/readiness/bounds checks. Rationale consistent observed rendering under intendedlaunch, not rootcausefix. Previous approved PNG verified in HEAD history; no historychanges. No thresholds,fixture/sourceasset/UI or runnerchanges. If approved, fallback compatibility with this newreference must be documented in Checkpoint2. Exact candidate approval required before touchingbaseline.
Existing golden before/after E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629,workingbytes equalcommittedblob. Initial/final Git shortstatus identical; no staging/commit/push/remotes. Private records/reviewpacket ignored. Only created ignored packet/script and appended private handoff/AIlog; no tracked changes added. Await explicit review of candidatepath/hash beforeCheckpoint2.


## EXEC-024 Checkpoint 2 - Approved golden migration - 2026-11-07T14:25:05.223669+01:00
Status: PASS. Exact approved candidate promoted byte-for-byte; two independent original runtime-selected visual pytest tests PASS with unchanged thresholds. No new scenario work/commit/push.
Approval provenance: explicit human EXEC-024 Checkpoint2 instruction, November7,2026, verdict APPROVED after review of original,candidate,side-by-side,enlarged image-region,diff. Instruction reports reviewing-assistant checks; this agent independently revalidated local identities rather than treating reported review as runtime proof. Approval applies only candidate debug-logs/exec024/review/candidate.runtime.png, SHA256 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC.
Initial branch main,HEAD ae07a0a7cbfae8be329d2e1a63d32ede575f32c9. Initial status exact saved debug-logs/exec024/checkpoint2/initial-state.json. Pre-existing app/router/selection/tests/runner/README changes and docs/ai_prompts_used.md modification preserved; untracked gate/helper/tests/upstreamtooling retained. No staging/remotes/history modifications.
Identity preflight: Python Pillow verify+full decode1028x1237RGBA PNG; target oldhash E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629; candidate approvednewhash 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC; Git show HEAD:qa_visual/baselines/android/pixel10-api37/long_headline.png bytes equal old workinggolden. Oldimage recoverable in existing commit ae07a0a7cbfae8be329d2e1a63d32ede575f32c9; no commit created. All checks passed before shutil.copyfile(candidate,target), then exact byte+hash assertion. Target qa_visual/baselines/android/pixel10-api37/long_headline.png is the ONLY baseline changed. No PNG generation/pixel edits.
Services: emulator-5554 device boot1,existingreverse host-15 tcp:8081 tcp:8081; Metro IPv4 /status packager-status:running, listenerPID26880 before/after; Appium3.3.0 ready. No Metro restart/environment changes between tests; existing IPv4/NODE_OPTIONS setup preserved. No appasset/content/layout changes, rebuild,wipe or cachepurge. Driver terminates previous process then mobile:deepLink; cleanup terminates and quits. Distinct native sessions with prior session quit before next session start.
Exact invocation twice, cwd D:\Projects\visual_regression_qa_strategy\qa_visual:
$env:VVP_QA_LAUNCH_URL = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=long_headline'
.\.venv\Scripts\python.exe -m pytest ./tests/test_long_headline.py -m visual -v -s
Ignored wrapper commands fromroot .\qa_visual\.venv\Scripts\python.exe debug-logs/exec024/checkpoint2/run_visual.py run1, then run2; wrapper sets exact env only for child, invokes original unchanged pytesttest, archives original Appium logsegment and rolling artifacts, asserts golden before/after. No monkeypatch/testsource/instrumentation. Priorrolling artifacts preserved exec024-cp2-prior/.
run1: exit0,1028x1237RGBA,0/1271636 changed,ratio0,PASS; SHA256 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC; native rects [{'height': 1132, 'width': 1028, 'x': 26, 'y': 720}, {'height': 1237, 'width': 1028, 'x': 26, 'y': 720}]; lifecycle ["[27c25306][AppiumDriver@aaae] Event 'newSessionStarted' logged at 1794057646775 (14:20:46 GMT+0100 (Central European Standard Time))", "[27c25306][AppiumDriver@aaae] Event 'quitSessionFinished' logged at 1794057663060 (14:21:03 GMT+0100 (Central European Standard Time))"]
run2: exit0,1028x1237RGBA,0/1271636 changed,ratio0,PASS; SHA256 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC; native rects [{'height': 1132, 'width': 1028, 'x': 26, 'y': 720}, {'height': 1237, 'width': 1028, 'x': 26, 'y': 720}]; lifecycle ["[665ef1f7][AppiumDriver@aaae] Event 'newSessionStarted' logged at 1794057674750 (14:21:14 GMT+0100 (Central European Standard Time))", "[665ef1f7][AppiumDriver@aaae] Event 'quitSessionFinished' logged at 1794057687310 (14:21:27 GMT+0100 (Central European Standard Time))"]
Pytest durations19.66s and15.82s respectively,1passed each. Both logs show exact qa-scenario:long_headline identity lookup before article-ready, successful ready-element display/title QA-FIXTUR: assertion, containment checks and native parent element screenshot. Readyrect1028x1132 at26,720; outerrect1028x1237 at26,720 ->[26,720][1054,1957]. Artifacts each qa_visual/artifacts/android/pixel10-api37/exec024-cp2-run1/ and exec024-cp2-run2/: long_headline.actual.png,long_headline.context.png,long_headline.diff.png,long_headline.comparison.json,pytest.log,appium.log,run.json. No extra diagnostic Appium session/capture needed.
Repeatability: actual1/actual2 byte-identical and decodedRGBA-identical,rawRGBchanged0,maxchannel0,policychanged0/1271636(0%). Each also equals exactapprovedcandidate. Diagnostic repeatability.json/diff under debug-logs/exec024/checkpoint2/. Existingpolicy verified channel_tolerance12,max_changed_ratio0.002; nooverride or sourcechange. Newgolden stable after both tests. Historical onepixel/channel1variation remains known; no universal byteidentity claim.
Regression checks:
- pnpm.cmd check:ts fromapp exit0.
- pnpm.cmd test --runInBand --runTestsByPath __tests__/screens/Home/qaScenario.test.ts __tests__/screens/Home/QaLaunchGate.test.tsx __tests__/app/native-intent.test.ts --coverage=false exit0,3suites36passed.
- fromqa_visual .\.venv\Scripts\python.exe -m pytest -m unit -q exit0,12passed1deselected.
- pnpm.cmd check exit1: existing src/screens/Home/fixtures/qaFeed.ts:16:11 Unknown word(FIXTUR),1issue/242files. Combinedcheck stops before tsc; separateTypeScript passes. Fixture/content unchanged. Existinginstalled checks used approved pnpm-store access; noinstall.
- git diff --check exit0,pre-existing LF/CRLF warnings only. Relative README linktarget checks pass after correcting diagnostic reader to explicitUTF8; no documentation-file encoding damage retained.
Documentation changed: qa_visual/README.md reconciles stale EXEC020 unverified statements, explicitruntimecommand/ordering and verified Android checks; adds dated humanapprovedmigration withold/newhashes,0changed two-runproof,originalGit recovery,uncommittedstatus,legacyfallbackwarning,unchangedthresholds and unresolvednative rounding. Generic manualreplacement snippet still marked documentedprocedure rather than exactcommands executed. RootREADME quickstart uses explicitURL plus documented IPv4Metro startup (not restarted this task),two-runresults/migrationstatus. qa_visual/baselines/README.md updateshash/date/launchcontract andoldhistoryreference. StrategyMD/PDF remain unchanged; historicalscope/metrics stillvalid. No CI/iOS claims.
Private decision/handoff/prompt records append approval,contractchange andverifiedresults. No privatebrief copied publicly. Existing reviewpacket remains Checkpoint1 historical evidence; candidatecopyhash unchanged. New migration islocal/uncommitted; previousgolden stillcommitted atHEAD. Changed this task: targetPNG,rootREADME,runnerREADME,baselineREADME,threeignoredprivate records plusignoreddiagnostics/artifacts. Allotherpreexisting filehashes preserved.
Remainingrisks: nativefractional-layout mechanismunresolved; environmentfallback mayfailbydesign against runtimegolden; display/renderingprofilemustremainpinned; developmentclient/Metrodependency not standaloneCIproof; persistedtheme/settings survivecoldlaunch; fourfutureIDs remainunsupported,no iOS/CIexecution. ExistingFIXTUR combinedcheckissue remains. This closes supportedlong_headline runtimevisual-baseline blocker under reviewedcontract, not broaderenvironmentguarantees.
Recommendation: await humanreview; nextbounded breaking_news implementation proposal should inspectminimalrealbannerextension,fixture/readiness/stateisolation andpreserve long_headline regression. No newscenarioUI/test/golden until separatelyauthorized.


## EXEC-025 - Breaking-news scenario candidate - 2026-11-07T14:39:07.101213+01:00
Status: PASS for implementation/native capture/repeatability/candidate preparation; official breaking-news golden remains UNAPPROVED and ABSENT. Both new visual pytest executions expectedFAIL only at missingbaseline. Await exactcandidate humanreview before promotion/another scenario.
InitialGit main,HEAD ae07a0a7cbfae8be329d2e1a63d32ede575f32c9; initialstatus saved debug-logs/exec025/initial.json. Preserved pre-existing modifications/untrackedupstreamtooling and priorrecords/evidence. Longgolden remains 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC (existingapprovedruntimebaseline; noPNGchanges). No stage/commit/push/remotes/install/CI/iOS/native rebuild/wipe/service restart.
Inspected AnnouncementCard source: mascot/image,impressionanalytics,useEffect,dismissbutton/action/navigation; not an authentic breakingnews feature. Not reused or modified. New banner explicitlysample-app extensionforthechallenge,not upstreamVVP productioncapability.
Implementation:
- app/src/screens/Home/fixtures/qaScenario.ts: enablesbreaking_news inexistingtypedregistry; exportsqaActiveScenario typedlivebinding setoncewithinitialselection before feedmount. Originalvalidation,precedence,__DEV__ gate andimmutablelauncharchitecture retained; threeotherfutureIDs remainunsupported.
- newqaBreakingNews.ts: frozen typedlabel/title syntheticpayload; fixedEILMELDUNG andGermanQA-Test headline. ExistingqaFeed.ts/WordPressmapper/ArticlePost/imageasset untouched; originaldeterministicarticle reusedbelowbanner,stablepagination/order. No newfixturearticledata,randomtime ornetworkrequest.
- newQaBreakingBanner.tsx: realView/Typography,existingspacing/radii,pinnedred/whiteborderandtypography; noanimation/dismiss/action/impression/analytics/media/time. BothFeedentry andcomponent itself require __DEV__,activefixture and exactbreaking_news. qa-breaking-banner-ready onlyafterpositivecontainerANDtitle onLayout; separateqa-breaking-banner-title/label. Currentrootfont-loadinggate reused. Normal/release UI notexposed; source/unitrelease proof only,notexecutedreleaseAPK.
- app/src/screens/Home/components/Feed.tsx: QAconditional ListHeaderComponent beforeordinaryarticle; long_headline/normalretain originalannouncement branch. No newwrapper forlong_headline. Announcementsremain suppressedbyexistingQA homeflag.
- qa_visual/visualqa/scenario_launch.py: permits exactsingleexplicitlong_headline/breaking_news; parameterizedidentitywait defaultlong_headline preservesexistingAPI. Same coldterminate/deepLink/cleanupcontract.
- newvisualqa/components/breaking_banner.py: separateComponentObject forrawtestID,positive/displayedstablebannerrect observedover2consecutivepolls(no fixedsleep),exacttitle,viewportandlabel/titlecontainment; nativebanner.screenshot_as_png,notparentguess/screenscreencrop. HomeScreen.breaking_banner exposesit.
- newtests/test_breaking_news.py: exactscenarioidentity,titleassertion,measuredready/capture/context/hierarchy/captureJSON,cleanup,candidate-onlymissinggoldenfail; futurecomparisonusestheunchangedPillowpolicy. Existinglong_headline.py adds explicitexpectedidentity afterdrivercreation topreventwrongscenario capture nowthatdriver supports2IDs. Existingpaths/title/bounds/data unchanged.
Testsadded/extended: app/__tests__/screens/Home/QaBreakingBanner.test.tsx (layoutready,otherID,disabledfixture,releaseguard),qaScenario.test.ts(registrysupport/override/release); Pythonnewtest_breaking_banner_unit.py containmentfailure and test_scenario_launch_unit.py exactbreakingidentity. No newframework/dependencies.
Nativeenvironment: sameMetroIPv4PID26880 throughout,running /status; Appium3.3.0ready; emulator-5554 online. MetroenvironmentEXPO_PUBLIC_QA_SCENARIO stayslong_headline; explicitruntimequery selectsdifferentfixture. Noresetstorage; eachsessionterminatespreviousapp andcleanupbefore next. Breaking->breaking->long sequenceproveslongidentity restoredwithoutMetrochanges. Persistedtheme/settings limitationsunchanged.
Exactcommands cwdqa_visual,childenvVVP_QA_LAUNCH_URL = exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=breaking_news:
.\.venv\Scripts\python.exe -m pytest ./tests/test_breaking_news.py -m visual -v -s
Run1:1failed19.37s,exit1,ONLYGoldenmissing aftersuccessfulexactidentity/ready/title/capture. Run2:1failed16.15s,exit1,samemissingbaselineonly. NativecapturePASS both. Each1028x493RGBA;bannerbounds[26,720][1054,1213],label[83,777][995,845],title[83,872][995,1156]. QAidentitymarker[0,168][3,171]outsidecapture. Sessions728bceeb-33ee-4e9c-b931-c8387c7439e7 and3430e85e-03b8-4a3c-b4d7-ed5bb75754e7;serverquit precedesnextstart. Noextravisualsessionsfornegativecases.
Artifacts: qa_visual/artifacts/android/pixel10-api37/exec025-breaking1/ andexec025-breaking2/: breaking_news.actual.png/context.png/hierarchy.xml/capture.json,pytest.log,appium.log,run.json. Originalnativeoperation innewPOM,exactassertions executed; logs/hierarchy supportprovenance.
Repeat: nativeactual1/2byte-identical anddecodedRGBAidentical;SHA256 E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F;rawRGBchanged0/506804(0%),maxchannel0;existingPillowtolerance12/maxratio0.002changed0/506804(0%),PASS forrepeatability ONLY. Noapprovedbannerreferencecomparisonexecuted. Candidate copiedbyte-forbyte tonongoldenignoreddebug-logs/exec025/review/breaking_news.candidate.png; fullcontext,repeatability.diff.png/repeatability.json/REVIEW.md alongside. No baselines/android/pixel10-api37/breaking_news.png exists.
Visualassessment: inspectedfirstactualandfullcontext; fullredborder/roundedcorners/padding,EILMELDUNG,4readableheadline lines,notruncation/overlap. Contextplacesbannerbelowheaderandaboveactualfixturearticle. Existingpush-token/Firebasewarning/devtoolsoverlayoutsidebanner; no newnotificationwork orapp-widenetworkisolationclaim. Secondactualexacthash provesidenticalbannercontent. HumanreviewNOTsubstitutedbyagentassessment.
Existinglongregression,explicitURLqa_scenario=long_headline,sameMetro:
.\.venv\Scripts\python.exe -m pytest ./tests/test_long_headline.py -m visual -v -s
1passed16.35s,exit0,1028x1237RGBA,0/1271636changed(0%),approvedSHAunchangedandactualequalsgolden. Sessionbe0f2ab3-capturerecord/fullserverlog underexec025-long-headline/. Standardactual/context/diff/comparisonJSON retained. All3sessionsindependent; noimage/threshold/baselinerepair.
Checks:
- Initialpnpm.cmd check:ts exit1: TS2352newtestglobalcast; correctedtest-only cast throughunknown. Finalcheck:ts exit0.
- InitialfocusedJest exit1: layoutfireEventisasyncininstalledtesting-library,unawaitedtestevents causedmissingready/actwarning; correctedawait. Nextfocusedexit1: importnamespacecopywasmutatedinsteadofmockobject; fixedtesttojest.requireMock. Finalfocused4suites39passedexit0; afterwardaddeddisabledfixturetest includedfinalbroadrun.
- pnpm.cmd test --runInBand --coverage=false exit0,181suites1442passed3skipped,1snapshotpassed,38.964s; logdebug-logs/exec025/jest-all.log. Existingconsolewarnings mayoccur; nosuitefailures.
- .\.venv\Scripts\python.exe -m pytest -m unit -q exit0,14passed2deselected.
- .\.venv\Scripts\python.exe -m pytest --collect-only -q exit0,16testscollected;collectionnotdeviceexecution.
- pnpm.cmd check exit1 ONLYunchanged qaFeed.ts:16:11 UnknownwordFIXTUR,1issue/244files. SeparateTypeScriptPASS; fixturetextpreserved. Logcombined-check.log.
- git diff --check exit0,lineendingwarnings only; READMErelativefiletargetchecksPASS. No packageinstall.
Documentation: root/runnerREADMEs accuratelystate2capture-supportedAndroidscenarios,oneapprovedreference/onependingcandidate; runneraddsbreakingcommand,fixture/POM/readiness/provenance/missingbaseline/metrics/productionboundary andrealbannerextensiondisclosure. Sanitizeddocs/ai_prompts_used.md appendedmaterialtasksummary,preservingexistingchanges. StrategyMD/PDF unchangedhistoricalscope. Privatehandoff/prompt/decisionsappendverifiedscope andapprovalpending; privatecontentnotcopiedpublicly.
GoldenafterSHA6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC; HEAD unchanged; no staging/remotes. Remaining: humanreviewexactcandidatepath/hash then separatelyauthorizedpromotionandnewreferencevisualverification; other3scenarioUIsunsupported. Existingcspellissue andnativefractionalrounding/persistedstate/devclientdependence remain. Noautoapproval,CI,iOS ornewscenariofollow-on.


## EXEC-026 - Breaking-news golden promotion and verification - 2026-11-07T14:56:26.851036+01:00

Status: PASS. Two independent breaking_news visual comparisons and the existing long_headline regression pass against the exact approved references. No application, fixture, image source, layout, runner, comparator or threshold changes.

Approval: the human decision-maker explicitly APPROVED the exact EXEC-025 candidate after candidate/context review on November 7, 2026, in the EXEC-026 instruction. Reviewing-assistant inspection was reported by the human; this run independently checked local files/provenance.

Promotion:
- Source: debug-logs/exec025/review/breaking_news.candidate.png.
- Destination: qa_visual/baselines/android/pixel10-api37/breaking_news.png.
- SHA-256 before copy and after all tests: E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F.
- Valid PNG, fully decoded, 1028 x 493 RGBA. Source bytes match both independent EXEC-025 native captures; metadata has exact scenario identity and rect x26,y720,width1028,height493; distinct source sessions verified. Saved diagnostic script and live POM use native element screenshot, not a full-screen crop. Target absent before promotion. shutil.copyfile copied exact approved bytes; no regeneration or overwrite of another baseline.
- long_headline remains byte-unchanged this task, SHA-256 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC.

Initial Git: main, HEAD ae07a0a7cbfae8be329d2e1a63d32ede575f32c9; exact short status and protected pre-existing file hashes saved debug-logs/exec026/initial.json. Existing modifications/untracked files preserved. No staging, commit, push or remote. New banner PNG is local/untracked; previous runtime long-headline migration remains local/uncommitted.

Runtime: existing emulator-5554 online, boot1; Metro IPv4 127.0.0.1:8081 /status=packager-status:running, listener PID26880 before/after; Appium3.3.0 /status ready. Same Metro process/environment throughout, EXPO_PUBLIC_QA_SCENARIO unchanged. No service restart, rebuild, reinstall, storage wipe or notification work.

Exact command from qa_visual for breaking1 and breaking2, each separate Appium session/cold app launch:
$env:VVP_QA_LAUNCH_URL = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=breaking_news'
.\.venv\Scripts\python.exe -m pytest ./tests/test_breaking_news.py -m visual -v -s
Driver terminates prior app, uses existing mobile:deepLink helper, verifies qa-scenario:breaking_news, then component readiness from positive title/container layout and repeated unchanged native rectangles, exact expected QA-Test headline, viewport and child containment; native element screenshot; cleanup terminates then quits. Both complete before next session.
- Run1: 1 passed,19.79s,exit0,1028x493RGBA,0/506804 changed,ratio0,PASS.
- Run2: 1 passed,15.92s,exit0,1028x493RGBA,0/506804 changed,ratio0,PASS.
- Both capture rects x26,y720,width1028,height493 ->[26,720][1054,1213]. Native identity/title/readiness and screenshot operations supported by per-run Appium logs and capture/hierarchy JSON/XML.
- Both actual SHA equals exact approved banner SHA above.

Repeatability: byte-identical and decodedRGBA-identical; rawRGB differences0/506804(0%),maxchannel0; comparator-adjusted changed0/506804(0%),equivalent. Comparator remains channel delta>12,max ratio0.002. Metrics/diff debug-logs/exec026/repeatability.json and repeatability.diff.png. No baseline or tolerance adjustment after tests.

Long-headline command from qa_visual, explicit URL same wrapper with qa_scenario=long_headline:
.\.venv\Scripts\python.exe -m pytest ./tests/test_long_headline.py -m visual -v -s
Result:1 passed,16.54s,exit0,1028x1237RGBA,0/1271636 changed,ratio0,PASS. Actual equals unchanged approved long PNG. Confirms breaking->breaking->long sequential launches preserve exact scenario identity without changing Metro environment.

Artifacts: qa_visual/artifacts/android/pixel10-api37/exec026-breaking1/, exec026-breaking2/, exec026-long-headline/. Each contains scenario.actual.png,scenario.context.png,scenario.diff.png,scenario.comparison.json,pytest.log,appium.log,run.json; banner folders additionally breaking_news.capture.json and hierarchy.xml. Ignored wrapper debug-logs/exec026/run_visual.py invokes original pytest tests and preserves each run. Three native tests total in this task; no new scenarios or diagnostic capture sessions.

Checks this task:
- pnpm.cmd check:ts from app: exit0.
- pnpm.cmd test --runInBand --runTestsByPath __tests__/screens/Home/qaScenario.test.ts __tests__/screens/Home/QaLaunchGate.test.tsx __tests__/screens/Home/QaBreakingBanner.test.tsx __tests__/app/native-intent.test.ts --coverage=false: exit0,4suites40passed.
- From qa_visual .\.venv\Scripts\python.exe -m pytest -m unit -q: exit0,14passed2deselected.
- pnpm.cmd check: exit1,ONLY existing src/screens/Home/fixtures/qaFeed.ts:16:11 Unknown word(FIXTUR),1issue/244files; combined spelling failure stops before TypeScript, independent tsc succeeds. Untouched fixture. Log debug-logs/exec026/combined-check.log. No broad Jest rerun needed for baseline/docs-only change; EXEC-025 broad result remains historical.
- git diff --check exit0; existing line-ending conversion warnings only. Relative README file targets resolve. Final golden hashes and initial protected file hashes verified; HEAD unchanged; no staged files/remotes.

Documentation changed: qa_visual/baselines/README.md inventories two exact approved references with hashes/dimensions/explicit launch IDs and review-before-replacement policy. qa_visual/README.md records human approval and successful post-promotion results, retains exact PowerShell commands for each fixture, distinguishes historical EXEC-025 missing-baseline failures, keeps review/regeneration human-controlled, states no CI/native iOS execution. Root README reconciles two approved scenarios and uncommitted state; challenge-specific banner extension attribution retained. Sanitized public prompt record appended; no private brief copied. StrategyMD/PDF unchanged historical deliverable.

Files changed this task: new banner golden; root README, runner README, baseline README, sanitized docs/ai_prompts_used.md; appended ignored private decisions/handoff/AI log; ignored diagnostics/artifacts. Initial code/fixture/assets/long golden and unrelated untracked files unchanged. Historical candidate/review packet retained as provenance, not rewritten.

Remaining limitations: pinned profile and development-client/Metro dependency; persistent theme/settings survive process termination; native fractional-layout root cause remains unresolved; no CI, native iOS, dark_article/no_image/empty_feed UI. Existing Firebase warning unrelated to this captured banner and untouched. Next: human review EXEC-026, then separately authorize bounded dark_article work with explicit theme-state isolation and preservation of both approved regressions. No automatic continuation or Git publication.


## EXEC-027 - Dark article native candidate - 2026-11-07T15:14:23.006686+01:00

Status: PASS for implementation, native capture, isolation and candidate preparation. Dark golden NOT approved/promoted; both dark pytest runs exit 1 only because reference is missing.

Initial state: main, HEAD ae07a0a7cbfae8be329d2e1a63d32ede575f32c9. Existing tracked/untracked work preserved; exact initial/final status saved debug-logs/exec027/initial-status.txt and final-status.txt. No staged files, commit, remote or push. Both approved PNGs verified before/after by SHA-256, irrespective of timestamps:
- long_headline: 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC.
- breaking_news: E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F.
No golden pixels changed; dark_article.png remains absent from baselines.

Architecture observed: SettingsProvider loads appearance from SettingsStore/AsyncStorage before children render; persistent theme setter is separate. useAppColorScheme normally picks stored light/dark or system useColorScheme. UiCard, ArticlePost and Typography consume real Colors from installed VVP design tokens. QaLaunchGate resolves immutable selection before root/provider/feed mount.
Minimal implementation: qaScenario registry enables dark_article and exports guarded getQaThemeOverride() returning dark for active dark_article, light for other supported QA scenarios, undefined outside __DEV__/active fixture. Shared hook reads override after unconditional context/device hooks, before normal preference resolution. No persistent setter/storage write added. ArticlePost exposes effective hook result as nonvisual accessibilityLabel qa-theme:dark/light on existing QA pressable; no layout/style/fixture/image changes. Release gating source/unit checked, no release build executed.

Python: scenario_launch allows explicit dark_article with existing terminate/deepLink/exactidentity flow. ArticleCard adds effective_theme marker check and observable twice-equal outer/title rect stability/viewport containment; existing native parent screenshot/containment/larger-bottom logic unchanged. New test_dark_article.py requires explicit URL, exact identity, effective dark, image-loaded existing ready ID, full expected QA-FIXTUR title, stable geometry; saves native card/context/hierarchy/capture metadata. Existing long test now explicitly verifies light marker. Unit coverage adds theme markers, missing-marker rejection, repeated layout and dark launch identity. No comparator refactoring or threshold changes.

Runtime: emulator-5554 online, boot1; IPv4 Metro /status packager-status:running, same PID26880 confirmed by netstat (CIM Get-NetTCPConnection unavailable: access denied); Appium3.3.0 ready. Existing adb reverse host-15 tcp:8081 tcp:8081. No service restart, Metro environment change, install, rebuild, wipe, user-setting modification or notification work. Device ui_night_mode=1. Same Metro retains long_headline environment fallback; URL selects each scenario explicitly.

Exact command from qa_visual (URL set per scenario in child environment):
$env:VVP_QA_LAUNCH_URL = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=dark_article'
.\.venv\Scripts\python.exe -m pytest ./tests/test_dark_article.py -m visual -v -s
Execution/archiving wrapper: debug-logs/exec027/run_visual.py, original test commands in each run.json. Independent sequence:
1. dark1: native capture succeeds, 1 failed21.66s exit1 ONLY Golden missing. Exact qa-scenario:dark_article, qa-theme:dark, full expected title/readiness verified. Session2f04b795-24df-4470-bc22-8b691127e0f6.
2. long-light: explicit qa_scenario=long_headline; original test_long_headline.py command same pytest flags. 1passed17.21s exit0, effective light asserted,1028x1237,0/1271636 changed,ratio0,PASS,actual equals approved long SHA.
3. dark2: native capture succeeds,1failed20.43s exit1 ONLY Golden missing. Exact dark identity/theme/title/readiness again. Session60152626-6e37-4bdf-bd55-88dfb4a44c49.
4. breaking-light: explicit qa_scenario=breaking_news; original test_breaking_news.py same flags.1passed16.89s exit0,1028x493,0/506804 changed,ratio0,PASS,actual equals approved banner SHA. Light override follows same hook policy; no extra dedicated theme assertion in banner test.
Each app terminated in cleanup before the next independent launch; no live switching.

Both darks1028x1237RGBA,outer rectx26,y720,width1028,height1237 ->[26,720][1054,1957]; innerready[26,720][1054,1852], title[104,1283][974,1567]. Scenario marker[0,168][3,171]. Both byte-identical/decodedRGBA-identical SHA256 6FD667E87476F941F7CB7A8152F60FFB8C51A3FD4217A7E993300AB32EB62A96. RawRGBdifferences0/1271636(0%),maxchannel0; comparator delta>12/maxratio0.002 differences0(0%),equivalent for repeatability. No dark approved-reference comparison PASS claimed.

Artifacts: qa_visual/artifacts/android/pixel10-api37/exec027-dark1/,exec027-dark2/,exec027-long-light/,exec027-breaking-light/: nativeactual/context,pytest/Appiumlogs,run.json; dark hierarchy/captureJSON; approved scenarios diff/comparisonJSON. Review packet ignored debug-logs/exec027/review/: dark_article.candidate.png exactcopydark1, dark_article.context.png, repeatability.diff.png, repeatability.json,repeatability.comparison.json,REVIEW.md. Candidate valid fully decoded PNG. Agent visually inspected dark1 actual and dark2 context (identical article proves both), complete four-lineheadline/artwork/metadata/summary/lowerpadding/corners, no clipping/overlap/unrelatedUI inside element. Genuine token colors in native capture: background#050D0F654121pixels,text#F7F7F746331pixels,muted#AAAAAA2959pixels; no overlay/screenshot manipulation. Fullcontext contains existing Firebase/push/devtool controls outsidecard, untouched. Human approval still required; visual assessment does not authorize promotion.

State isolation: read ONLY themePreference via adb exec-out run-as database bytes into in-memory SQLite; no raw storage contents printed or saved. Stored system observed after dark1/before light, and after dark-light-dark/breaking. No theme-setting changes. Hook tests cover conflicting stored/device choices without setter calls, plus normal behavior. Original SettingsStore migration logic untouched; other persistent settings/onboarding remain and no app-wide network isolation claimed.

Validation:
- pnpm.cmd check:ts from app exit0.
- focused Jest six suites52passed exit0 (hook,scenario,gate,banner,SettingsProvider,native-intent); expected storage-failure test logs console.error.
- pnpm.cmd test --runInBand --coverage=false exit0:181suites1443passed3skipped,1snapshotPASS,43.345s; full log debug-logs/exec027/jest-all.log.
- from qa_visual .\.venv\Scripts\python.exe -m pytest -m unit -q exit0,19passed3deselected; --collect-only -q exit0,22collected. Collection distinct from execution.
- Initial mistaken root-directory Python invocation failed7imports(ModuleNotFoundError visualqa), tool exit1; reran from documented qa_visual cwd, no source workaround.
- pnpm.cmd check exit1 ONLY unchanged qaFeed.ts:16:11 UnknownwordFIXTUR,1issue/244files; separatetscPASS. Log combined-check.log. Do not alter fixture/golden to silence spelling.
- git diff --check exit0; existing LF/CRLF warnings only. Ignore checks confirm private/diagnostic/artifacts excluded. No dependencies installed.

Task files: app/src/screens/Home/fixtures/qaScenario.ts, app/src/hooks/useAppColorScheme.ts, app/src/components/posts/ArticlePost.tsx; app/__tests__/hooks/useAppColorScheme.test.tsx and __tests__/screens/Home/qaScenario.test.ts; qa_visual/visualqa/scenario_launch.py,components/article_card.py; tests/test_dark_article.py(new),test_long_headline.py,test_article_card_unit.py,test_scenario_launch_unit.py; rootREADME,runnerREADME,baselineREADME,sanitizeddocs/ai_prompts_used.md; appended ignored private records and diagnostic artifacts. Existing unrelated modifications/untracked files preserved.

Remaining: candidate human review and separately authorized exact-hash promotion/two native reference comparisons. No dark baseline yet; no_image/empty_feed unsupported, no CI/iOS/commit/push. Native fractional-layout mechanism unresolved; pinned dev-client environment still required. No persisted preference changed on device to test opposing values; that condition covered by hook tests, runtime proof uses existing system preference. Stop after EXEC-027.


## EXEC-028 - Dark golden promotion and regression verification - 2026-11-07T15:37:11.045622+01:00

Status: PASS. Human explicitly approved exact EXEC-027 dark candidate on November7,2026 after PNG/context review; approval instruction also reports reviewing-assistant inspection. This run independently verified local hash/PNG/native provenance before promotion.

Initial Git main, HEAD ae07a0a7cbfae8be329d2e1a63d32ede575f32c9. Exact initial status and protected source/test hashes saved debug-logs/exec028/initial.json. All pre-existing tracked/untracked work retained. No staging, commit, push or remote creation.

Promotion: debug-logs/exec027/review/dark_article.candidate.png -> qa_visual/baselines/android/pixel10-api37/dark_article.png using shutil.copyfile, target confirmed absent. Valid fully decoded1028x1237RGBA PNG. Exact approved/source/destination SHA256 6FD667E87476F941F7CB7A8152F60FFB8C51A3FD4217A7E993300AB32EB62A96. Candidate bytes match both EXEC-027 genuine native screenshots; distinct sessions2f04b795-24df-4470-bc22-8b691127e0f6 and60152626-6e37-4bdf-bd55-88dfb4a44c49, capture metadata exactscenario/theme/bounds and screenshot server evidence verified. No regeneration/pixel alteration. New golden local/untracked,not committed.

Existing goldens verified before/after unchanged:
- long_headline SHA2566A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC.
- breaking_news SHA256E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F.
All three final hashes checked after tests. Comparator source/thresholds unchanged: RGB channel delta>12,maximum ratio0.002.

Runtime: emulator-5554 online,boot1; MetroIPv4 /status packager-status:running,PID26880 before/after; Appium3.3.0 ready. Same Metro process/environment throughout, no fixture env change/restart/rebuild/reinstall/wipe. Existing nonpersistent QA hook selects actual VVP dark/light tokens before article mount; no implementation change this task.

Exact command from qa_visual, each independent driver/cold app launch (URL set only in child test environment by ignored wrapper debug-logs/exec028/run_visual.py):
$env:VVP_QA_LAUNCH_URL = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=dark_article'
.\.venv\Scripts\python.exe -m pytest ./tests/test_dark_article.py -m visual -v -s
For light scenarios substitute qa_scenario=long_headline / breaking_news and ./tests/test_long_headline.py / ./tests/test_breaking_news.py. Exact executable,URL,args,exit and hash saved in each run.json.

Sequential results, all exit0 and1passed:
- dark1:20.52s,1028x1237,0/1271636changed,ratio0,PASS; sessionff72fb5b-35d1-495c-8eaf-72b7eb8ac8cd.
- dark2:17.21s,same dimensions,0changed,PASS; session713fc94c-187e-478f-8e2a-04db1c54eb70.
- long-light:18.37s,1028x1237,0/1271636changed,ratio0,PASS; effective light asserted by original test.
- breaking-light:18.47s,1028x493,0/506804changed,ratio0,PASS; saved native hierarchy independently parsed qa-theme:light on underlying article[26,1266][1054,2151], no dark marker. Evidence debug-logs/exec028/breaking-theme-evidence.json. Original test/framework unchanged.
- dark-after-light (explicitly authorized optional isolation check):17.14s,1028x1237,0/1271636changed,ratio0,PASS; exactdarkidentity/effectivetheme restored.

Dark tests verify qa-scenario:dark_article before readiness; qa-theme:dark; exact expected QA-FIXTUR title; bundled image loaded; repeated unchanged outer/title rectangles/viewport containment; native direct-parent screenshot/containment/larger-bottom. All dark outer bounds[26,720][1054,1957]. Each app terminated and session quit before next launch. No live switching or capture of another scenario. Actuals equal exact approved dark hash. First/second dark byte-identical,decodedRGBA-identical;rawRGB0/1271636(0%),maxchannel0; comparator0changed(0%),equivalent. Finaldarkafterlight byte-identical too. Metrics/diff debug-logs/exec028/repeatability.json,repeatability.comparison.json,repeatability.diff.png.

Artifacts: qa_visual/artifacts/android/pixel10-api37/exec028-dark1/,exec028-dark2/,exec028-long-light/,exec028-breaking-light/,exec028-dark-after-light/. Each includes scenario.actual.png/context.png/diff.png/comparison.json,pytest.log,appium.log,run.json. Dark folders additionally hierarchy.xml/capture.json; breaking folder also its existing capture/hierarchy diagnostics. Aggregate evidence debug-logs/exec028/verification.json. StoredthemePreference read ONLY by in-memorySQLite from adb run-as database bytes, value system before/after; no private DB saved/printed and no settings altered. Opposing persisted/device values remain unit-tested rather than changed on device.

Checks:
- pnpm.cmd check:ts exit0.
- pnpm.cmd test --runInBand --runTestsByPath __tests__/hooks/useAppColorScheme.test.tsx __tests__/screens/Home/qaScenario.test.ts __tests__/screens/Home/QaLaunchGate.test.tsx __tests__/screens/Home/QaBreakingBanner.test.tsx __tests__/helpers/SettingsProvider.test.tsx __tests__/app/native-intent.test.ts --coverage=false exit0,6suites52passed; logjest-focused.log.
- pnpm.cmd test --runInBand --coverage=false exit0,181suites1443passed3skipped,1snapshotpassed,35.936s; logjest-all.log.
- From qa_visual .\.venv\Scripts\python.exe -m pytest -m unit -q exit0,19passed3deselected; --collect-only -q exit0,22collected. Collection distinct from execution.
- pnpm.cmd check exit1 ONLY existing qaFeed.ts:16:11 UnknownwordFIXTUR,1issue/244files; logcombined-check.log. No fixture spelling/golden change. SeparateTypeScriptPASS.
- Protected app/source/test/runner/comparator hashes equal initial snapshot; no code/config/fixture/assets/layout changes. git diff --check passes with existing LF/CRLF notices. README relative links verified and private/artifacts/debuglogs ignored.

Documentation: rootREADME now3approvedAndroidscenarios, realdark/nonpersistenttheme,separateapprovedreference; runnerREADME retains exact explicit launch commands for all3 and updates historicalcandidate/missingbaseline status to approved/passing; baselineREADME inventories exactdarkhash/dimensions/approval/policy; sanitizedAIprompt appended. Historicalreviewpacket unchanged as provenance. Private decisions/handoff/prompt appendverifiedapproval/results. No private employer content copied public.

Changed this task: new dark_article baseline; README.md,qa_visual/README.md,qa_visual/baselines/README.md,docs/ai_prompts_used.md; appended3ignoredprivate records; ignoredgenerateddiagnostics. HEAD unchanged,no stagedfiles/remotes. Both older approvedbaselines unchanged; unrelated work preserved.

Remaining: nativefractionalroundingmechanism unresolved,pinnedAndroidrendering/devclient/Metrodependency; other persistedsettings survive; releasegate source/unitchecked but no releasebuildruntimeproof; CI/nativeiOS unverified; no_image/empty_feed unsupported. Firebasewarning untouched/outsidecapture. Next smallest separately authorized task: inspect existing optional-media ArticlePost behavior, then implement deterministic no_image with genuine no-media rendering, readiness/bounds,repeatability/candidate and3existingregressions; no automaticgoldenapproval. Stop after EXEC-028 pendinghumanreview.

## PRE-EXEC-029 - Local Git checkpoint - 2026-11-07
Status: PASS. Local commit f0b38e91724bac180fdcf9b1febd592184f22922 (f0b38e9) on main, parent ae07a0a7cbfae8be329d2e1a63d32ede575f32c9: "feat(qa): establish runtime-selected Android visual regression suite". 33 files (19 modified incl. long_headline.png, 14 added incl. breaking_news.png and dark_article.png), +1162/-37, staged by explicit paths only; git diff --cached --check clean; staged diff scanned for private paths/identity/employer/secrets: none. No push, no remote, no hooks (core.hooksPath unset).
Golden hashes verified in worktree, staged index and HEAD blobs: long_headline 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC; breaking_news E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F; dark_article 6FD667E87476F941F7CB7A8152F60FFB8C51A3FD4217A7E993300AB32EB62A96. PNGs untouched.
Docs: baselines/android/pixel10-api37/README.md hash fixed; qa_visual/README.md now uses $RepoRoot=(git rev-parse --show-toplevel) instead of a machine path and states debug-logs/ references are gitignored, local-only. No code/test/threshold/golden change; no scenario run; Metro/Appium/emulator untouched.
Still untracked (intentionally excluded, not deleted): app/.github/, app/.gitleaks.toml, app/.husky/, app/.watchmanconfig, app/CODE_OF_CONDUCT.md, app/Gemfile, app/Gemfile.lock, app/eas.json, app/fastlane/, app/lint-staged.config.ts. Ignored: AGENTS.md/CLAUDE.md (not in repo), .project-private, debug-logs, artifacts.
Next intended task (needs explicit authorization): EXEC-029 no_image, QA-only per approved scope.

## EXEC-029 - no_image implementation and candidate - 2026-11-07
Status: IMPLEMENTATION CHECKPOINT PASS; golden approval PENDING. Start: main f0b38e91724bac180fdcf9b1febd592184f22922, clean except 10 untracked upstream scaffolding entries; 3 golden hashes verified before/after.
Source: app/src/screens/Home/fixtures/qaScenario.ts (QA_NO_IMAGE_SLUG, no_image captureSupported, getQaArticleMedia), qaFeed.ts (qaNoImageArticle: same text, slug qa-no-image, id 910002, _links {}, no imageUrl; selectQaArticle), app/src/components/posts/ArticlePost.tsx (qaMedia contract; image wrapper omitted only for "none"; qa-article-no-image-ready via text onLayout; image-bearing readiness unchanged). Runner: scenario_launch.py allowlist +no_image; ArticleCard(ready_id), NO_IMAGE_READY_ID, image_views_in_card(); HomeScreen.no_image_article_card; new tests/test_no_image.py. Tests: new app/__tests__/screens/Home/qaNoImage.test.ts, app/__tests__/components/posts/ArticlePost.qaNoImage.test.tsx; updated qaScenario.test.ts (no_image active/light; empty_feed still unsupported); Python unit additions in test_scenario_launch_unit.py, test_article_card_unit.py.
Native (same Metro PID26880, Appium 3.3.0, emulator-5554; wrapper debug-logs/exec029/run_visual.py, URL exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=<id>, cmd .venv python -m pytest ./tests/test_<id>.py -m visual -v -s):
- noimg1/noimg2: exit1 ONLY "Golden missing" after all assertions; identity, light theme, exact title, no-image ready, stable bounds [26,837] 1028x711, 0 ImageView in card, no card-ready marker. Sessions ccab49a3-5ea0-45c5-9668-2b7143e728e6, 1a4930a8-4873-4d47-a6ff-0e8682fb8607. Byte-identical, raw 0, max channel 0, comparator 0/730908.
- dark (exit0, 0/1271636), long-after-dark (exit0, 0/1271636), breaking-light (exit0, 0/506804): all actual SHA == approved goldens.
Review packet: debug-logs/exec029/review/ (no_image.candidate.png SHA AC5BD84B93778F4773B3A38ABD391A89483295446A2E096DD59E21CA288B3012, context, metrics.json, repeatability comparison/diff, REVIEW.md). Artifacts qa_visual/artifacts/android/pixel10-api37/exec029-*/.
Checks: pnpm.cmd check:ts exit0; focused Jest 10 suites 94 passed exit0; full Jest 183 suites 1456 passed 3 skipped exit0; pnpm.cmd check exit1 only existing qaFeed.ts:16:11 FIXTUR; pytest -m unit 21 passed exit0; collect 25. git diff --check clean. After native runs, test_no_image.py had a whitespace-only reflow of one assert message (bash heredoc backslash artifact); units/compile rechecked, no native rerun.
Docs: README.md, qa_visual/README.md (no-image section, capture-supported list, scope), docs/ai_prompts_used.md. Nothing staged/committed.
Remaining: golden approval for no_image; empty_feed unsupported; prior risks unchanged (CI/iOS unverified, release runtime unproven, FIXTUR spelling, rounding mechanism).
Next: human review of candidate; promotion only on explicit approval of exact SHA.

## EXEC-030 - no_image golden promotion and regression verification - 2026-11-07
Status: PASS. Start HEAD f0b38e91724bac180fdcf9b1febd592184f22922 with EXEC-029 uncommitted changes; existing 3 golden hashes verified. Candidate debug-logs/exec029/review/no_image.candidate.png verified: SHA AC5BD84B...3012, valid PNG 1028x711 RGBA, byte-equal to both EXEC-029 actuals (runs exec029-noimg1/2, sessions ccab49a3-5ea0-45c5-9668-2b7143e728e6, 1a4930a8-4873-4d47-a6ff-0e8682fb8607, url qa_scenario=no_image, rect x26 y837 1028x711, 0 ImageView, light). Target absent before copy; shutil.copyfile; destination SHA verified.
Native (Metro PID 26880 unchanged, Appium 3.3.0, emulator-5554; wrapper debug-logs/exec030/run_visual.py; URL exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=<id>; cmd qa_visual/.venv python -m pytest ./tests/test_<id>.py -m visual -v -s), order and results (all exit0, 1 passed, actual SHA == golden):
- noimg1 21.21s 0/730908 session 8346f5dc-ca8b-4d2b-bf58-fa97d7680c23
- dark 18.09s 0/1271636; long-after-dark 16.41s 0/1271636; breaking-light 16.32s 0/506804
- noimg2 18.30s 0/730908 session 17691c2d-baba-4800-9679-ad64d190d68c
no_image runs: identity qa-scenario:no_image, ready qa-article-no-image-ready, theme light, exact title, rect [26,837][1054,1548], 0 card ImageViews, card-ready absent. Repeatability: byte-identical, raw 0, max channel 0, tolerance 0/730908 (debug-logs/exec030/repeatability.json, .comparison.json, .diff.png). Artifacts qa_visual/artifacts/android/pixel10-api37/exec030-*/.
Checks: check:ts exit0; focused Jest 10 suites 94 passed exit0; full Jest 183 suites 1456 passed 3 skipped exit0; pnpm check exit1 only qaFeed.ts:16:11 FIXTUR; pytest -m unit 21 passed; collect 25.
Docs: README.md (four scenarios, element vs context capture, no_image approved), qa_visual/README.md (no-image approved section, all-four command loop, scope), qa_visual/baselines/README.md (no_image entry; prior entries now reference checkpoint f0b38e9), qa_visual/baselines/android/pixel10-api37/README.md (four-hash table), docs/ai_prompts_used.md. Nothing staged/committed.
All four hashes final: long 6A9E18DA...C878CC, breaking E552AD4D...38BE7F, dark 6FD667E8...62A96, no_image AC5BD84B...3012.
Remaining: empty_feed (persisted-state leakage, successful-empty readiness); CI/iOS unverified; release runtime unproven; FIXTUR spelling; rounding mechanism; EXEC-029/030 work uncommitted (recommend selective checkpoint).

## PRE-EXEC-031 - Four-scenario Git checkpoint - 2026-11-07
Status: PASS. Commit 8c54f0f711f7b4a78a8a49d25bc1728cc919b002 on main, parent f0b38e91724bac180fdcf9b1febd592184f22922; 18 files (14 M, 4 A: qaNoImage.test.ts, ArticlePost.qaNoImage.test.tsx, test_no_image.py, no_image.png), +528/-44. Explicit-path staging; cached --check clean; sensitive-pattern scan 0 hits; image_diff.py untouched; only PNG staged was no_image.png. Only extra edit: qa_visual/baselines/README.md no_image status line made durable ("human-approved ... promoted byte for byte and verified in EXEC-030"), human-approved.
HEAD blob hashes = worktree = approved: long 6A9E18DA...C878CC, breaking E552AD4D...38BE7F, dark 6FD667E8...62A96, no_image AC5BD84B93778F4773B3A38ABD391A89483295446A2E096DD59E21CA288B3012.
Evidence preserved (not rerun): EXEC-030 two no_image + dark/long/breaking native PASS 0 changed; check:ts 0; Jest 183 suites 1456 passed 3 skipped; pytest unit 21, collect 25; pnpm check FIXTUR-only failure. Provenance in ignored debug-logs/exec029, exec030.
Remaining untracked: only the 10 upstream scaffolding entries (app/.github, .gitleaks.toml, .husky, .watchmanconfig, CODE_OF_CONDUCT.md, Gemfile, Gemfile.lock, eas.json, fastlane, lint-staged.config.ts). No tracked changes.
Limitations: empty_feed unsupported (persisted-state/cache leakage and successful-empty readiness to address); CI/iOS unverified; release runtime unproven; FIXTUR spelling; native rounding mechanism unresolved.
Next: EXEC-031 empty_feed, pending explicit authorization.

## EXEC-031 - empty_feed implementation and candidate - 2026-11-07
Status: IMPLEMENTATION CHECKPOINT PASS; golden approval PENDING.
Start state: HEAD 8c54f0f; clean except the 10 scaffolding entries; four golden hashes verified before and after.

Source changes:
- qaScenario.ts: empty_feed captureSupported.
- qaFeed.ts: outcome record and reset; the empty_feed branch returns [] and records success count 0.
- Feed.tsx: resets the outcome per request; qaEmptyLaidOut state; qa-empty-feed / qa-empty-feed-ready markers plus qa-theme label passed to ListEmptyComponent only in empty_feed under __DEV__.
- EmptyComponent.tsx: optional message-region QA props; collapsable false only when a testID is given.

Runner changes:
- scenario_launch allowlist adds empty_feed.
- New visualqa/components/empty_feed_state.py (EmptyFeedState: ready, theme, message, residue, stable layout, element capture).
- HomeScreen.empty_feed_state.
- New tests/test_empty_feed.py and tests/test_empty_feed_state_unit.py; test_scenario_launch_unit updated.

App test changes:
- New __tests__/screens/Home/qaEmptyFeed.test.ts and Feed.qaEmptyFeed.test.tsx.
- qaScenario.test.ts: empty_feed active/light.
- qaNoImage.test.ts: empty_feed removed from the non-active list.

Native runs (Metro PID 26880 unchanged, Appium 3.3.0, emulator-5554):
- Wrapper: debug-logs/exec031/run_visual.py <scenario> <run>.
- URL: exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=<id>.
- Command: qa_visual/.venv python -m pytest ./tests/test_<id>.py -m visual -v -s.

Isolation sequence:
- iso1-long: exit 0, comparator 0 changed. Actual SHA E3302175...3992; one pixel (743,190) in the cover differs by R+1, within tolerance.
- iso2-empty1: exit 1, Golden missing only.
- iso3-long: exit 0, SHA = golden.
- iso4-empty2: exit 1, Golden missing only.
- Empty runs: identity, light theme, ready, exact message, stable rect [26,825][1054,1134] (1028x309), every residue count 0. Hierarchies contain no QA-FIXTUR/qa-article/qa-breaking entries.
- Sessions: 83b96d99-a2de-4be6-a50e-c4c4ac20f63e and 5f2dc46d-76a4-44da-8a62-416fa4d6e5b2.
- Repeatability: byte-identical; raw 0; max channel 0; comparator 0/317652.

Regressions: reg-long, reg-breaking, reg-dark and reg-noimg all exited 0; every actual SHA equals its golden.

Review packet: debug-logs/exec031/review/
- empty_feed.candidate.png, SHA 903B971081AC2EA2FEB2A37D1B73473602E176A8E9FFE046074E7D3BDE5FA795
- context, metrics.json, repeatability.comparison.json/.diff.png, REVIEW.md
Artifacts: qa_visual/artifacts/android/pixel10-api37/exec031-*/

Checks:
- check:ts exit 0.
- Focused Jest: 11 suites, 69 passed.
- Full Jest: 185 suites, 1471 passed, 3 skipped.
- pnpm check: exit 1, only qaFeed.ts:16:11 FIXTUR.
- pytest -m unit: 29 passed; collect 34.
- git diff --check clean.

Docs: README.md (four approved plus the empty_feed candidate), qa_visual/README.md (empty-feed section, capture-supported text, scope, historical negative-launch note), docs/ai_prompts_used.md. Nothing is staged or committed.

Remaining:
- Golden approval.
- Root README lines 18/20 still say the earlier baselines are "local, uncommitted"; this pre-existing wording is stale.
- Donation card not covered.
- The push-token LogBox toast is visible in context screenshots only.
- CI/iOS unverified; release runtime unproven; FIXTUR spelling; rounding mechanism.

Next: human review of the candidate; promote only on explicit approval of the exact SHA.

## EXEC-032 - empty_feed promotion and five-scenario verification - 2026-11-07
Status: PASS.
Start state: main HEAD 8c54f0f711f7b4a78a8a49d25bc1728cc919b002 with the uncommitted EXEC-031 changes; four golden hashes verified.

Candidate checks (debug-logs/exec031/review/empty_feed.candidate.png):
- SHA 903B9710...A795; valid PNG, 1028x309 RGBA.
- Byte-equal to both EXEC-031 actuals (exec031-iso2-empty1 and iso4-empty2, sessions 83b96d99-... and 5f2dc46d-...).
- capture.json rect x26 y825 1028x309, matching hierarchy bounds [26,825][1054,1134].
- Message text is inside [26,998][1053,1134]; donation text is outside, at [78,1595][1000,1731].

Promotion: target absent before the copy; shutil.copyfile; destination SHA verified.

Native sequence (Metro PID 26880 unchanged, Appium 3.3.0, emulator-5554):
- Wrapper: debug-logs/exec032/run_visual.py.
- URL: exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=<id>.
- Command: qa_visual/.venv python -m pytest ./tests/test_<id>.py -m visual -v -s.
- Order and results (all exit 0, 1 passed, actual SHA = golden):

| Run | Changed pixels | Session |
|---|---|---|
| empty1 | 0/317652 | d9ad1828-1c6a-498b-b27b-8216625b3e7b |
| long | 0/1271636 | |
| breaking | 0/506804 | |
| dark | 0/1271636 | |
| noimg | 0/730908 | |
| empty2 | 0/317652 | eaa2db61-f0dc-4eb3-9355-6114a6d687b7 |

Empty runs: identity, light theme, ready, exact message, rect [26,825][1054,1134], every residue count 0. Hierarchies contain no QA-FIXTUR/qa-article/qa-breaking/qa-theme:dark. The no_image hierarchy after dark has no dark marker.
Repeatability: byte-identical; raw 0; max channel 0; comparator 0/317652.
Evidence: debug-logs/exec032/verification.json, repeatability.comparison.json, repeatability.diff.png, *.out. Artifacts: qa_visual/artifacts/android/pixel10-api37/exec032-*/.

Checks:
- check:ts exit 0.
- Focused Jest: 11 suites, 69 passed.
- Full Jest: 185 suites, 1471 passed, 3 skipped.
- pnpm check: exit 1, only qaFeed.ts:16:11 FIXTUR.
- pytest unit: 29 passed; collect 34.
- git diff --check clean.

Docs:
- README.md: five approved scenarios; stale "local, uncommitted" wording fixed to reference f0b38e9; empty_feed approved, local and uncommitted.
- qa_visual/README.md: approved section, five-scenario loop.
- qa_visual/baselines/README.md: empty_feed entry.
- pixel10 README: five-hash table.
- docs/ai_prompts_used.md.
Nothing is staged or committed.

Final hashes: long 6A9E18DA...C878CC, breaking E552AD4D...38BE7F, dark 6FD667E8...62A96, no_image AC5BD84B...3012, empty_feed 903B9710...A795.

Remaining:
- EXEC-031/032 work uncommitted (recommend a selective checkpoint).
- CI/iOS unverified; release runtime unproven; FIXTUR spelling; rounding mechanism.
- Donation card not covered.
- No demonstrated intentional failing regression.

## PRE-EXEC-033 - Five-scenario Git checkpoint - 2026-11-07
Status: PASS.
Commit bcc56b24dbe67472e178ce27fbab54a442bce482 (bcc56b2) on main, parent 8c54f0f711f7b4a78a8a49d25bc1728cc919b002. 20 files (14 M, 6 A), +724/-31.
Added files: Feed.qaEmptyFeed.test.tsx, qaEmptyFeed.test.ts, empty_feed.png, test_empty_feed.py, test_empty_feed_state_unit.py, empty_feed_state.py.

Staging and scans:
- Staged by explicit path only; cached --check clean.
- Staged blob of empty_feed.png = 903B9710...A795.
- The only PNG in the commit is empty_feed.png; image_diff.py and the four prior goldens are unchanged.
- Sensitive-pattern scan: 0 hits. The only threshold mentions are the existing env defaults 12/0.002 in the new test.
- The first git commit attempt (PowerShell here-string piped to -F -) failed with a pathspec error and created nothing. It was retried with a scratchpad message file.

Docs corrected before staging:
- empty_feed "not yet committed" became "tracked in Git": README.md x2, qa_visual/README.md x2, baselines/README.md x1.
- breaking/long x2/dark "not yet committed" now references f0b38e9 (qa_visual/README.md).
- Root README results line now says three in f0b38e9 and no_image in 8c54f0f.
- Root README "What has been demonstrated" now covers all five scenarios with dimensions and the EXEC-032 six-launch evidence.
- POM description now includes BreakingBanner and EmptyFeedState.
- deliverables/strategy.md untouched.

HEAD blob = worktree = approved hashes:
- long 6A9E18DA...C878CC
- breaking E552AD4D...38BE7F
- dark 6FD667E8...62A96
- no_image AC5BD84B...3012
- empty_feed 903B9710...A795

Evidence preserved, not rerun:
- EXEC-032: six cold launches PASS with 0 changed; two empty_feed actuals byte-identical.
- check:ts 0; Jest 185 suites, 1471 passed, 3 skipped; pytest unit 29, collect 34.
- pnpm check fails only on FIXTUR.

Remaining untracked: only the 10 upstream scaffolding entries. No staged or tracked changes.

Remaining delivery tasks (each needs authorization):
- Final consolidation: deliverables/strategy.md scope (still long_headline-only) and an optional final README pass.
- Optional controlled failing-regression demonstration.
- Limitations: FIXTUR spelling; CI/iOS unverified; release runtime unproven; rounding mechanism; donation card uncovered.

## EXEC-033 - Intentional visual failure demonstration - 2026-11-07 (VERIFIED, uncommitted)
HEAD bcc56b2 at start; five golden hashes verified before and after (unchanged).
New: qa_visual/tests/test_intentional_visual_failure.py, qa_visual/demo_assets/{intentional_mismatch_breaking_news.png, generate_intentional_mismatch.py, README.md}. Modified: qa_visual/pytest.ini (marker + addopts), README.md, qa_visual/README.md, docs/ai_prompts_used.md.
Collection: default 34/35 (1 deselected); -m visual 5; -m unit 29; -m intentional_failure exactly 1. Demo file without -m: 1 deselected, exit 5.
Native (debug-logs/exec033, artifacts exec033-*):
- pass1 breaking_news PASS, 0 changed, actual = golden SHA.
- fail: identity/readiness/title PASS, capture byte-identical to golden; FAILED at test_intentional_visual_failure.py:69, 468349/506804 (92.41%) > 0.2%; exit 1; actual/diff/comparison/context/capture written; no failure-page-source (no Appium/locator failure).
- pass2 breaking_news PASS, 0 changed.
- Suite: long, breaking, dark, no_image, empty all PASS, 0 changed, actuals byte-identical to goldens.
Unit: 29 passed, 6 deselected.
Observation (pre-existing, documented): bare `pytest` without VVP_QA_LAUNCH_URL -> four visual tests fail fast by design; long_headline legacy env fallback runs and fails 11640/1271636 (0.915%). Not caused by EXEC-033.
Next (needs authorization): review/commit EXEC-033; final consolidation incl. deliverables/strategy.md:67 (still says no failing-regression evidence).

## EXEC-034 - Final strategy documentation reconciliation - 2026-11-07 (VERIFIED, uncommitted)
Start: HEAD bcc56b2; EXEC-033 changes uncommitted and preserved.
Changed: deliverables/strategy.md, deliverables/strategy.pdf (SHA AC8564B1727536CC0E7A532B7D6E6A6F874405740A326F3B6582FA950287B8B2, 2 A4 pages, ReportLab 5.1.0 via %TEMP%\exec013-pdf-render-env; builder copy in session scratchpad), README.md (artifacts are git-ignored), qa_visual/README.md (two artifact-availability clarifications), docs/ai_prompts_used.md.
Verification: pypdfium2 opened PDF, 2 pages, metadata title OK, %PDF/%%EOF; both pages rendered at 1.5x and inspected (no clipping/overflow; tables readable); text scan found no employer/private/local-path markers; key evidence strings present.
No app/test/pytest.ini/fixture/threshold/golden changes in EXEC-034. No tests rerun (evidence from EXEC-032/033).
Remaining for human review: commit of EXEC-033 + EXEC-034 changes; FIXTUR spelling; CI/iOS/release runtime unverified; one-pixel layout root cause; donation card uncovered; long_headline legacy env fallback mismatch when run without launch URL.

## EXEC-035 - Self-contained pytest scenario launching - 2026-11-07 (VERIFIED, uncommitted)
Start: HEAD bcc56b2; EXEC-033/034 uncommitted changes present and preserved.
Root cause: visualqa/android.py make_driver() read only VVP_QA_LAUNCH_URL; tests had no way to declare a scenario, four tests pytest.fail()ed without it, long_headline fell back to legacy activate_app (0.915% mismatch).
Change: pytest.ini marker qa_scenario(id); new qa_visual/conftest.py (qa_scenario fixture; root conftest also puts qa_visual on sys.path for IDE runs); scenario_launch.py SUPPORTED_SCENARIOS, build_launch_url, resolve_launch_url (VVP_METRO_HOST/PORT; matching VVP_QA_LAUNCH_URL kept, conflicting -> ValueError before session); android.make_driver(scenario=None) (legacy path kept when no scenario); six tests declare marker and call make_driver(qa_scenario); unconditional terminate in cleanup; 12 new unit tests.
Native (VVP_QA_LAUNCH_URL unset): individually breaking/long/dark/no_image/empty PASS exit 0, 0 changed, actuals = golden SHA; -m visual 5 passed exit 0 (91 s); default `pytest tests -v` 46 passed 1 deselected exit 0; intentional demo FAIL exit 1 at assertion 468349/506804, artifacts new, identity breaking_news; stale URL (long_headline) -> ValueError 0.39 s exit 1; matching URL PASS.
Unit 41 passed; collection default 46/47, visual 5, intentional 1; repo-root cwd run applies pytest.ini and imports.
Hashes unchanged (E552AD4D, 6FD667E8, 903B9710, 6A9E18DA, AC5BD84B; demo A8BBE42E). image_diff.py unchanged; no app diff. git diff --check clean except known PDF trailing whitespace.
Docs: qa_visual/README.md (new self-launching section, PyCharm, overrides, updated commands), README.md quick start, strategy.md line on launching, strategy.pdf regenerated (2 pages, SHA 5346BC39...40A1, both pages inspected), docs/ai_prompts_used.md.
Not done: PyCharm GUI itself not exercised (equivalent CLI runs incl. repo-root cwd). Stop for human review.

## CHECKPOINT-001 - Commit verified EXEC-033/034/035 baseline - 2026-11-07
Commit 2bc313e63d9026cdd8cb448136c7746758fbce94 (parent bcc56b2) "feat(visual-qa): finalize screenshot regression demo and self-launching pytest tests"; lightweight tag visual-qa-baseline-exec035 -> same commit. No push, no remote, no Co-Authored-By trailer.
20 files (explicit paths): .gitattributes (new, `*.pdf binary`; core.autocrlf=true made checkout conversion a corruption risk), README.md, deliverables/strategy.{md,pdf}, docs/ai_prompts_used.md, qa_visual/{README.md,pytest.ini,conftest.py}, visualqa/{android,scenario_launch}.py, six visual/demo tests, test_scenario_launch_unit.py, demo_assets/{README.md,generate_intentional_mismatch.py,intentional_mismatch_breaking_news.png}.
Pre-commit: five golden SHA-256 match baselines README records; demo A8BBE42E...EB3CA; baselines and app/ no diff vs bcc56b2. `pytest tests -v` (no launch URL) 46 passed 1 deselected exit 0; five visual 0 changed pixels. Staged PDF blob SHA 5346BC39...40A1 = inspected file, renders 2 pages. `git diff --cached --check` exit 0; private-marker scan of staged text clean.
Post-commit: tracked tree clean; only the 10 upstream scaffolding entries untracked (untouched). Ignored artifacts/debug-logs/.project-private not committed.
Rollback: `git switch --detach visual-qa-baseline-exec035` (inspect) or, deliberately, `git reset --hard visual-qa-baseline-exec035` on main.
Remaining: FIXTUR spelling; CI/iOS/release runtime unverified; one-pixel layout root cause; donation card uncovered; PyCharm GUI not exercised (CLI-equivalent only).


## EXEC-036 - Golden regeneration/configuration verification - 2026-11-08T00:48:03.068685+01:00
Status: PASS. Initial/final main HEAD 2bc313e63d9026cdd8cb448136c7746758fbce94, tag visual-qa-baseline-exec035. Initially clean tracked tree, ten unrelated upstream untracked entries; preserved. No remote/staging/commit/tag/push.

Read root/app agent instructions, current handoff/decisions, requirements interpretation and original private PDF (pypdfium2 in existing temp render environment; no private text copied), README/strategy, all five tests, conftest/pytest.ini, driver/launcher/POM/comparator/unit coverage and app configuration/ignore rules. Actual source is authoritative. Existing regeneration example was long_headline-specific, unexecuted and lacked programmatic hash validation; replaced with generic documented PowerShell blocks. No source/helper/dependency/configuration changes.

Runtime preflight: emulator-5554 device, boot1, existing tcp8081 reverse; Metro IPv4 /status packager-status:running; Appium /status ready3.3.0. No service restarts or environment changes. No VVP overrides in parent environment. Source pipeline: test marker -> resolved explicit URL -> terminate/deepLink -> exact identity -> component readiness/title/theme/layout -> element screenshot -> context -> comparison; no golden writes. Missing references fail after actual/context, without new diff/metrics. Existing mismatches produce diff/JSON then fail. All five use profile-specific paths; profile does not configure emulator.

Commands (from qa_visual unless stated):
- .\.venv\Scripts\python.exe -m pytest .\tests -v: exit0, 46 passed/1 deselected,96.54s, five independent native captures zero changed. Log debug-logs/exec036/pytest-default.log. After success pytest atexit cleanup logged PermissionError WinError5 for old system-temp pytest-current; not a failing test, no cleanup attempted.
- Exact README capture block extracted/executed: python -m pytest .\tests\test_breaking_news.py -v -s: exit0,1passed17.33s. Scenario identity qa-scenario:breaking_news, exact title, measured readiness and containment verified; rect x26,y720,w1028,h493. Session5bb8e7af-5dd6-4bf4-b077-ca2ab7f1d36a vs suite81a8c1b5-204f-421e-9fe0-c7d65501ac5b. Candidate/context/diff inspected: complete border, four-line title, no clipping; context Firebase warning outside banner. Native PNG1028x493RGBA, SHA E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F.
- .\.venv\Scripts\python.exe -m pytest -m unit -q --basetemp=artifacts/exec036-unit-temp: exit0,41passed6deselected0.91s, clean.
- pytest --collect-only -q: exit0,46/47 selected1deselected. Repo-root cwd breaking file collection: exit0,1collected (IDE-style imports; GUI not exercised).
- README promotion block extracted into ignored rehearsal; only target assignment redirected to ignored temporary-reference.png and scripted Read-Host answers. Wrong hash/decline absent/decline existing reject; absent authorized copy succeeds; existing differing demo reference backs up then replaces; existing backup refuses repeat. Exit0. Candidate/destination hash exact; backup A8BBE42E...EB3CA. No real reference targeted; scripted PROMOTE authorizes only this rehearsal, not a real golden.
- python -m visualqa.image_diff --baseline ../debug-logs/exec036/rehearsal/temporary-reference.png --actual artifacts/review/3436b549-0afa-4757-bb82-7936c10f3fc2/breaking_news.actual.png --diff ../debug-logs/exec036/rehearsal/verification.diff.png --result-json ../debug-logs/exec036/rehearsal/verification.comparison.json: exit0,0/506804.
- Same comparator with demo_assets/intentional_mismatch_breaking_news.png: expected exit1,468349/506804=92.412254%. Native intentional pytest not rerun; default exclusion and unchanged demo/comparator verified.

Evidence: debug-logs/exec036/initial.json, verification.json, candidates.json, suite/* (all five fresh captures/context/diff/metrics and capture metadata where supported), rehearsal.log, rehearsal/*, capture-readme.log, capture-location.json, unit.log, collection.log. Review packet qa_visual/artifacts/review/3436b549-0afa-4757-bb82-7936c10f3fc2/. All ignored. All candidate pixels/hash equal their current golden; long/dark1028x1237,breaking1028x493,no_image1028x711,empty1028x309. No candidate approved/promoted.

Before/after six reference hashes match worktree and HEAD; full values in initial.json/verification.json. Comparator12/0.002 unchanged; no app,fixture,test,launcher,threshold,reference,demonstration asset or strategy changes. git diff --check exit0;17 README relative links/anchors verified.

Configuration decision: no Python dotenv loading/example/dependency needed. Optional process environment works locally and can be injected by future CI. Full URL overrides host/port but must match test marker. Profile whitelist validated, numeric tolerance parsing/ranges validated after capture. Host/port/endpoint/package not comprehensively validated early. Tolerance env variables affect four normal tests, not breaking or demo; leave unset. App .env.sample safe APP/telemetry template; Expo loader leaves inherited process values intact. APP default volksverpetzer but unknown values select Mimikama. EXPO_PUBLIC_QA_SCENARIO is client-bundled dev fallback, URL takes precedence, none disables it; not secret. QA gate/theme state unchanged. Real .env/.env.*, private/docs/logs/artifacts/credentials ignored; reviewed templates excepted. No secrets printed.

Modified tracked docs only: README.md,qa_visual/README.md,docs/ai_prompts_used.md. Private02/03/04 appended. No additional example/helper; manual hash+confirmation commands sufficient and rehearsed. Strategy current, no PDF regeneration needed. Existing ten scaffolding entries untouched. Minor inspection hiccups: PowerShell brace-glob syntax rejected then corrected; pypdf unavailable, existing pypdfium2 used; one installed-package rg path absent, actual Expo loader inspected. No installation.

Remaining: partial endpoint validation/tolerance asymmetry; old temp cleanup warning; CI/iOS/PyCharm GUI/release runtime unverified; known FIXTUR spelling and native rounding root cause unchanged. Await human review; do not start EXEC-037 automatically.


## EXEC-037 - Framework organization and maintainability - 2026-11-08T01:20:10+01:00
Status: PASS; uncommitted. Start/final main HEAD 09fc21a9bede9cfa1df76d58d17e0802b7466c67. Initially clean tracked tree; ten unrelated app scaffolding entries preserved. No staging, commit, tag, remote or service startup changes.
Plan recorded before source changes: separate five unit files; one root pytest.ini for both working directories; extract paths/artifacts/comparison and session lifecycle; retain scenario assertions and POM; no new lint dependency.
Baseline: pytest -v --basetemp=artifacts/exec037-before-temp, exit0,46passed1deselected96.09s; five comparisons0pixels. Emulator already online; Metro IPv4 packager-status:running, Appium3.3.0ready. No VVP_QA_LAUNCH_URL/profile/tolerance overrides set.
Implementation: moved five *_unit.py files byte-equivalent (UTF-8 contents verified) to unit_tests; moved pytest.ini to repo root, testpaths=qa_visual/unit_tests qa_visual/tests,pythonpath=qa_visual. qa_scenario fixture typed and misleading sys.path docstring corrected. android_session context manager preserves diagnostics/terminate/finally quit. VisualArtifacts centralizes profile validation, unchanged filenames, context/hierarchy/metadata writing and comparator calls. Six tests retain every UI assertion (AST checked), fixture constants unchanged; tests still own native element capture and final assertion. Nine new unit cases cover invalid profiles, missing reference safety, explicit override policy, artifact names and cleanup on failure.
Style: consistent imports and annotated shared interfaces; multiline metadata and readable test functions. Ruff absent; evaluated/deferred to avoid new dependencies or mass formatting. Untouched POM/comparator/launcher retained. Breaking/demo use fixed defaults because historical tests called compare_png directly; no product rationale found. Four others retain explicit env overrides; future unification requires review. No policy change.
Verification (full commands/logs/metrics in debug-logs/exec037):
- unit-directory: `-m pytest unit_tests/ -v --basetemp=artifacts/exec037-unit-directory-temp` (qa_visual cwd), exit 0.
- unit-marker: `-m pytest -m unit -q --basetemp=artifacts/exec037-unit-marker-temp` (qa_visual cwd), exit 0.
- visual-directory: `-m pytest tests/ -v --basetemp=artifacts/exec037-visual-directory-temp` (qa_visual cwd), exit 0.
- visual-marker: `-m pytest -m visual -v --basetemp=artifacts/exec037-visual-marker-temp` (qa_visual cwd), exit 0.
- default: `-m pytest -v --basetemp=artifacts/exec037-default-temp` (qa_visual cwd), exit 0.
- individual: `-m pytest tests/test_dark_article.py::test_dark_article_android_card_matches_reviewed_golden -v --basetemp=artifacts/exec037-individual-temp` (qa_visual cwd), exit 0.
- intentional: `-m pytest tests/test_intentional_visual_failure.py -m intentional_failure -v -s --basetemp=artifacts/exec037-intentional-temp` (qa_visual cwd), exit 1.
Results: unit-directory50pass; unit-marker50pass6deselected; visual-directory5pass1deselected93.55s; visual-marker5pass51deselected93.42s; default55pass1deselected95.78s; individual dark function1pass18.85s; intentional1failed17.08s at actual result.passed assertion,468349/506804=92.412254%,exit1.
All normal visual comparisons0changed/0ratio, actual PNGs valid RGBA and expected dimensions: long/dark1028x1237,breaking1028x493,no_image1028x711,empty1028x309. Original actual/context/diff/JSON conventions retained; per-run snapshots in visual-directory/,visual-marker/,default/,individual/,intentional/ under debug-logs/exec037. Comparison thresholds12/0.002. No golden writes.
Collection both root and qa cwd55/56selected1deselected; root unit50,visual5,intentional1,individual1,all exit0. Existing root-cwd unit execution50pass. Direct PyCharm node selection supported by equivalent CLI and root import checks; GUI not operated. All six protected SHA-256 values equal preflight and HEAD; references-before/after.json contains full hashes. App,fixture,POM,scenario launch,comparator,strategy Markdown/PDF unchanged. git diff --check exit0 (only informational LF->CRLF notices). Initial/final ten app untracked entries identical; private/log evidence ignored. One read-only assertion inspection initially used Windows default encoding, then passed with explicit UTF-8; no test or source defect.
Docs: root/runner README updated for paths, commands, shared responsibilities, conventions and preserved tolerance asymmetry. EXEC-036 regeneration/configuration sections preserved verbatim. Public prompt record updated; no private brief copied. No strategy/PDF update needed.
Remaining: PyCharm GUI/CI/iOS unverified; intentional tolerance asymmetry unchanged; known app FIXTUR spelling/native rounding/donation limitations untouched. Await review; do not begin EXEC-038 or commit.


## EXEC-037 bounded remediation - primary exception preservation - 2026-11-08T01:47:41+01:00
Status: PASS, uncommitted. Start/final main HEAD09fc21a9bede9cfa1df76d58d17e0802b7466c67. Prior EXEC-037 unstaged changes and ten unrelated app scaffolding entries preserved.
Audit correction: previous test named preserves_failure actually EXPECTED diagnostic error masking. The old inline cleanup and refactored context manager both allowed diagnostic/terminate/quit errors to replace primary failures. Earlier verification of cleanup did not prove preservation.
Changes only within this remediation: visualqa/android.py, unit_tests/test_visual_check_unit.py, qa_visual/README.md, docs/ai_prompts_used.md and private handoff/prompt records. _cleanup_driver attempts termination then quit; first cleanup failure propagates if no prior error, subsequent ones are attached using exception notes with formatted secondary tracebacks. android_session captures a BaseException, attempts diagnostics and cleanup, then bare-reraises the exact original object/traceback. BaseException includes pytest failure outcomes and interruptions. make_driver uses the same preservation after a usable driver exists, including the legacy launch failure branch (now also attempts termination). Remote construction failure still propagates without nonexistent-driver cleanup. save_diagnostics and visual/comparison code unchanged.
Unit coverage: body success/failure; diagnostics/termination/quit individually and together; actual diagnostic mkdir filesystem failure; exact object identity and original traceback-frame retention; secondary traceback notes; call counts/order; pytest.fail/KeyboardInterrupt; real factory flow with mocked Remote creation failure and runtime/legacy launch failure, plus cleanup failures.
Commands/results:
- From repo root: qa_visual/.venv/Scripts/python.exe -m pytest qa_visual/unit_tests/test_visual_check_unit.py -k 'session or make_driver' -vv --basetemp=qa_visual/artifacts/exec037-remediation-focused: exit0,22passed5deselected0.42s.
- From qa_visual: .venv/Scripts/python.exe -m pytest unit_tests/ -q --basetemp=artifacts/exec037-remediation-units: exit0,68passed1.01s.
- Same interpreter: -m pytest --collect-only -q: exit0,73/74collected1deselected0.53s. Collection, not a combined default execution.
- -m pytest tests/ -m visual -v --basetemp=artifacts/exec037-remediation-visual-temp: exit0,5passed1deselected93.62s.
- -m pytest tests/test_intentional_visual_failure.py -m intentional_failure -v -s --basetemp=artifacts/exec037-remediation-intentional-temp: expected exit1,1failed17.70s at result.passed;468349/506804changed,ratio0.9241225404692939.
Runtime: existing emulator-5554online,MetroIPv4packager-status:running,Appium3.3.0ready; no service startup/restarts. All normal comparison metrics0pixels/0ratio; valid PNGs long/dark1028x1237,breaking1028x493,no_image1028x711,empty1028x309. Actual/context/diff/JSON conventions unchanged; per-run copies/logs/commands/results in debug-logs/exec037-remediation. All6referenceSHA256 equal preflight and HEAD (reference-hashes.json). Thresholds12/0.002 unchanged.
Final checks: git diff --check exit0 (informational LF->CRLF notices only). No app,fixture,reference,POM,launcher,comparator,visual-test,dependency,strategy changes during remediation. Previously approved EXEC-037 working files preserved except the scoped edits. No staging/commit/tag/push.
Limitations: cleanup attempts cannot ensure a disconnected/unresponsive server actually releases resources; existing driver timeouts apply. If Remote fails before returning a usable driver, this code cannot clean an unknown server-side session. Existing save_diagnostics may stop collecting after a filesystem error, now recorded as a note on the original failure. No broader diagnostic redesign. Ready for human review/commit authorization; do not start EXEC-038.


## EXEC-037 final commit - 2026-11-08T01:55:18+01:00
Human approved the refactor and exception-preservation remediation. Created local main commit 5a0f2f0026763b437118759b70c64e708e3d3901, parent 09fc21a9bede9cfa1df76d58d17e0802b7466c67, message: refactor(visual-qa): organize tests and harden session lifecycle. No Co-Authored-By trailer, amend, new/moved tag, remote or push.
Reviewed complete working diff and new files; staged explicit 25-path allowlist (19 changes with rename detection), including five exact unit relocations and root pytest.ini move. Staged name-status/full-diff content check, sensitive-pattern scan and cached --check passed. Text-only scope; no app,fixture,golden,demonstration image,generated artifact,private file or scaffolding included. No active Git hooks found.
Post-commit parent/message/file inventory verified; six reference hashes match original and committed blobs; tracked tree/index clean; exactly ten prior app scaffolding entries remain untracked. Tag visual-qa-baseline-exec035 remains2bc313e. Prior evidence retained:22focused/68totalunits PASS,73normaltests collected,5nativePASS0pixels,intentional comparatorFAILexit1. Tests not repeated for commit-only operation.
Private handoff/prompt record appended after commit and remain ignored. Stop; EXEC-038 requires separate authorization.


## EXEC-038 - Allure visual test reporting - 2026-11-08
Status: PASS with caveat; uncommitted. Start/final main HEAD 5a0f2f0; ten app scaffolding entries preserved. No stage/commit/tag/push.
Changes: qa_visual/requirements.txt (+allure-pytest==2.16.2); new visualqa/allure_report.py; visual_check.py (started_ns field, attach calls in compare()); conftest.py autouse fixture (labels, current-run failure diagnostics); unit_tests/test_allure_report_unit.py (6 tests); READMEs and docs/ai_prompts_used.md. No app/fixture/golden/threshold/launcher/comparator/test-file change.
Allure CLI 2.36.0 (Report 2, npm global; Java 17). Output dirs artifacts/allure-results|allure-report|junit (ignored); separate normal/visual/individual/intentional-failure.
Final runs (debug-logs/exec038/final-*): units 74 pass; default 79 pass 1 deselected 77.6s; -m visual 5 pass 0 px each; individual breaking_news pass; intentional fails genuinely 468349/506804; HTML for 4 report dirs generated and inspected in headless Chrome (screenshots allure-*.png); attachments byte-matched to goldens/artifacts; six reference hashes + demo reference equal HEAD.
CAVEAT: earlier runs on a slow emulator state (~180s suite) failed dark_article 11147px and long_headline 11640px (~1px fixture image shift); reproduced on stashed EXEC-037 code; later runs 0 px. Root cause (emulator state) unproven; no golden/threshold change. Evidence: dark_first_failure.*, earlier runs in debug-logs/exec038.
Side effects: I started Appium (was down) and stopped it afterwards; accidental `allure serve --help` server stopped. Limitations: CI, iOS, Allure 3, PyCharm GUI unverified; pre-capture failure attachment covered by unit tests only. Await review; do not start EXEC-039 or commit.


## EXEC-038 report inspection and commit - 2026-11-08
Browser inspection (headless Chrome via Selenium, reports served from artifacts/allure-report by local http.server, then stopped; no artifact regenerated, no test changed):
- visual report, long_headline (passed): golden, actual, diff PNGs expanded in the Allure UI, each natural width 1028 and rendering correctly; directly opened files also render; comparison JSON readable (changed_pixels 0, passed true); parameters readable (scenario, profile, pixels, ratio, thresholds). Screenshots: debug-logs/exec038/ui-v-*.png, ui-v-all.png, v-long-*.png.
- intentional-failure report: status Failed; suite "Intentional reference-mismatch demonstration (not an app regression)"; tags, description; incorrect reference (blue), actual (red) and diff images render; JSON shows 468349/506804, passed false. Screenshots: ui-i-*.png, ui-i-all.png, i-*-file.png.
- My first guessed attachment deep-link URLs returned Allure "Not found"; a wrong guess, not a report defect.
Unresolved stability observation (no confirmed cause): two intermittent ~1px fixture-image-shift mismatches, dark_article 11147px and long_headline 11640px, in early EXEC-038 runs; dark_article reproduced on stashed EXEC-037 code; later full runs 0px. Logs: debug-logs/exec038/dark_first_failure.{actual.png,diff.png,comparison.json}, final-*.comparison.json, final-default.log, final-visual.log, final-individual.log, final-intentional.log, appium.log. Emulator degradation is a hypothesis only (the early runs were slower), not confirmed.

EXEC-038 commit: local main 7d8c7f1709c6ffac85f5911c6de429f0bd8d8992, parent 5a0f2f0, message "feat(visual-qa): add Allure visual regression reporting", no trailer/amend/tag/push. 8 files (6 modified, 2 new) staged by explicit path. NOTE: `git diff --cached --check` reported "qa_visual/visualqa/allure_report.py:97: new blank line at EOF"; commit proceeded anyway (checks were not chained). Trivial whitespace defect remains in the commit; fix needs a separate authorized commit or amend. Ten app scaffolding entries still untracked.

EXEC-038 commit amended (human-authorized, whitespace only): original 7d8c7f1709c6ffac85f5911c6de429f0bd8d8992 -> replacement dfe9b16eb4a803f0bc994d962d13c8f5ccdc36f9, parent 5a0f2f0 unchanged, message unchanged, no trailer. Reason: git diff --cached --check had flagged trailing blank lines at EOF of qa_visual/visualqa/allure_report.py in the original commit; only those two blank lines were removed, no functional change. git show --format= --check HEAD passes. Android tests not rerun (whitespace only). Original commit was unpushed/untagged. No tag/push; ten app scaffolding entries still untracked. EXEC-039 not started.


## EXEC-039 - Screenshot reproducibility investigation - 2026-11-08
Status: investigation complete, no fix implemented; nothing staged/committed. HEAD dfe9b16; ten app entries untouched. Evidence: debug-logs/exec039/ (SUMMARY.md, runs.tsv, per-run dirs, analysis/analyze.py, run_matrix.sh, invalid-concurrent-launch/).
Findings: (1) Archived EXEC-038 dark mismatch (11147 px): all changes in image band y29-527; text region y>=527 = 0 changes; sub-pixel anti-aliasing differences on the image edges (golden blended rows y29/497/526; actual hard edges) => image rendered at a fractional offset (~0.5px vertical), not layout/crop shift; container rect identical (26,720,1028x1237). Same pixel counts (11147/11640) repeated across ~10 runs/sessions incl. unmodified EXEC-037 code => a persistent alternate rendering state, not a per-capture race. (2) Mismatches and ~2x slower runs (36s vs 16s/test) all occurred within ~20 min after the emulator cold boot (10:09:48); clean thereafter. Temporal correlation only. (3) Clean matrix: 15 runs, 1 Appium socket hang up (dark-4), 0 visual mismatches, Allure on/off identical, durations equal. (4) long_headline shows rare 1-level single-pixel variants in the image band (2/9).
Mistake: my first matrix launch ran twice concurrently (unreliable ps check on Windows); discarded as invalid, re-run once with a lock. Appium started by me and stopped afterwards.
Not changed: app, fixtures, goldens, thresholds, tests, Appium lifecycle, Allure. Await human review; do not start EXEC-040.


## EXEC-039 cold-boot probe - 2026-11-08
Status: complete, read-only, nothing staged/committed. HEAD dfe9b16; ten app entries untouched. Evidence: debug-logs/exec039/cold-boot/ (cold_boot_probe.sh, runs.tsv, boot-method.txt, boot-timeline.txt, appium.log, per-run dirs with actual/diff/json/capture/hierarchy/pytest/appium slice/top).
Method: adb emu kill; emulator.exe -avd Pixel_10 -no-snapshot-load -gpu software (t0 2026-11-08T11:34:34+01:00, identical flags to the earlier instance, i.e. a genuine cold boot with software GPU); boot_completed +30s; Appium+Metro ready +52s; adb reverse 8081 re-added. Startup load average was 13 at +54s.
Results: 14 runs (dark/long at +54-113s, +425-483s, +1202-1258s, +1804-1825s): all PASS 0 px, 0 transport failures; 12 byte-identical; 2 long_headline captures (B-long-2, D-long-1) carry the known 1-level single-pixel variant (743,190). No dex2oat processes observed at any run start. Element geometry identical (dark hierarchy bounds and capture rect constant).
Hypothesis: boot-state/warm-up NOT reproduced, so timing correlation lost support; still unresolved, not contradicted (one cold boot only). Differences from the EXEC-038 failing period remain unidentified. Appium stopped by script; emulator left running; no code/golden/threshold/Allure changes. Await review; do not start EXEC-040.


## EXEC-040 - Housekeeping, pytest matrix verification, pre-publication audit - 2026-11-08
Status: complete; uncommitted. HEAD dfe9b16; ten app entries untouched. Nothing staged/committed/tagged/pushed; no history rewrite, remote, or publication.
Housekeeping: removed tracked docs/ai_prompts_used.md; moved ignored docs/AGENT_TASK_HISTORY.md to .project-private/archive/ (private, not deleted); removed empty docs/; removed its .gitignore entry and the README link; AGENTS.md (local, gitignored; CLAUDE.md imports it) repo map now points at deliverables/ and forbids recreating either file; prompts go to 04_AI_PROMPT_LOG.md only. OUTSTANDING (not done): human-compiled, human-reviewed AI prompt disclosure for the employer submission (requirement R11 in 01_REQUIREMENTS.md); the removed public file must not be presented as complete.
Pytest matrix (evidence debug-logs/exec040/): c1 `-m visual` FIRST execution exit1 2 failed 3 passed 185s (dark 11147px, long 11640px: the same counts as EXEC-038; artifacts not archived - my script lapse; only log counts survive); c1 re-run 5 passed 79.9s exit0 0px (c1-rerun/); c2 `-m "visual or intentional_failure"` 5 passed 1 failed 127.1s exit1 (Allure six-visual); c3 default 79 passed 1 deselected 84.2s exit0; c4 `-m "unit or visual or intentional_failure"` 79 passed 1 failed 96.5s exit1. Allure six-visual HTML opened in headless Chrome: 5 passed / 1 failed in two suites, attachments present (allure-six-suites.png). qa_visual/README.md has the verified matrix and a recurrence note.
Stability: third occurrence (EXEC-038, EXEC-040 first run; EXEC-039 cold boot did not reproduce). Identical pixel counts each time = persistent alternate image rendering state lasting one run set, with ~2x slower runs. Unresolved; no cause claimed. Candidates not yet tested: image cache state, host contention.
Pre-publication audit (current tracked + 9-commit history, no remote/tags except visual-qa-baseline-exec035): no employer name, challenge PDF, secrets (only a test placeholder token), absolute machine paths or private/handoff/agent files in any revision; strategy.pdf is own deliverable (metadata clean). Findings: (1) history still contains docs/ai_prompts_used.md (8 commits) - sanitized, no employer terms, but partial; (2) all 9 commits authored with a personal Gmail address; (3) generic wording "challenge"/"challenge-scoped" in README, qa_visual docs, strategy.md signals an assignment (no names); (4) ten untracked upstream app/ files (.github workflows/deploy, fastlane, eas.json...) need an explicit include/exclude decision; (5) upstream MIT + brand assets (Volksverpetzer/Mimikama) need attribution review; (6) AGENTS.md/CLAUDE.md are gitignored so they are not in the repo.
Not changed: app, fixtures, tests, visualqa, goldens (all six hashes equal HEAD), thresholds, Allure. Await review; no EXEC-041.


## EXEC-040B - Failure evidence retention + publication readiness - 2026-11-08
Status: complete; uncommitted (EXEC-040 changes preserved). HEAD dfe9b16; ten app entries untouched; nothing staged/committed/tagged; no remote/push/history change.
Code: new qa_visual/visualqa/failure_evidence.py (retain(): unique dir artifacts/android/<profile>/failures/<UTC>-<scenario>-<pid>/ with reference/actual/diff/comparison/capture/hierarchy/context/failure-* (current-run files only via started_ns), manifest.json (reason, node id, times, Appium session id, comparison, platform/python, VVP_* env, sha256s, collection_problems); never raises, warns instead); visual_check.py calls it on failed comparison and missing golden (assertions/semantics/thresholds untouched); 7 new unit tests (81 unit total). README documents it. Allure code unchanged; .project-private archive of AGENT_TASK_HISTORY.md deleted.
Live evidence (debug-logs/exec040b/): L1 intentional exit1 -> complete package (6 files + manifest; no hierarchy because that test writes none; 468349/506804). L2 default+Allure: 2 failed 84 passed 178s: MISMATCH RECURRED (dark 11147, long 11640) and was auto-retained (packages ...dark_article-35416, ...long_headline-35416). Retained dark actual.png is BYTE-IDENTICAL (sha256 41b83cc7f762...) to EXEC-038 dark_first_failure.actual.png; same change bands (image band y29-527 only, text region 0). => discrete repeatable alternate image rendering, not noise. L3 intentional again: 4 packages exist, earlier ones intact after later runs. L4 default+Allure: 1 failed 85 passed 107s; the failure was a UIA2 transport error on the first test after fresh Appium start ("Timed out waiting for the root AccessibilityNodeInfo"), non-visual, correctly no package. Six goldens unchanged; no app/test/threshold changes.
Pattern note (unproven): the three visual-mismatch episodes (EXEC-038, EXEC-040 c1, EXEC-040B L2) were the first full-suite runs after a fresh Appium start and ran ~2x slower; EXEC-039 individual-run matrices and cold boot after fresh Appium start did not reproduce, and UIA2 transport errors also cluster at fresh starts. Candidate to test next: first suite after a fresh Appium/UIA2 server vs. image alt state. No cause claimed.
Audit: gitleaks 8.30.1 (portable zip downloaded to scratchpad, SHA-256 matched release checksums file), `gitleaks git --redact` (9 commits, all refs) and `gitleaks dir` on a copy of the 539 tracked working-tree files: 1 finding, same in both: app/config/volksverpetzer.config.ts:19 Algolia searchKey, present verbatim in the public upstream commit 8b42175 (public client-side search key by design; ACL not verified). Untracked files and ignored/private dirs not scanned (by design); default rules only (repo-root .gitleaks.toml absent). Details: debug-logs/exec040b/gitleaks/ (redacted JSON).
Untracked app/ classification: .github (13 files; upstream deploy/release workflows needing upstream secrets, FUNDING.yml with upstream links) = unnecessary, EXCLUDE; .gitleaks.toml (default upstream config) = optional, exclude; .husky (pre-commit lint-staged) = optional, exclude; .watchmanconfig = optional, harmless; CODE_OF_CONDUCT.md (upstream contact app@volksverpetzer.de) = unnecessary, exclude; Gemfile/Gemfile.lock (fastlane Ruby) = unnecessary; fastlane/ (47 files, ~1MB, store metadata/changelogs) = unnecessary, exclude; eas.json = optional (tracked package.json scripts dev:android/preview etc. reference EAS profiles; `pnpm android` = expo run:android does not need it); lint-staged.config.ts = optional (paired with husky). Recommended minimum: exclude all, or include only eas.json if dangling script references matter.
Licensing: app/LICENSE.md = MIT (c) 2026 Volksverpetzer VVP gUG - confirms rights to the code only. Unresolved: no explicit grant for logos/mascot/Rive/webp brand assets (volksverpetzer, mimikama, faktenbot*.riv, logo_*), FUNDING/donation links, Mimikama (separate organization) config/images. Minimum: keep LICENSE.md + README attribution, add a short NOTICE/README statement that upstream trademarks/brand assets remain property of their owners and are included only for the demo, confirm permission or replace/remove Mimikama assets (not needed for the QA scenarios, APP defaults to volksverpetzer), keep the pinned upstream commit reference.
History/publication: 9 commits, 1 tag (visual-qa-baseline-exec035), no remote; all authored with personal Gmail; partial docs/ai_prompts_used.md remains in 8 commits (no employer terms; incomplete disclosure); generic "challenge"/"challenge-scoped" wording in README/qa README/baselines README/strategy.md (no employer name); no employer PDF, handoff/agent files or absolute machine paths in any revision. Recommendation: a private remote is fine with current history; for a PUBLIC repo prefer a clean history (squash/new repo from the final tree, noreply author email, no prompt-file history) or rewrite with filter tooling after human decision; do not rewrite without approval.
Fresh-clone: public READMEs give emulator/Metro/Appium/venv/test commands (PowerShell/Windows only); gaps: `pnpm install`/app dev-build prerequisites only partly covered, no macOS/Linux commands, AGENTS.md/CLAUDE.md are gitignored (a fresh clone has no agent guidance) - recommend a short sanitized tracked AGENTS.md (no .project-private/handoff/challenge wording) + 2-line CLAUDE.md.
Outstanding: human-reviewed AI prompt disclosure. Await review; do not start EXEC-041.


## EXEC-040C - Publication finalization - 2026-11-08
Status: complete; uncommitted (EXEC-040/040B work preserved). HEAD dfe9b16, branch main. Nothing staged/committed/tagged; no remote/push/history change; ten app/ entries untouched and excluded.
Approved decisions applied: private first remote; keep 9-commit history/authors; exclude all ten untracked upstream app files; AGENTS.md/CLAUDE.md/.project-private stay ignored and private; no public agent instructions; "challenge" wording unchanged; no further instability investigation; goldens/fixtures/thresholds/retries unchanged.
EXEC-040C changes: README.md (+ "Setup from a fresh checkout" table with verified vs not-verified status, link to NOTICE.md, MIT-does-not-cover-brand-assets sentence; Documentation link), qa_visual/README.md (emulator launch flags used by verified runs; GPU/launch flags at golden capture were not recorded; recurrence note incl. no_image 710 vs 711 px), new NOTICE.md (provenance, MIT retained in app/LICENSE.md, brand-asset limitation, permissions unresolved, golden images contain only synthetic content - verified visually). Nothing deleted/replaced among app assets.
Brand assets: Volksverpetzer icons/splash/notification, shop/steady/paypal buttons, einhorn, logo_pike, logo_animated, welcome, 404, success, 3 FaktenBot Rive files; Mimikama variant: 5 images + config (not used by tests, APP defaults to volksverpetzer). fixture-cover.png added by this project. All referenced by app code (rive via FaktenBot component).
Algolia finding (value not recorded here): app/config/volksverpetzer.config.ts:19 `searchKey`, consumed only by @algolia/client-search in src/screens/Search/components/AlgoliaSearch.tsx (client-side; necessarily shipped inside the app bundle) and present in the public upstream commit 8b42175. Assessment: intended public client-side search key. NOT verified: its Algolia ACL/restrictions (no request made with it). Recommend: keep, add gitleaks allowlist/note if CI scan is added; optionally ask upstream to confirm it is search-only. Re-scan: gitleaks 8.30.1 `gitleaks dir` on 542 files (tracked + the 3 new untracked non-app files, copied to scratchpad): same single finding. History scan from EXEC-040B unchanged (no new commits).
Verification (debug-logs/exec040c/): units `pytest -m unit -q` exit 0, 81 passed 6 deselected; default `pytest -v` exit 1, 3 failed 83 passed 1 deselected, 186s (fresh Appium, 32-39s/test): dark_article 11147px, long_headline 11640px (byte-identical actual.png to the EXEC-038/040B captures, same bands) and NEW no_image: card height 710 vs 711 (size mismatch, total changed). All 3 auto-retained as packages ...dark_article-10224, ...long_headline-10224, ...no_image-10224 under qa_visual/artifacts/android/pixel10-api37/failures/ (7 packages total). Not retried, no golden/threshold change. Pattern: 4th episode = first full suite after fresh Appium start, ~2x slower; alternate state now also alters element geometry. git diff --check clean; links resolve; goldens/app/tests unchanged.
Repo content checks: 540 tracked; none of AGENTS/CLAUDE/.project-private/debug-logs/handoff/artifacts/venv/node_modules/.github/fastlane/husky tracked; only PDF = deliverables/strategy.pdf (own deliverable); docs/ absent; required files tracked (fixtures, 5 goldens + demo reference, tests, requirements, pytest.ini, LICENSE, fixture-cover.png). WARNING: the ten app/ entries are untracked but NOT ignored, so `git add -A`/`git add .` would pick them up (incl. upstream deploy workflows). Stage by explicit path, or add them to .git/info/exclude (local only) - not done.
Proposed commits: (1) feat(visual-qa): retain evidence for failed visual comparisons = visualqa/failure_evidence.py, visualqa/visual_check.py, unit_tests/test_failure_evidence_unit.py, qa_visual/README.md; (2) chore: remove discontinued prompt/history documents = .gitignore, delete docs/ai_prompts_used.md, README.md link-removal hunk; (3) docs: add fresh-clone setup and provenance notice = NOTICE.md + remaining README.md hunks. README.md hunks interleave (2)/(3): split with git apply --cached or accept README.md in (3) with (2) leaving a stale link for one commit.
Remaining blockers to a private remote: none technical. Decisions/risks still open: brand-asset permissions (limitation documented), history keeps partial prompt file and personal email (accepted for private), instability unresolved (gate non-blocking), human AI-prompt disclosure outstanding. Await review; no EXEC-041.


## EXEC-040D - Housekeeping commits - 2026-11-08
Status: PASS. Two local commits on main, no amend/tag/remote/push, explicit-path staging only, no trailer (consistent with project history).
1. ce09b5e833af22557ad4bfe61124634c686cea1c (parent dfe9b16) "feat(visual-qa): retain failed comparison evidence": qa_visual/visualqa/failure_evidence.py (new), visualqa/visual_check.py, unit_tests/test_failure_evidence_unit.py (new), qa_visual/README.md.
2. 0e7b206 (full SHA: `git rev-parse 0e7b206`; parent ce09b5e) "docs: consolidate setup, attribution and housekeeping": .gitignore, README.md, NOTICE.md (new), deleted docs/ai_prompts_used.md.
Checks: cached --check passed before each commit; `git show --format= --check` passed for both; six reference hashes unchanged; unit `pytest -m unit -q` exit 0, 81 passed 6 deselected 2.33s; visual suite NOT rerun; known failed-suite evidence retained (debug-logs/exec040b, exec040c; qa_visual/artifacts/.../failures/, 7 packages). Final status: clean tracked tree; ten app/ entries untracked/intact; AGENTS.md, CLAUDE.md, .project-private ignored; docs/ absent; tag visual-qa-baseline-exec035 only; no remote.
Carry-forward risks: 4 episodes of visual instability (first-full-suite-after-fresh-Appium correlation, unconfirmed; no_image 710 vs 711 geometry variant); UIA2 transport failures; visual CI advisory-only initially; brand-asset permissions unresolved (NOTICE.md); human AI-prompt disclosure outstanding; ten app/ entries are untracked-but-not-ignored (stage by path only).
Blockers to first private push: none technical.


## EXEC-040E - Pytest discovery hardening - 2026-11-08
Status: PASS; one local commit (hash in `git log -1`), message "fix(pytest): restrict test discovery to test directories"; files: pytest.ini, qa_visual/README.md. No push/tag/remote/amend.
Root cause: `testpaths` in the root pytest.ini applies only when pytest runs from the rootdir. From qa_visual/ no-arg runs recursed through all of qa_visual/, incl. artifacts/ (6,230 paths in artifacts/ considered, 1.6s collection), exposing PermissionError risk on unreadable temp dirs; `pytest tests ...` avoided it. The eight PermissionErrors did NOT reproduce here (walk of artifacts/: 0 unreadable dirs), so the mechanism is established, the specific errors are not reproduced.
Fix: norecursedirs = pytest defaults + artifacts baselines demo_assets visualqa (setting it replaces defaults, so repeated). After: 44 paths considered, 0 entered in artifacts/, 0.35s; selection identical from root and qa_visual (86 normal of 87; 5 visual; 81 unit).
Cache warning: not reproducible; root .pytest_cache is writable (write test ok), no warning in any run today, no cache_dir configured by the project; earlier runs used -p no:cacheprovider. Cause therefore local filesystem/session permissions rather than project config (unproven for the original session). Documented in qa_visual/README.md with -p no:cacheprovider workaround.
Verification from qa_visual/: `pytest --collect-only -m visual -q` exit 0, 5/87 selected; `pytest -m unit -q` exit 0, 81 passed 6 deselected 1.59s; `pytest -m visual -v` exit 0, 5 passed 82 deselected 86.6s (87s wall), no new failure packages, no PermissionError/cache warning. Evidence: debug-logs/exec040e/. Goldens unchanged; git diff --check clean. Historical artifacts/evidence untouched; ten app/ entries intact. Appium started for the run and stopped.
Note: this visual run passed (no instability episode this time).


## EXEC-041 - Excluded app/ entries dependency review + clean tracked-only build - 2026-11-08
Status: complete, read-only for the repo (no staging/commits/tags/remote; Git tracking and ignore rules unchanged; no goldens/fixtures/thresholds touched; ten app/ entries intact; six reference hashes unchanged). HEAD 8ed5ac2.
Clean-checkout validation: `git archive HEAD | tar -x -C D:\cc` (tracked files only, all ten entries absent, no .env). In D:\cc\app: `pnpm install --frozen-lockfile` rc0 14s (husky prepare ran harmlessly with no .husky); `pnpm check:ts` rc0 11s; `pnpm exec expo config --type public` rc0 (resolves without eas.json; package de.volksverpetzer.app, v2.5.5); `expo prebuild --platform android --no-install` rc0 5s; `gradlew.bat assembleDebug -PreactNativeArchitectures=x86_64` BUILD SUCCESSFUL 3m54s -> app-debug.apk (de.volksverpetzer.app, 130 MB, sha256 768e0c26b40ff763...). Logs debug-logs/exec041/. NOT verified: installing/running that APK (would replace the verified installed dev build; deliberately skipped), `pnpm android`/expo run:android end to end, Appium tests against the clean-built APK, cold-network/cold-cache build (pnpm store + Gradle caches were warm), other ABIs, EAS builds, iOS, macOS/Linux.
Findings: app/.github is nested, so GitHub would never run its workflows (root .github only; they also use ./.github/actions relative paths); secrets they need: EXPO_TOKEN, PLAY_SERVICE_ACCOUNT_JSON, BUNNY_*, CODECOV_TOKEN, GITLEAKS_LICENSE; deploy-web on push to prerelease. fastlane/ is read only by scripts/prepare-*.mjs (release/store metadata; src/constants/Changelog.ts is tracked generated output, so runtime/build do not need fastlane). eas.json is used only by EAS scripts in package.json (android:local, dev:*, preview:*), the app README's EAS dev-build docs and a comment in app.config.ts; not needed for prebuild/gradle. husky/lint-staged: package.json prepare + devDependency; hook inactive here (core.hooksPath unset). Left D:\cc (~size in MB above) in place: my rm -rf was blocked by the safety check (and was unnecessary); delete it manually when convenient.
Recommendations: all ten Keep excluded; eas.json Defer until a workflow needs EAS; husky + lint-staged.config.ts only as a pair, defer; .github/.gitleaks.toml defer until our own root workflows exist. Tracked repo is sufficient for the planned local-gradle Android Appium pipeline. Minimum before first push: nothing required for these entries; stage by explicit path (untracked-not-ignored) or add them to .git/info/exclude.

## EXEC-042A - GitHub Actions Android build CI - 2026-11-08
Added .github/workflows/android-build.yml (workflow_dispatch only, ubuntu-24.04, permissions contents:read, 45 min timeout, Temurin Java 17, Node from app/.nvmrc (24), pnpm from packageManager (12.11.2), action versions pinned to commit SHAs: checkout v7.0.1, setup-java v6.2.0, setup-node v7.1.0, pnpm/action-setup v6.1.1, upload-artifact v7.0.2). Steps: pnpm install --frozen-lockfile; expo prebuild --platform android --no-install; ./gradlew assembleDebug -PreactNativeArchitectures=x86_64; verify app/android/app/build/outputs/apk/debug/app-debug.apk; upload artifact android-debug-apk-x86_64 (7 days). README section added. Verified locally only: YAML parse, paths/scripts exist, git diff --check, no qa_visual change. GitHub-hosted execution NOT verified. A remote 'origin' (private repo URL) now exists; nothing pushed. Commit "ci(android): add GitHub Actions debug APK build" (no trailer, consistent with earlier history).

## EXEC-042A-R1 - runner disk-space remediation - 2026-11-08
First GitHub run failed after ~25m27s in Gradle (x86_64 native/CMake): "No space left on device" (also in runner _diag log). Consumers unmeasured. Added .github/scripts/disk-report.sh (df -h/-i, avail, du -sh on known paths) run at 4 checkpoints (job start, after cleanup, before Gradle, after Gradle with !cancelled()), and a narrow cleanup step right after checkout (before toolchain setup) removing only existing non-symlink dirs /usr/share/dotnet /opt/ghc /usr/local/.ghcup /usr/local/share/boost /opt/hostedtoolcache/CodeQL /usr/share/swift, printing size and reclaimed MiB. Android SDK/NDK, hostedtoolcache otherwise, Java/Node/pnpm untouched. Build commands unchanged; no caching added. Verified locally: YAML parse, step order, bash -n, diff --check, qa_visual untouched. NOT verified on GitHub. Commit "ci(android): mitigate GitHub runner disk exhaustion".

## EXEC-042B - advisory emulator visual CI - 2026-11-08
Commit 1639858 "ci(visual): add advisory Android emulator screenshot tests" (parent 38fb58d; build run #2 had passed in 33m38s, 27 GB free before / 13 GB after Gradle). Workflow gained job visual-tests (needs build-debug-apk, ubuntu-24.04, 60 min): download android-debug-apk-x86_64, KVM check (fail clearly if absent, no fallback), Java17/pnpm/Node24/Python3.13, pip requirements, pnpm install (Metro only; no prebuild/Gradle), Appium 3.3.0 + uiautomator2 7.1.2, AVD Pixel_10 from system-images;android-37.0;google_apis_playstore_ps16k;x86_64 forced to 1080x2424/420dpi/4 GB RAM, -no-window -no-snapshot -gpu swiftshader_indirect, install APK, Metro expo start --dev-client --localhost --port 8081 + adb reverse, Appium on 4723, bounded readiness checks, bundle warm-up, app-launch check. Test step: python -m pytest -m visual -v (+ --alluredir/--junitxml), continue-on-error so rc stays visible; summary script classifies comparison mismatch vs other/infrastructure vs not executed. Artifacts: visual-evidence, visual-allure-results, visual-allure-report (best effort), visual-infra-logs. Scripts in .github/scripts. Local env differences vs goldens: Linux host, emulator build/image revision may differ (local emulator 36.5.10, image rev 3), swiftshader_indirect vs -gpu software, fastboot cold boot. Verified locally only: YAML parse, script syntax, summary script with synthetic JUnit, pytest collects exactly 5 visual tests, goldens unchanged. NOT run on GitHub.

## EXEC-042B-R1 - separate visual workflow with APK reuse - 2026-11-08
Commit 18db02a "ci(visual): reuse APK from previous build workflow" (parent 1639858, not amended). android-build.yml restored byte-identical to 38fb58d (one job build-debug-apk, disk cleanup/reports intact). New .github/workflows/android-visual-tests.yml: workflow_dispatch, required input source_run_id, permissions contents:read + actions:read, single job visual-tests (no needs, no prebuild/Gradle), checkout fetch-depth 0, .github/scripts/check_source_run.py (numeric id; run in this repo; workflow path android-build.yml; completed+success; artifact android-debug-apk-x86_64 exists, unexpired, non-empty; source sha ancestor of GITHUB_SHA; reject if app/ (non-.md), qa_visual baselines/demo_assets/visualqa/tests/conftest/requirements, pytest.ini changed), then download-artifact v8.0.2 with run-id/repository/github-token, SHA-256 + emulator/Appium provenance in summary. Emulator/Appium/Metro/pytest/Allure steps and four artifacts moved unchanged from 1639858. Local checks: YAML, shell/py syntax, synthetic accept/reject cases, real repo diffs (eca3aa4 and 38fb58d compatible with HEAD; 5a0f2f0 rejected), goldens unchanged. NOT run on GitHub; gh API field names (run.path, artifacts expired/expires_at) unverified live.

## EXEC-042C - emulator provisioning + bounded diagnostics - 2026-11-08
First GitHub run of android-visual-tests.yml (source APK from build run) passed source validation, download and Appium setup, then failed at "Setup 4/5": emulator binary: libpulse.so.0 missing; avdmanager: "No device found matching --device pixel_10" and pixel_9. Then "Collect final logs" ran >12 min until cancelled. Root cause (assessment): hosted Ubuntu 24.04 image lacks libpulse0 and its cmdline-tools lack those hardware profiles; the hang's exact command is unconfirmed - candidates: adb daemon spawned inside a redirected/captured step, adb with no device, unbounded du in disk-report.sh. Old script also hid errors (fallback chain, `| tail`, no pipefail, `emulator -version ... || true`).
Fix (commit "ci(visual): fix emulator provisioning and bounded diagnostics"): new install-emulator-deps.sh (apt libpulse0, bounded, verified via ldconfig) as step 4a before boot; start-emulator.sh rewritten with pipefail: logs avdmanager list device, creates AVD WITHOUT --device (display forced to 1080x2424/420 via config.ini), verifies system.img, emulator runs, ldd of qemu, config.ini and avd list, detects emulator death, adb start-server redirected; new collect-final-logs.sh: every command under timeout (10 s adb, 90 s disk report), adb devices to file then device check via awk, explanatory note if no device, always exit 0; step timeout-minutes 4. disk-report.sh unchanged (shared with build). Mock tests: hanging adb, no device, logcat hang, disk timeout, AVD/image/emulator failure paths. Unverified on GitHub: that avdmanager accepts no --device, libpulse0 is the only missing lib, emulator boots with KVM, Appium/dev-client/pytest stages never reached yet. Rerun: same source_run_id (artifact expires 7 days after its upload).

## EXEC-042D - false-positive QEMU ldd preflight - 2026-11-08
Second GitHub visual run: packages/system image installed, `emulator -version` OK (37.2.13.0), then start-emulator.sh aborted ("unresolved shared libraries listed above") because bare `ldd` on emulator/qemu/linux-x86_64/qemu-system-x86_64* showed bundled Android Emulator libs "not found". Root cause: my preflight ran ldd without the launcher's library search path (the emulator launcher sets it), so a healthy install looked broken. Fix (commit "ci(visual): make QEMU ldd preflight informational"): ldd now informational only (bare and approximate-LD_LIBRARY_PATH output to emulator-ldd.txt, never fails); real failures still caught: emulator -version must run, system image, AVD creation/verification, emulator process death now reports exit status, tail of emulator.log and an explicit error for "error while loading shared libraries", 420 s boot timeout, adb device, 1080x2424/420 checks. libpulse0 step, final-log collection, APK/source validation, build workflow, qa_visual, app unchanged. Mock tests: launch failure (ldd "not found" present) reaches launch and fails with status 127 + log; mock successful boot passes. Unverified: real AVD creation without --device, emulator boot with KVM, everything after. Rerun with source_run_id 42494990156 (while artifact is unexpired).

## EXEC-042E - KVM preflight reliability - 2026-11-08
Evidence: a visual run failed at "Check KVM acceleration" almost immediately; the failure branch's `ls -l /dev/kvm` showed `crw-rw-rw- root kvm 10,232`, i.e. the device existed with world rw by the time of the listing, yet the shell checks (-c/-r/-w) had failed just before. Earlier visual runs passed the step. Commit comparison 18db02a/f47a4fa/21f9b1f: enable-kvm.sh byte-identical, step/order/runner/permissions/env identical; later changes only after the KVM step. Root cause UNCONFIRMED. Leading hypothesis only: asynchronous `udevadm trigger` applied the 0666 mode after the shell checks ran but before `ls` (no settle). Others open: runner-specific virtualization, shell test misreport.
Fix (commit "ci(visual): improve KVM preflight reliability"): enable-kvm.sh now prints diagnostics before/after (image, id, uname, cpu flag count, ls/stat, exists/-c/-r/-w results separately), applies the same minimal udev rule, `udevadm settle --timeout=10` under `timeout 15` (warning only), then decides by kvm_check.py (20 s timeout): stat, open O_RDWR, ioctl KVM_GET_API_VERSION must equal 12; codes 10 missing, 11 not char dev, 12 access denied, 13 open failed, 14 ioctl failed, 15 unexpected version, timeout -> error. Shell -r/-w are diagnostics only. No retries, no fallback; workflow YAML unchanged. Local validation: mocked/injected for 12-15 and success; real for missing (10), regular file (11); real WSL /dev/kvm (crw-rw---- root:kvm, user not in kvm group) -> code 12 correctly; shell wrapper with fake python (pass, deny, hang->20 s). Success path with a real ioctl NOT exercised. GitHub-only risks: whether KVM works on that VM, udev settle effect, real ioctl value. Rerun visual workflow with source_run_id 42494990156 (if artifact unexpired).

## EXEC-042F - noninteractive AVD creation - 2026-11-08
GitHub run: KVM preflight passed (EXEC-042E), emulator 37.2.13.0, API 37 image installed, 66 device definitions, then avdmanager printed "Do you wish to create a custom hardware profile? [no]" and $HOME/.android/avd/Pixel_10.avd/config.ini did not exist. The create call had used `<<< "no"`; since the script reached "AVD not created" it had returned success without creating. Exact root cause UNCONFIRMED (why the here-string answer was not honoured / where avdmanager wrote). Fix (commit "ci(visual): make AVD creation noninteractive and verified"): `printf 'no\n' | timeout -k5 300 avdmanager create avd -n Pixel_10 -k <image> --force` (still no --device), avdmanager's own status via PIPESTATUS (124 = timeout), full output in avdmanager-create.log, config.ini location taken from `avdmanager list avd` Path (fallback ANDROID_AVD_HOME or ~/.android/avd), config existence and list check, output dumped on any failure. Display/RAM/cold-boot config, KVM, libpulse, log collection unchanged. Mock tests (stdin receives "no" and AVD created -> full mock boot passes; exit 3 fails; exit 0 without config fails; hang -> 124 timeout error). Unverified on GitHub: real avdmanager behaviour, emulator boot, Appium/Metro/pytest stages. Rerun with source_run_id 42494990156 if unexpired.

## EXEC-042G - AVD directory mismatch - 2026-11-08
GitHub run: KVM passed; AVD created (log: /home/runner/.config/.android/avd/Pixel_10.avd/config.ini, 1080x2424, 420, 4096 MB, API 37) but emulator exited 1: "Unknown AVD name [Pixel_10] ... no file Pixel_10.ini in $HOME/.android/avd". Cause: avdmanager and the emulator launcher resolve the default AVD home differently on the runner (exact env reason not examined). Fix (commit "ci(visual): pin ANDROID_AVD_HOME for AVD creation and discovery"): start-emulator.sh exports ANDROID_AVD_HOME=${RUNNER_TEMP:-/tmp}/android-avd before create/list/emulator -list-avds and the nohup emulator launch (inherited); logs HOME/ANDROID_USER_HOME/XDG_CONFIG_HOME; verifies Pixel_10.avd/config.ini, Pixel_10.ini, ini path= equals the AVD dir, avdmanager list avd shows Pixel_10, `emulator -list-avds` lists Pixel_10 (all before launch, with dumps of output and AVD home on failure). printf 'no' answer, PIPESTATUS/timeout handling, boot/death/display checks unchanged. Mock tests: success (mismatched defaults, launch env shows pinned home), avdmanager ignoring env, missing ini, wrong ini path, emulator not listing. Unverified on GitHub: real emulator boot onward. Rerun with source_run_id 42494990156 if unexpired.

## EXEC-042H - ADB authentication - 2026-11-08
GitHub run: all setup reached the emulator launch; emulator.log: "Failed to open /home/runner/.android/adbkey", "adbkey generation failed", "No adb private key exists", later "Boot completed in 118960 ms"; adb reported "device unauthorized" for the whole wait and the script failed with sys.boot_completed not 1 within 420 s. Established: no host key existed/could be created. NOT established: why the emulator's own generation failed (leading guess only: ~/.android absent/unwritable; the AVD had landed under ~/.config/.android so Android config dirs differ on the runner).
Fix (commit "ci(visual): initialize ADB authentication before emulator boot"): new init-adb-auth.sh (logs user/HOME/adb version; fails if ANDROID_USER_HOME/ANDROID_SDK_HOME point elsewhere; requires `adb keygen`; mkdir 700; reuses a non-empty existing pair else `timeout 30 adb keygen $HOME/.android/adbkey`; verifies both non-empty, chmod 600/644, prints type/owner/mode/size only, never contents). start-emulator.sh now: unsets ANDROID_USER_HOME/ANDROID_SDK_HOME (logged), runs init script, `adb kill-server` + `start-server` once after key creation, then launches the emulator (ANDROID_AVD_HOME pin retained); boot loop polls `adb devices` state (absent/offline/unauthorized/device), logs transitions only, queries sys.boot_completed only in state device, distinct final errors per state, same 420 s limit (BOOT_TIMEOUT/POLL_INTERVAL env overrides for tests only). No ADB_VENDOR_KEYS, no auth bypass, no repository/secret keys; key lives in ~/.android on the ephemeral runner, not in LOG_DIR/artifacts.
Mock validation: keygen missing/existing/failing/empty/unsupported, mismatched ANDROID_USER_HOME, uncreatable dir (real Linux perms via WSL: key 600, dir 700), order keygen -> kill-server -> start-server -> emulator launch, state sequences incl. success, persistent unauthorized/offline/absent, device-but-not-booted, getprop never called outside state device, no secret strings in output. Real emulator/adb on Linux NOT exercised. GitHub-only unknowns: whether adb on the runner honours ~/.android/adbkey after unsetting overrides, whether the emulator then authorizes it, subsequent Appium/Metro/pytest stages. Rerun with source_run_id 42494990156 if unexpired.

## EXEC-042I - API 37 AVD metadata + emulator stability - 2026-11-08
Verified GitHub timeline (UTC, 2026-11-08): 19:38:29 adb authorized, boot_completed=1, APK install started; 19:38:34 surfaceflinger "Assertion failed: !rcEnc->featureInfo()->hasReadColorBufferDma" then SIGABRT (RegionSampling thread, mapper.ranchu.so); 19:38:36-37 surfaceflinger and system_server died; install failed "Failure calling service package: Broken pipe (32)". Also low-memory kills, CPU contention, SystemUI ANR, 2 emulator cores, host disk 6.4 GB free/92% used. Causality strongly suspected, not proven.
External lead (hypothesis): https://github.com/actions/runner-images/issues/14484 - older Command-line Tools write target=android-0 for android-37.0 AVDs; CLI 22.0 fixes metadata and crash. Our runner's CLI version and AVD target are UNKNOWN (android-0 NOT observed by us).
Change (commit "ci(visual): validate API 37 AVD and emulator stability"): start-emulator.sh logs ANDROID_HOME/JAVA_HOME/java, PATH vs invoked sdkmanager/avdmanager, versions, installed packages; after AVD creation requires Pixel_10.ini target=android-37.0 and config.ini image.sysdir.1=system-images/android-37.0/google_apis_playstore_ps16k/x86_64 (observed values printed; never hand-patched). Conditional CLI: if metadata wrong and invoked CLI is not 22.0 -> install cmdline-tools;22.0 (bounded), select any cmdline-tools/* dir whose sdkmanager reports 22.0 (covers latest-2), recreate AVD with that avdmanager, re-verify, else fail; if metadata already correct nothing is reinstalled. New post-boot-health.sh (45 s window, 5 s poll, called at end of start-emulator.sh): emulator pid alive, adb state device, surfaceflinger and system_server pidof present and unchanged (1 transient adb error tolerated, 2 fail), `cmd package list packages` answers (timeout/failure fail), logcat since gate start scanned for hasReadColorBufferDma / surfaceflinger fatal signal; evidence file health/health-failure.txt; logcat never cleared. New install-apk.sh replaces the plain `adb install -r -g` (same command, 300 s bound): pre-install adb state, pm responsiveness, APK size+sha256, host df, guest /data df, MemAvailable; on failure keeps exit status and writes install-failure.txt (state, sf/system_server pids, pm, filtered logcat). Workflow change: only that one install line. Unchanged: build workflow, ADB auth, KVM, libpulse, AVD pin, display/RAM/flags, APK reuse, tests.
Validation (mocks only; no real emulator): CLI/target cases (correct, android-0 -> 22.0 -> accept, persistent android-0, 22.0 already in use, missing, wrong API, image path mismatch, 22.0 install not found), gate cases (healthy 6 polls, sf/system_server restart, missing, offline/unauthorized/absent, pm timeout/fail, logcat signature, transient tolerance, emulator exit), install cases (success, rc 32, timeout 124). Test-only env overrides: HEALTH_SECONDS/INTERVAL, QUERY_TIMEOUT, INSTALL_TIMEOUT.
Unverified live: runner CLI version/target, whether 22.0 fixes the crash, whether memory/CPU (2 cores, low-mem kills) alone destabilize the guest, health-gate signature wording on real logs. Next: rerun visual workflow with source_run_id 42494990156 (if unexpired); inspect "Command-line Tools diagnostics" group, "AVD metadata" lines, health gate result, health/ and install/ files in visual-infra-logs.

## EXEC-042J - scenario activation diagnostics + native crash triage - 2026-11-09
Evidence (local only, .local-evidence/exec-042j/, ignored via root .gitignore `**/.local-evidence/`; extracted copies in the session scratchpad, not the repo): analysis md (secondary) + visual-allure-report.zip, visual-allure-results.zip, visual-infra-logs_3.zip (pytest/junit/allure JSON, appium.log, metro.log, logcat-tail.txt covering 20:13:40-20:15:25 only, environment, health, install logs).
Confirmed: 5/5 visual tests TimeoutException "qa-scenario:<id> was not exposed" inside make_driver before yield; no screenshots/hierarchy existed for that path. Deep link reached MainActivity (shell START, then dev-launcher re-START from the app uid), JS "Running main" ~10 s after the deep link (long_headline 20:13:54), Metro served bundles. During long_headline (pid 7449) Glide loaded assets/images/qa/fixture-cover.png at 20:13:57 - only rendered when qaFixtureEnabled -> strong (not conclusive) indication the QA selection was ACTIVE and the fixture rendered, i.e. the failure is likely marker exposure/finding by UiAutomator2 (6 "ByMatcher: Node returned null child" warnings) or an overlay, NOT URL parsing. No crash in the long_headline window. Native crash separately confirmed for no_image: 20:14:48.240 SIGSEGV SEGV_ACCERR tid mqt_v_js pid 7761, "trying to execute non-executable memory", MountingCoordinator::pullTransaction / FabricUIManagerBinding::schedulerDidFinishTransaction, ~1 s after Running "main"; page size 16384; CI fingerprint .../CE2A.260420.051.A2/16418371 vs local .../CP21.260306.017.A1/15087165 (different API 37 image builds); RN 0.86.3, expo 57.0.30, expo-router 57.0.28, react-native-screens 4.26.2, reanimated 4.5.1, gesture-handler 2.32.0, Fabric on. Cause unknown; not shown to cause the other four failures. Not reproduced locally (not attempted beyond the passing run). Analysis-doc discrepancy: none material; it did not mention the fixture-cover load implication or the image-build difference.
Path traced: Appium mobile:deepLink -> am start VIEW exp+vvpapp://expo-development-client/?url=...&qa_scenario=<id> -> MainActivity (dev launcher) -> Linking.getInitialURL() -> app/src/screens/Home/fixtures/qaScenario.ts resolveQaSelection (searchParams "qa_scenario") / initializeQaScenario -> QaLaunchGate.tsx renders 1x1 accessible View accessibilityLabel qa-scenario:<id>; +native-intent.tsx routes to /home. Locally (real emulator, today) the new JS log shows: initial URL exp+vvpapp://expo-development-client/ qa_scenario=["breaking_news"] -> status=active ... and "marker rendered"; breaking_news PASSED (23.9 s). So the URL contract works locally with the same URL shape.
Changes (commit "test(visual): diagnose scenario activation failures"): qa_visual/visualqa/launch_diagnostics.py (bounded capture before session cleanup: Appium screenshot -> adb screencap fallback, page source -> uiautomator dump fallback, query_app_state, pidof, dumpsys window/activity focus, filtered bounded logcat, sanitized URL, original exception; classification app-process-absent / dev-client-screen / wrong-marker / marker-present / qa-selection-rejected / error-overlay / other-app-foreground / crash-signature / hierarchy-unavailable / marker-absent-unknown-screen; diagnostic-errors.txt; never raises; note added to the original exception); android.make_driver(diagnostics_dir) + android_session passes <artifacts>/launch-diagnostics/<scenario>/; allure_report.attach_launch_diagnostics; app QA-only console.info of sanitized initial URL + selection and "marker rendered"; workflow input visual_scope (all|breaking_news) validated by .github/scripts/visual-scope.sh before setup (fails job if invalid), EXPECTED_VISUAL from it; README lines; .gitignore (user edit) committed.
Verification: unit 101 passed (19+1 new); jest 24 suites/184 tests passed (qaScenario incl. new describeQaLaunchUrl tests, QaLaunchGate, native-intent, qa fixtures); pnpm check:ts rc 0; eslint/prettier problem counts on touched app files equal to HEAD (pre-existing style debt, none added); bash -n, YAML, git diff --check ok; goldens/thresholds/build workflow/APK contract/emulator scripts unchanged. REAL local emulator (Pixel_10 API 37, local Metro, Appium 3.3.0): breaking_news PASSED; forced failure via VVP_METRO_PORT=8099 -> FAILED with real failure-screen.png (dev-client "There was a problem loading the project"), hierarchy, app-state (DevLauncherErrorActivity), logcat, classification dev-client-screen; Allure raw JSON referenced 5 attachments, all files present; generated HTML report contains them. Evidence under debug-logs/exec042j (ignored).
APK: no native change; existing APK is technically compatible, BUT the committed compatibility check (check_source_run.py, approved contract) rejects source run 42494990156 because app/ (non-md) and qa_visual/visualqa/ changed -> a new "Android debug build" run is required before the visual run (or a separately approved change to the contract). Next: push after review; run build; then visual workflow with new source_run_id and visual_scope=breaking_news; read launch-context.txt classification + failure-screen.png + "[qa-scenario]" lines in logcat.txt.

## EXEC-042K - Expo developer-menu dismissal before scenario checks (local commit; see git log, starting 27abb47)
Evidence (original visual-evidence.zip, not just the analysis): CI breaking_news run (APK build run 42602902168) failed with the Expo onboarding bottom sheet ("This is the developer menu...", Runtime version: exposdk:57.0.0, Close, Continue) covering the running app; app hierarchy exposed only that sheet (a11y-window-id 12), so qa-scenario:breaking_news was invisible although JS logged status=active + marker rendered. Evidence zips remain untouched in .local-evidence/.
Change: new qa_visual/visualqa/expo_overlay.py (hierarchy-only recognition via ElementTree; onboarding = onboarding text + Continue TextView + (runtime version or Close); dev-menu panel = runtime version + Close + >=2 panel labels (Go home/Reload/TOOLS/Fast Refresh/Open DevTools); no coordinates, no generic Continue/Close). Click only when exactly one Continue (or Close) control with a clickable parent exists, via XPath element click; wait <=8 s for that variant to disappear; no second click. scenario_launch.wait_for_scenario_identity (used by launch and by tests) now polls the exact marker every 0.5 s (45 s unchanged), probes the overlay at most every 1.5 s (late overlays handled), dismisses at most once per variant (onboarding, then the panel it opens), extends the wait by <=10 s total, and still requires the exact marker. Ambiguous/click-failure/still-visible/reappeared -> ExpoOverlayError (WebDriverException) with notes; launch_diagnostics (EXEC-042J path) captures it; new classification expo-dev-menu-overlay; launch-context.txt gains "expo overlay evidence". Timeout after dismissal keeps the original message plus a note with the dismissal report.
Local real finding: after `adb shell pm clear de.volksverpetzer.app` the first launch reproduced the onboarding. Continue opens the full dev-menu PANEL (Close, no Continue), so dismissal is two-stage; first attempt (before two-stage fix) failed with "still visible" and also showed the old classifier mislabelled the panel as error-overlay (fixed). After the fix: pm clear -> breaking_news PASSED against the unchanged golden (21 s), repeat run PASSED (19 s, overlay absent). Data of the app was cleared once on the local emulator; it self-restores (onboarding done), no other restoration needed.
Verification: unit tests 129 passed (.venv Scripts python), incl. 29 new expo-overlay tests (mocked clock/driver); pytest collects exactly 5 visual tests; goldens/thresholds/fixtures/workflows/scripts untouched; git diff --cached --check clean.
APK compatibility: check_source_run.incompatible_changes rejects the three qa_visual/visualqa files changed here -> run 42602902168 (built before) is REJECTED by the unchanged rule; a fresh "Android debug build" is required before the next visual run. (Technically the APK is unchanged.) gh CLI unavailable locally so the run's headSha was not queried.
Unresolved: CI-only confirmation (first-launch onboarding in the CI image), whether the other four scenarios/no_image SIGSEGV are affected (separate, not investigated).

## EXEC-042L - isolated no_image crash reproduction (start d48e8d7, local commit only)
Context: latest full-suite GitHub run (APK build 42616325655 from d48e8d7): breaking_news, dark_article, empty_feed, long_headline PASSED with 0 changed pixels (real golden comparisons); no_image FAILED in scenario initialization (native SIGSEGV/SEGV_ACCERR on mqt_v_js, libreactnative.so MountingCoordinator::pullTransaction, 16 KB pages, ~17:38:51 UTC 2026-11-09; no active/marker log lines; launcher foreground; Expo overlay not detected). Earlier full-suite run had a similar crash. Fixture-specific vs order/lifecycle/image/resource causes: UNPROVEN. Evidence zips in .local-evidence/exec-042k/ (untouched).
Change: visual_scope gains `no_image` -> tests/test_no_image.py::test_no_image_android_card_matches_reviewed_golden (expected 1); allowlist case in .github/scripts/visual-scope.sh, workflow choice option, README line; default `all` unchanged (5). collect-final-logs.sh additionally writes ci-logs/logcat-crash.txt (`logcat -b crash -d -t 1000`, timeout-bounded, script still exits 0). No tombstone/root access attempted. No visualqa/app/golden/threshold/emulator changes.
Verification (local, scripts only): visual-scope.sh for all/breaking_news/no_image writes correct env; injection string and empty value rejected rc=1; pytest collects the node (1 test) and 5 visual tests overall; collect-final-logs with fake adb produces logcat-crash.txt and rc 0, and with a failing adb still rc 0; bash -n and YAML parse OK; git diff --check clean. Not run on GitHub; does not reproduce the crash.
APK compatibility: check_source_run.incompatible_changes([...4 changed paths]) == [] (workflow, scripts, README not monitored) -> build 42616325655 (built from d48e8d7, which is the current visualqa state) is eligible; artifact expiry ~2026-11-16, verify on the run.
Next: push, run "Android visual tests (advisory)" with source_run_id=42616325655, visual_scope=no_image. Classify pass / native crash / other / infra separately.

## EVAL-001 - final deliverable audit and closure (HEAD at start 79126a9)
See .project-private/docs/09_EVAL_001_CLOSURE.md (audit R01-R12, findings, evidence index, walkthrough, Q&A). Changes: strategy.md/pdf updated to hosted-CI evidence (3 pages), stale "no CI" README statements corrected, deliverables/ai_prompt_disclosure.md DRAFT added (human compiles the final). Development frozen; no tests run, no APK rebuilt.

## README-003 - Consolidated demo README - 2026-11-11
Status: complete, uncommitted; branch main, HEAD 52ef3b836deb458c53d1878b5ab4316139a973ea unchanged. Root README now 204 lines with nine approved sections; nested qa_visual/README.md removed after transferring setup, run, golden approval, artifacts/Allure, CI evidence and limitations. Four links in three retained Markdown guides now resolve to root anchors. No helper/framework contract discrepancy found: all five fixed pytest nodes, accepted JUnit class names, comparison fields and retention fields match sources and available recorded JUnit.
Verification: inline read-only link/anchor + AST/node/hash checker passed (14 local links/anchors, tracked Markdown references, nine sections, five nodes); PowerShell offline safety suite rerun: 50 cases passed. git diff --check passed (only LF-to-CRLF informational warnings); five golden SHA-256s and all three helper hashes unchanged. No native runs/services/build/install/CI/remote access. App, runner, fixtures, goldens, thresholds, workflows and deliverables unchanged. Tracked delta exactly README.md, deletion qa_visual/README.md, and cross-reference edits in qa_visual/baselines/README.md, qa_visual/baselines/android/pixel10-api37/README.md, qa_visual/demo_assets/README.md. Ten original app entries and README-002 scripts remain untracked; nothing staged/committed/tagged/pushed. Private handoff/prompt log updated only locally.
Carry-forward: full clean-host onboarding and actual ADB/native helper capture unverified; hosted no_image crash unresolved, suite not green; brand-asset rights unresolved; human AI disclosure remains outstanding. Candidate review required before any documentation commit. No further task started.

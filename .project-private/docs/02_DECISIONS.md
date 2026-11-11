> **CURRENT STATUS (2026-11-01): The human has approved `vvp_app` + the test-only fixture fetcher + Appium/pytest + one Android scenario. Phase is EXECUTION. Older OPEN statements below are historical; see the latest section at the bottom.**

# Decision log — short architecture decision records

> **Latest human direction (2026-11-01): prioritize `vvp_app` for the authorized, bounded PLANNING feasibility spike.** Earlier JetNews-first recommendations below are retained as historical research, not the active priority. SUT, mocking, runner and CI implementation decisions remain **OPEN**.

**As of 2026-11-01:** PLANNING. User authorized a bounded test-only fixture implementation feasibility spike; final SUT, mock architecture, runner and CI implementation are **OPEN**. This is not execution-phase sign-off.

## Decision policy

- **Tier A — human approval:** SUT, mock seam, main testing approach, major scope/tool pivot, paid service, hand-in claims.
- **Tier B — decide pragmatically + log briefly:** reversible fixture names/layout, helper library, routine project structure.
- **Tier C — proceed:** formatting, typos, normal debugging.
- At most 2–3 feasible options at each Tier A gate, with benefits, costs, recommendation, fallback, and actual feasibility evidence. Do not force another confirmation for an already recorded approval.

## ADR-000 — Lightweight source-of-truth workflow

- **Status:** USER-DIRECTED approach, in use for scaffold; exact implementation may be adjusted.
- **Choice:** Planning → Execution → Evaluation, short requirements/decision/handoff docs, AI prompt register, human sign-off for major choices. No elaborate agent bureaucracy.
- **Reason:** Deadline and resumption across agents, with trustworthy evidence.

## ADR-001 — SUT selection (FIRST)

- **Status:** OPEN; shortlist only, not verified locally.
- **Goal:** An Android-runnable existing news UI whose data source can be replaced with fixed fixtures, plus credible cross-platform story and minimal setup time.
- **Shortlist:**
  - **Google JetNews** (`https://github.com/android/compose-samples/tree/main/JetNews`) — native Android news sample; likely good fixture seams, but Kotlin/Gradle learning and iOS strategy separate.
  - **Volksverpetzer `vvp_app`** (`https://github.com/Volksverpetzer/vvp_app`) — real React Native/Expo news app and potentially reusable app code; unknown setup and injection difficulty.
  - **Now in Android** (`https://github.com/android/nowinandroid`) — strong reference on fake data and Roborazzi; large existing codebase and existing visual tests make it less desirable as the take-home implementation.
- **Fallback:** Tiny owned news sample app with a production-style component and injected fixture provider (explicitly permitted by employer).
- **First action:** Run the feasibility rubric in `docs/05_SUT_SELECTION.md` on **at most two** candidates. A SUT only wins when data injection is feasible; visual resemblance is secondary.

## ADR-002 — Mock-data injection (SECOND; coupled to SUT)

- **Status:** OPEN.
- **Preferred candidate:** **Fixture repository in test-only build/config** if SUT supports a clean swap of its real data provider; same UI renders fixed synthetic data.
- **Alternative:** Local/mock HTTP server with fixed route responses if a configurable API base URL makes this easier, especially when Android/iOS have separate app codebases.
- **Last resort:** Proxy/network interception; avoid certificate-pinning and brittle environment issues unless already supported.
- **Critical acceptance:** A named test scenario reliably produces fixed headlines, images, dates and states; live backend changes cannot affect screenshot data; scenarios don't leak between tests; real UI components remain unchanged.
- **Platform policy:** Share fixture **schema and scenarios**; allow platform-specific injection adapters. Do not overengineer universal mocks.
- **Reference:** `docs/06_MOCKING_STRATEGY.md`.

## ADR-003 — Test automation and visual comparison (THIRD; after SUT/mock spike)

- **Status:** OPEN. Strong USER PREFERENCE for shared-code approach; not final approval.
- **Leading candidate:** **Appium + Python/pytest**, Android UiAutomator2 + iOS XCUITest, shared tests/fixtures/reporting, platform-specific driver/selectors/baselines. Fits candidate familiarity and interviewer-reported QA-throughput issue; requires emulator/simulator and careful stability controls.
- **Alternative:** Native component snapshots (Android Paparazzi/Roborazzi; iOS swift-snapshot-testing). More isolated, often faster CI; less shared test implementation.
- **Likely production recommendation:** **Hybrid layering**: many fast component snapshots + few high-value Appium rendered-screen journeys. Whether both layers can be *implemented* is subject to deadline; don't promise a hybrid demo without tests.
- **Appium risks:** Emulator boot and session time, rendering nondeterminism, selector differences, CI device cost. Appium does **not** provide mocks automatically.
- **Reference:** `docs/07_ARCHITECTURE_CI.md`.

## ADR-004 — CI execution and scalable rollout (FOURTH)

- **Status:** PROPOSED architecture; not implemented.
- **Default:** Local Android emulator for demonstrable CI path; separately describe macOS iOS simulator or hosted device-farm extension. Cloud is **optional**, not mandated by PDF.
- **PR:** focused deterministic visual gates; baseline/actual/diff artifacts; no automatic golden acceptance.
- **Nightly/release:** broader scenario/device/theme matrix, parallel capacity as justified by measured cost.
- **Evidence before claiming success:** a completed green CI run and a deliberate or naturally failing diff run, if feasible.
- **Reference:** `docs/07_ARCHITECTURE_CI.md`.

## Approval gate — fill before EXECUTION

```text
SUT: OPEN
Proof it builds/renders: NOT VERIFIED
Mock mechanism + scenario selection: OPEN
Proof fixed fixture rendered: NOT VERIFIED
Demo platform + test runner: OPEN
Goldens/comparison plan: OPEN
CI minimum + fallback: OPEN
Human approval: PENDING
``` 

Changing a chosen architecture after approval requires a short reason and updated handoff, not a large document.


---

## 2026-11-01 public source inspection — decision checkpoint (NEW)

**Decision states remain OPEN. No Tier A approvals, implementation or demonstrated Android screenshot.** Read-only GitHub repository pages reviewed; user's Windows machine not inspected. The following is one proposed *coupled* decision to ask for approval after the bounded feasibility spike, not a retroactive approval.

| Gate | Proposed default | Reconsider / fallback | Evidence needed before approval |
|---|---|---|---|
| ADR-001 SUT | **JetNews** native Compose sample | `vvp_app` only if app data boundary and launch are demonstrated promptly; owned news app if JetNews fails hard | Pin source SHA, rights/assets check, actual runnable/renderable UI |
| ADR-002 fixtures | **Test-only `PostsRepository` / scenario-specific `PostsFeed`** | `vvp_app`: test-only provider or HTTP server if confirmed configurable | Fixture-to-real-view text change, no live content, controlled state/reset |
| ADR-003 runner | **Conditional Appium + Python/pytest** if a pinned local Android emulator, selectors and fixture launch control are readily available | **Roborazzi/Paparazzi direct Compose snapshots** if emulator/Appium cost or readiness blocks the deadline | First real screenshot + repeatable reference comparison; measured effort on host |
| ADR-004 CI | PR smoke + approved Android goldens/diff artifacts; written macOS iOS pathway; broader nightly matrix | Native snapshot on PR, limited Appium on nightly/critical screens | Testable workflow and actual green job needed before claiming CI works |

**Rationale:** JetNews' `FakePostsRepository` is source-confirmed; however, it introduces a fake 800 ms delay and every-fifth failure, so merely using its existing data would *not* meet screenshot determinism. `HomeScreens.kt` uses existing `PostCardTop` and `PostCardSimple`. `vvp_app` (Expo + TypeScript) has stronger cross-platform app-code reuse but its exact network seam remains untraced. JetNews is not claimed to contain a breaking banner or premium badge as-is. Android Compose tags need evaluation; none found in inspected `HomeScreens.kt` file.

**Approval question to human:** authorize the **bounded read-only/local build feasibility spike** described in `05_SUT_SELECTION.md`, then approve or adjust the entire SUT + mock + runner + CI-minimum bundle **once** based on results. Do not start EXECUTION or lock Appium beforehand.

---

## ADR-001A — Human-approved SUT spike order (2026-11-01)

**Status: APPROVED for bounded PLANNING feasibility only. Not an SUT selection or EXECUTION authorization.**

- **Human decision (verbatim):** "Prioritize vvp_app in the bounded SUT/mock feasibility spike. Keep implementation and runner decisions open."
- **Operational impact:** Inspect **Volksverpetzer `vvp_app` first** for native Android launch feasibility and a deterministic data seam. JetNews is second candidate/fallback if vvp hits a hard feasibility blocker; an owned small sample remains the final deadline fallback. Now in Android remains a reference.
- **Supersedes:** The previously documented JetNews-first **spike ordering and provisional default** for this work session. Earlier JetNews findings remain valid historical evidence, not an approval to switch back or implement it.
- **Still OPEN:** actual SUT choice; whether to use test-only fixture provider versus mock HTTP; named scenario entry/reset and target screen; screenshot runner (Appium + Python/pytest versus Maestro + visual comparison or justified alternative); local/device CI; hand-in claims. Never infer approval from this spike authorization.
- **Verification:** Public `vvp_app` README documents Expo/TypeScript, Node 24+, pnpm, `pnpm android`, app variants, `.env` configuration and native EAS build profiles. F-Droid describes a network-dependent app connected to a non-configurable service in the distributed variant; **not proof that source-level endpoint override is impossible**. Concrete article service/hook/component files and build on the user's Windows machine remain unverified.
- **Boundary:** Read-only source inspection and bounded checkout/build/launch checks are authorized in PLANNING; no test-build fixture changes, screenshot-framework code, golden generation or CI implementation until the major design is approved. A successful public F-Droid build (if found) is not an executed build on our machine.

### Next explicit approval gate (not requested yet)

Provide actual `vvp_app` feed component → hook/query/service → data source path, source SHA, Windows build/launch evidence, test selectors and license/asset limits. Then compare two concrete mock choices (fixture provider or mock API) and two runner choices (Appium/pytest or Maestro visual assertions), with JetNews/owned-sample fallback and CI consequences; ask for a **single coupled implementation approval**. Until then statuses are OPEN.

References: https://github.com/Volksverpetzer/vvp_app ; https://f-droid.org/de/packages/de.volksverpetzer.app/ ; https://docs.maestro.dev/reference/commands-available/assertscreenshot .


---

## ADR-001A evidence checkpoint — user's Windows checkout (2026-11-01)

**Decision state unchanged: `vvp_app`-first bounded feasibility spike APPROVED; final SUT, data seam, runner and implementation remain OPEN.**

User-supplied PowerShell command output from `D:\Projects\axel-springer-assignment\vvp_app` establishes:

- `git clone --branch prerelease --single-branch` completed successfully; `git rev-parse HEAD` returned `8b421753a17a18cd648447319adcca61a288f97f` (recorded exact revision; not evidence of a permanent detached/pinned working branch).
- `node --version` returned `v22.12.0`; repository README asks for Node `24.x+`. The mismatch must be resolved before treating an install/build as supported.
- `pnpm` was initially unavailable; user installed global pnpm via `npm install -g pnpm`; `pnpm --version` then returned `12.11.2`. Project's pinned `packageManager`, engines and lockfile compatibility **not yet examined**; do not claim pnpm 12 is the right project version.
- `adb devices -l` returned an empty device list; no emulator/device was running.
- Android emulator `-list-avds` returned `Pixel_10`. An existing AVD definition is not proof of boot, SDK/JDK correctness, or functional app.

**Next authorized PLANNING work:** inspect `.nvmrc`, package scripts/engines and tracked env-sample name (without exposing secrets); trace exact feed UI → data hook/service/API boundary and existing `testID`s; check Java/Android environment and only then try an Android build/launch. Read-only `git archive` of HEAD may be uploaded for direct source inspection. No `pnpm install`, fixture edits, runner adoption, goldens, CI work or Tier A decision is reported as completed.


---

## ADR-001A checkpoint 2 — archived source trace and toolchain validation (2026-11-01)

**Status:** Authorized `vvp_app`-first feasibility inspection is advancing. **No Tier A implementation decision approved.** The user generated a `git archive HEAD` from the reported commit `8b421753a17a18cd648447319adcca61a288f97f`; its source contents were reviewed (a Git archive alone does not cryptographically prove the SHA), **not compiled or executed**. Git working tree clean in user report.

- **Toolchain:** `.nvmrc` = `24`; `package.json` declares Node `24.x` and `pnpm@12.11.2`, matching `pnpm-lock.yaml`. User host Node `22.12.0` is out of range, pnpm `12.11.2` matches. Host `java -version` is Java 11.0.24, `JAVA_HOME=C:\Program Files\Java\jdk-11`; React Native `0.86.3` requires/recommends JDK 17 for Android per official React Native guidance. `ANDROID_HOME` and configured Pixel_10 AVD exist; actual emulator boot and native build are still unverified. `.env.sample` exists and `.env` is not tracked.
- **Existing main news-data seam (now SOURCE-CONFIRMED):** `src/app/(tabs)/home.tsx` creates enabled `FeedFetcher` functions; `src/screens/Home/fetchers/FeedFetcher.ts` wires WordPress feeds to `WordPressAPI.create(entry.handle)`; `WordPressFetcher.createFetchers(api)` accepts a `getPosts/searchPosts` object; its `mapArticleToPost` builds a `Post` wrapping the **existing** `ArticlePost`; `src/screens/Home/components/Feed.tsx` feeds `GenericPost` / `ArticlePost`. This makes a deterministic **test-only injected fetcher** a concrete implementation candidate. **No fixture injection has occurred.**
- **Important distinction:** `src/helpers/apiUrl.ts` offers a FOSS-only, HTTPS-only override for the auxiliary `ServerAPI` (`src/helpers/network/ServerAPI.ts`), **not** the WordPress site URLs used by the main article feed. A local WireMock service cannot be assumed to replace the primary feed without separate URL/client injection. Earlier assumption that all content comes from one fixed app server is corrected by the archived source.
- **Dynamic side effects to control:** `ArticlePost.tsx` performs a separate `WordPressAPI.getFeatureImage` request based on `_links["wp:featuredmedia"]`; also uses read-progress persisted state and `ViewCounter`, with optional animated loading GIF. Feed has announcements and enabled social sources. A deterministic headline alone is not full visual determinism. Existing `testID="article-progress-bar"` is not a unique, content-ready locator; add a stable card/root ID and ready signal if Appium/Maestro is selected.
- **Rights:** root `LICENSE.md` is MIT; do not assume supplied logos, editorial photos or trademark are freely reusable. Use synthetic test content and locally owned static assets for committed fixtures/screenshots; retain attribution/notice for reused code.

### Coupled choice for forthcoming human approval — PROPOSED, not selected

1. **Recommended if Android build works:** `vvp_app` + debug/test-only **fixture feed provider** at `WordPressFetcher.createFetchers`/Home `Feed.fetchers` boundary, using actual `ArticlePost`; optionally a test-only card-preview route as minimum fallback. Freeze image, time, announcement, engagement, onboarding and persisted-state effects. Intended first scenario: long German headline with explicit fixture and no live fetch. **Still requires a verified local native build, test-only scenario-selection/reset design and actual fixture-to-UI proof in EXECUTION.**
2. **Alternative:** `vvp_app` + deterministic WordPress HTTP stub, *only* after deliberately adding a debug-only WordPress client/base-URL seam and image endpoint controls. HTTPS-only `ServerAPI` override does not solve this.
3. **Deadline contingency:** If Expo native build on corrected Node/JDK is still blocked after a short attempt, present JetNews with its confirmed fake repository (or small owned news app). Do not force `vvp_app` for code sharing alone.

**Runner remains OPEN:** compare Appium + Python/pytest vs Maestro + screenshot diff only after the native app/fixture-seam gate. No running app, screenshots, goldens, diff, iOS or passing CI is claimed. Human already approved the bounded investigation; do **not** re-request that approval. Ask once for EXECUTION approval of the coupled SUT/mock/runner/scope decision after remaining feasibility evidence.

---

## 2026-11-01 — fixture implementation feasibility authorization (LATEST)

**Human statement:** "I have reviewed the approach. We can proceed." This followed an explicit recommendation to conduct a **bounded, development-only `vvp_app` home-feed fixture feasibility test**. Interpret as permission to prepare/apply that narrow experiment, **not** as final Tier A approval of SUT, mocking mechanism, Appium/Maestro, full implementation, goldens or CI.

**Android baseline observed by user:** native development app running with actual article cards/headlines on the Pixel 10 emulator; `adb devices`, `sys.boot_completed=1`, `pm path android` responsive after cold boot. Metro running. The social feed `/proxy/instaFeed?account=pruefpunkt` returned HTTP 502 and a visible debug toast. Those live-feed observations are **not** fixture-mode proof.

**Bounded proof prepared by assistant:** binary Git patch `vvp_qa_fixture.patch` against pinned `vvp_app` `8b421753a17a18cd648447319adcca61a288f97f`. `EXPO_PUBLIC_QA_SCENARIO=long_headline` + `__DEV__` gates a synthetic article returned by the existing WordPress mapper and rendered using unchanged feed flow and existing `ArticlePost`; static local generated image; no non-QA home feed fetchers, announcements, view counter or reading progress in this QA scenario; ready/title `testID`. Startup popups suppressed in fixture mode. **No final architecture approval is implied by creating this patch.**

**Static verification performed:** patch cleanly applies to a fresh extracted copy of the user's exact archive; PNG image bytes match; all six edited/new TypeScript files pass TypeScript syntax/transpilation only. **Not verified:** full `pnpm check:ts`, Metro packager success after patch, actual fixture UI on Windows, no app-wide background network calls, screenshot golden/diff, driver selector, CI, iOS.

**Next human evidence:** apply patch locally, run `pnpm check:ts`, start Metro with the opt-in QA scenario, show fixture headline and image on emulator and report whether toast remains. **Combined approval of SUT + mocking + runner + narrow scope remains pending** until those results are in.

---

## ADR-005 — FINAL approval of Android visual demo scope (2026-11-01)

**Status: APPROVED BY HUMAN. Supersedes all older `OPEN` statements for the four explicitly approved choices.**

**Human statement (verbatim):** "Yes. It is good enough to move forward. I approve Volksverpetzer + test-only fixture fetcher + Appium/Python pytest + one Android screenshot scenario, with Maestro as the time-boxed runner fallback."

| Decision | Approved scope | Evidence / remaining gate |
|---|---|---|
| SUT | Volksverpetzer `vvp_app`, pinned upstream `prerelease` commit `8b421753a17a18cd648447319adcca61a288f97f` | Android native live and QA fixture view user-confirmed; code derivative to be committed |
| Mock | `__DEV__` + `EXPO_PUBLIC_QA_SCENARIO=long_headline` fixture fetcher returning synthetic WordPress-mapped article to unchanged `ArticlePost` | Patch applied on Windows; `pnpm check:ts` passed; user screenshot confirms title/image; no complete app-wide network audit |
| Runner | Appium + Python/pytest, Android UiAutomator2 | **Approved, not installed/executed**. XCUITest iOS strategy only. Maestro fallback if bounded Appium setup blocks; pivot requires brief reason and explicit acknowledgement. |
| Minimum visual demo | One Android long-headline article-card screenshot → human-reviewed committed golden → automatic comparison and failing diff if feasible | Appium session, true native PNG, repeatability, golden, diff and CI **not yet verified** |
| PR/CI | Design a practical focused PR gate; implement narrow runnable path and evidence artifacts; iOS in strategy | A YAML proposal is not green CI evidence; do not overbuild device cloud |

**Phase transition:** PLANNING → **EXECUTION** authorized. No further SUT/mock/runner approval prompt necessary. Time-box UiAutomator2 setup and document exact obstacles; do not silently switch runner. Reserve time for strategy, README, prompt log and interview rehearsal.

**Initial implementation artifact prepared, not yet Windows-verified:** `qa_visual/` Python suite (platform-neutral image comparator, Android driver adapter, one integration test, baseline review workflow, local unit checks and README), to be placed inside `vvp_app`. No approved reference PNG is included, because only the emulator-window image was shared and a native Appium element screenshot has not yet been captured. Do not copy that window screenshot as a fake golden.

---

## ADR-005 — Submission repository foundation (2026-11-01, proposed layout; migration pending)

**Naming and intent:** Human selected the neutral portfolio name `visual_regression_qa_strategy`, not employer-branded naming. Proposal: one root Git repository with `app/` (adapted `vvp_app`), sibling `qa_visual/` (Appium/pytest framework), public `docs/`, historical `reference/patches/`, root `AGENTS.md`/`CLAUDE.md`, root README and root CI workflows if implemented. No nested Git repository or submodule.

**Private material:** Original challenge PDF and detailed assignment-specific planning/phase documents remain local under ignored `.project-private/`; only neutral, accurate deliverables and AI prompt disclosure are public. The original `vvp_qa_fixture.patch` is an already-applied historical reference, **not** a patch to apply twice. Preserve original upstream Git metadata outside new root before `git init`. GitHub remote should be private until asset-rights and content review.

**Evidence state:** This is a repository layout decision/proposal, **not an executed move, committed repo, pushed remote or verified post-migration Android build**. The user has not provided migration command results. Any final layout changes should update this ADR.


## EXEC-020 - Runtime selection decision (human approved, 2026-11-07)
Option B is approved: one development QA artifact, immutable per-cold-launch scenario selection, no live switching. Retain EXPO_PUBLIC_QA_SCENARIO as fallback. Explicit qa_scenario launch query wins; none disables fallback. Only long_headline is capture-supported; four future IDs remain unsupported. __DEV__ gate remains mandatory.
Implementation candidate: initial-URL promise gate above root providers/feed, with a dev-client wrapper URL to explicitly load Metro and a development-only native-intent route to home. Installed dependency source shows plain app-scheme cold launch may land in the launcher chooser. No delayed post-render selector is permitted. Runtime delivery is BLOCKED pending available emulator/Metro/Appium; unit/source evidence is not acceptance of native reliability or a standalone CI QA artifact. Do not implement new scenario UI until foundation runtime verification passes.


## EXEC-024 - Approved runtime-selected baseline contract - 2026-11-07T14:25:05.223669+01:00
Human explicitly APPROVED exact runtime candidate 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC on November7,2026 after image/diff review; approval instruction authorized promotion andtwo nativeverification runs. Replaced only qa_visual/baselines/android/pixel10-api37/long_headline.png withapprovedbytes. Previous environmentfallbackhash E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629 remains inGitHEAD ae07a0a7cbfae8be329d2e1a63d32ede575f32c9. Migration local/uncommitted; no historychange. Explicit qa_scenario=long_headline coldlaunch nowdefines referencecontract. Two independent originalAppiumpytest runsPASS(exit0),0changed,1028x1237,exactidentity/readiness/title/bounds verified; actualsbyteidenticaltocandidate/eachother. Thresholdsunchanged12/0.002. Legacyfallbackmaynotmatchnewreference. Nativefractionalroundingcauseunresolved andnot claimedfixed. Supportedlong_headline runtimevisual acceptance closes under thisreviewedcontract; noapproval toimplementnewscenarios/CI/iOS or commit/push. Persistentstate/standalonebuild limitationsremain. OriginalOptionBselectionarchitecture retained.


## EXEC-025 - Breaking-news sample extension and approval boundary - 2026-11-07T14:39:07.101213+01:00
HumanauthorizedminimalQA-onlybreakingbannerintheexistingfeedandAppiumframework. AnnouncementCarddismiss/actions/impressionsarenotreused. ActivebreakingselectionusesguardedrealView/Typographybanner,measuredlayoutreadiness,separateComponentObject/nativeelementcapture;originalsyntheticarticlebelowunchanged. breaking_newsnowcapture-supported;dark_article/no_image/empty_feedremainunsupported. TwoindependentnativecapturesmatchSHA E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F;candidateinignoreddebug-logs/exec025/review/,NOTapprovedorinstalledasgolden. Existinglonggolden/regressionunchangedPASS. Humanreviewexactcandidateandseparatepromotionauthorizationrequired. NoadditionalUIscenario/CI/iOS/commitapproved.


## EXEC-026 - Breaking-news reference approved and verified - 2026-11-07T14:56:26.851036+01:00
Human explicitly approved only candidate SHA-256 E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F after image/context review on November7,2026. Exact bytes copied to qa_visual/baselines/android/pixel10-api37/breaking_news.png (1028x493RGBA); local/uncommitted, no automatic regeneration. Two independent explicit breaking_news cold-launch regressions pass with0changed; byte/raw/policy repeat differences0. Existing long_headline passes against unchanged 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC. Two approved Android references now verified; comparator remains delta>12,maxratio0.002. Banner remains a development-only sample-app challenge extension, not authentic upstream production functionality. Normal production UI and runner architecture unchanged. Await review before another scenario; no CI/iOS/commit/push authorization implied.


## EXEC-027 - Development-only nonpersistent QA appearance - 2026-11-07T15:14:23.006686+01:00
Human authorized dark_article using real VVP theme and unchanged article. Immutable launch selection now enables dark_article. A read-only __DEV__/active-fixture override in the shared color-scheme hook selects dark for this ID and light for the two approved scenarios; no user setting writes or duplicate UI. Real article metadata exposes effective-theme marker for Appium. Two independent native dark captures are byte-identical (1028x1237,SHA2566FD667E87476F941F7CB7A8152F60FFB8C51A3FD4217A7E993300AB32EB62A96), separated by effective-light long regressionPASS. Both existing references/regressions preserved,PASS0changed. Dark candidate is NOT approved and absent from baselines; explicit human review and separate promotion task required. No other scenario/CI/iOS/commit authorized. Release gating unit/source verified, release build not executed.


## EXEC-028 - Dark reference approved and verified - 2026-11-07T15:37:11.045622+01:00
Human explicitly approved exact candidate SHA2566FD667E87476F941F7CB7A8152F60FFB8C51A3FD4217A7E993300AB32EB62A96 on November7,2026. Bytecopy installed dark_article.png1028x1237RGBA; newlocaluntracked reference,not committed. Two independent dark regressionsPASS0changed,light long/breakingPASS0changed withnativeeffectivelightmarkers,finaldarkafterlightPASS0changed. Darkactualsbyteidentical;storedtheme systemunchanged. Bothpriorapprovedgoldens unchanged,threshold12/0.002retained. ThreeapprovedAndroidreferences nowverified; no fixture/layout/selectorarchitecture change. CI/nativeiOS unverified; no newscenarioimplementation/commit/push authorized. Awaitreviewbeforeboundedno_image.


## PRE-EXEC-029 - Approved no_image scope and local Git checkpoint - 2026-11-07
Human approved: (1) no_image is a development-only QA fixture variation using the real ArticlePost; legitimately absent featured media (not an invalid URL); no image panel/placeholder/onLoad-dependent readiness; NO general production optional-media change in EXEC-029; limitation to be documented transparently. (2) Stale long_headline hash in qa_visual/baselines/android/pixel10-api37/README.md corrected to 6A9E18DA...C878CC. (3) Selective local checkpoint before further scenarios; no push, no remote. Upstream scaffolding (app/.github, fastlane, .husky, eas.json, Gemfile*, .gitleaks.toml, lint-staged.config.ts, .watchmanconfig, CODE_OF_CONDUCT.md) deliberately excluded. Commit carries no Co-Authored-By trailer by human instruction; sanitized docs/ai_prompts_used.md is the assistance disclosure.


## EXEC-029 - no_image QA media contract (implemented; candidate pending approval) - 2026-11-07
Implemented per approved PRE-EXEC-029 scope. Root cause of old cover behavior: ArticlePost chose QaFixtureCover by slug (isQaArticle), not from fixture data, so `_links: {}` never signalled absence. New explicit dev-only contract getQaArticleMedia(slug) in qaScenario.ts: qa-long-headline -> "bundled-cover"; qa-no-image -> "none" only while active scenario is no_image; undefined for production articles, normal launches, release. ArticlePost omits only the image wrapper for "none"; readiness qa-article-no-image-ready from text-block onLayout. no_image capture-supported; launcher allowlist extended. Runtime-selection architecture, thresholds, goldens unchanged. Challenge-scoped; not upstream VVP support. Candidate SHA AC5BD84B93778F4773B3A38ABD391A89483295446A2E096DD59E21CA288B3012 NOT approved/installed.


## EXEC-030 - no_image reference approved and verified - 2026-11-07
Human approved only candidate SHA AC5BD84B93778F4773B3A38ABD391A89483295446A2E096DD59E21CA288B3012 after image/context review; outer-padding concern resolved (element screenshot = outer card only; context shows feed margins). Byte copy to qa_visual/baselines/android/pixel10-api37/no_image.png (1028x711 RGBA), local/uncommitted. Two no_image regressions PASS 0 changed; dark/long/breaking PASS 0 changed. Four approved Android references; thresholds 12/0.002 unchanged; no rendering/fixture/architecture change. CI/iOS unverified; empty_feed unsupported.


## PRE-EXEC-031 - Four-scenario local checkpoint - 2026-11-07
Human accepted EXEC-030 and approved the exact 18-file inventory. Local commit 8c54f0f711f7b4a78a8a49d25bc1728cc919b002 (parent f0b38e9) "feat(qa): add no_image Android visual scenario and approved golden"; no Co-Authored-By trailer by instruction (disclosure in docs/ai_prompts_used.md). Four approved Android references now tracked in HEAD. Upstream scaffolding remains intentionally excluded. No push/remote. Next intended task: empty_feed (EXEC-031), not yet authorized.

## EXEC-031 - empty_feed successful-empty contract - 2026-11-07
Implemented within the approved QA-only boundary, with no production architecture rewrite. empty_feed = the one configured synthetic source (qaFeedFetcher) resolves [] successfully. It is not offline, error, loading or zero-configured-feeds coverage.
Success vs error: FetcherUtilities turns exceptions into [], so a dev-only outcome record (qaFeed.ts getQaFeedOutcome/isQaSuccessfulEmptyFeed/resetQaFeedOutcome) is written only on fixture resolution. Feed clears it before each request in empty_feed mode.
Readiness qa-empty-feed-ready on the message region requires: success outcome, initialLoad, !refreshing, posts 0, measured layout.
EmptyComponent gained optional messageTestID, messageAccessibilityLabel and onMessageLayout props. They are unset in production and other scenarios, so the markup is unchanged.
Capture boundary: message region only. The donation card (scroll picker, payment buttons) is excluded; the context screenshot is diagnostic.
empty_feed is now captureSupported and on the launcher allowlist; the theme is light. No scenario remains "unsupported" in the registry (that code path is kept).
Candidate SHA 903B971081AC2EA2FEB2A37D1B73473602E176A8E9FFE046074E7D3BDE5FA795 is NOT approved and NOT installed. Human review is required. Thresholds 12/0.002 and the four goldens are unchanged.

## EXEC-032 - empty_feed golden approval - 2026-11-07
Human reviewed the image and context. Approval covers ONLY candidate SHA 903B971081AC2EA2FEB2A37D1B73473602E176A8E9FFE046074E7D3BDE5FA795, plus the message-only capture boundary (donation card, payment controls, dynamic status bar and dev warnings excluded).
Promoted byte for byte to qa_visual/baselines/android/pixel10-api37/empty_feed.png (1028x309 RGBA); local and uncommitted.
Five approved Android references; thresholds 12/0.002 unchanged; no rendering, fixture or architecture change. CI and iOS are unverified.

## PRE-EXEC-033 - Five-scenario Git checkpoint - 2026-11-07
Human accepted EXEC-032 and approved the exact 20-file inventory plus documentation-only corrections.
Five-scenario Android suite is the final approved demonstration scope; no further visual scenarios are planned.
Local commit bcc56b24dbe67472e178ce27fbab54a442bce482 (parent 8c54f0f): "feat(qa): add empty_feed Android visual scenario and approved golden". No Co-Authored-By trailer, by instruction. No push or remote.
deliverables/strategy.md scope mismatch is deferred to final consolidation.

## EXEC-033 - Intentional visual failure demonstration - 2026-11-07
Human-approved design: dedicated pytest marker intentional_failure, excluded by default via addopts -m "not intentional_failure"; genuine FAIL at the comparison assertion (no xfail, skip or inverted assertion).
Deliberately incorrect reference qa_visual/demo_assets/intentional_mismatch_breaking_news.png (R/B channel swap of the approved breaking_news golden; 1028x493 RGBA; SHA A8BBE42E3932FEA83B1FC905814310022CF75D8617FC0F019528B18E905EB3CA). Versioned demo asset with a deterministic generator; never in baselines/ and not a golden.
Framed as a reference-mismatch demonstration, NOT an application regression. No app, golden, threshold, CI or iOS change. Uncommitted, awaiting review.

## EXEC-034 - Final strategy reconciliation - 2026-11-07
Strategy restructured into 9 sections; two pages kept (brief allows ~1-3). Evidence claims limited to EXEC-032/033 local runs; iOS, CI components, DI/mock-server and component snapshots presented as proposals only. No employer architecture assumed. Removed strategy link to ignored docs/AGENT_TASK_HISTORY.md. Agent-led implementation ends here; human review next.

## EXEC-035 - Self-contained scenario launching - 2026-11-07
Human decision: visual tests are independently runnable (PyCharm Run) and declare their own scenario. Chosen: @pytest.mark.qa_scenario("<id>") + fixture + launcher-built dev-client URL; VVP_QA_LAUNCH_URL kept only as a validated, matching-only override; VVP_METRO_HOST/PORT optional. Intentional demo uses the same marker, keeps intentional_failure and not visual. No app/fixture/golden/threshold change.


## EXEC-036 - 2026-11-08T00:48:03.068685+01:00
Keep environment/default configuration, no dotenv or new example/helper. Document inherited-env precedence and existing validation limits. Fresh candidates are native test output; approval is a separate human hash decision. Rehearse promotion in ignored temporary files with explicit confirmation, verified backup and copied hash. All five native comparisons and41units pass; six references unchanged. No actual promotion authorized/performed. Further refactoring remains a separate reviewed task.


## EXEC-037 - 2026-11-08T01:20:10+01:00
One authoritative root pytest.ini; visual tests stay in qa_visual/tests, Python units move to unit_tests. Extract only artifact/comparison plumbing and session lifecycle. Scenario assertions, native component capture, thresholds and reference bytes remain unchanged. Preserve explicit environment-tolerance opt-in for four scenarios; breaking/demo defaults unchanged. Ruff deferred, no dependency added. Verification50units,5visuals0pixels,default55pass1deselected; intentional real failure retained. Changes uncommitted for human review.


## EXEC-038 decisions
- Allure is optional (inert without --alluredir); no CLI needed for tests; evidence attached inside VisualArtifacts.compare() before the assertion; staleness via mtime >= VisualArtifacts.started_ns; reporting active only for qa_scenario tests.
- Intentional demo reported in a separate results dir/suite, never converted to xfail/skip.
- Readable titles via __allure_display_name__ (plugin resets dynamic titles at call phase).


## EXEC-040 decisions (human-directed)
- Discontinued docs/AGENT_TASK_HISTORY.md and docs/ai_prompts_used.md; private 03_HANDOFF.md is the operational history; prompts logged privately only. Final employer AI-prompt disclosure is outstanding human work (R11).
- FIXTUR spelling and duplicate breaking_news identity wait are intentionally out of scope.

## EXEC-040B decisions
- Failure evidence retained under artifacts/android/<profile>/failures/ (ignored); comparison semantics, thresholds, Allure, lifecycle untouched.
- Proposed (not yet approved): sanitized tracked AGENTS.md; exclude upstream tooling files; clean public history; brand-asset notice; confirm Mimikama assets.

## EXEC-040C decisions (human-approved)
Private first remote; keep history and authorship; exclude all ten untracked upstream app files; AGENTS.md/CLAUDE.md/.project-private stay ignored; no sanitized public agent file; leave "challenge" wording; no more instability investigation; human compiles AI prompt disclosure. Added NOTICE.md (brand assets unresolved limitation) and fresh-clone setup table.

## EXEC-042B decisions
- Visual CI is advisory (continue-on-error on the pytest step only); setup failures fail the job. No retries, no golden/threshold changes, no CI-specific baselines without human approval.
- Own small emulator scripts instead of a third-party emulator action (exact API 37 ps16k image needed); no emulator matrix.
- Separate jobs: APK reused via artifact, no second native build.

## EXEC-042B-R1 decisions
- Build and visual tests are independent manual workflows; visual reuses a prior run APK via source_run_id (7-day expiry) validated at run time. Compatibility = ancestor + no APK/visual-affecting path changes, not SHA equality. Docs/workflow changes never invalidate.

# Visual Regression Suite Expansion — Decision & Implementation Handoff

**Project:** Visual Regression QA Strategy — adapted Volksverpetzer mobile news application  
**Decision date:** 2026-11-07  
**Decision status:** **Scope approved by the human decision-maker; implementation details pending inspection in the existing execution thread**  
**Suggested project location:** `docs/08_VISUAL_SUITE_EXPANSION_DECISION.md` (new document; do **not** replace `02_DECISIONS.md`)  
**Primary audience:** candidate / implementation-thread AI architect / coding agent  
**Relationship to existing decisions:** extends, but does not supersede, the approved Volksverpetzer + development-only synthetic fixtures + Appium/Python/pytest architecture.

## 1. Executive decision

Retain the **already implemented Appium `long_headline` test** (implementation reported by the candidate) and add **four targeted Android visual regression scenarios**, using the same real-app fixture injection, Appium runner, Python comparison engine, reporting, and human-reviewed goldens:

1. **`breaking_news`** — a deterministic breaking-news banner appearing in context above or within the actual news feed.
2. **`dark_article`** — the existing article teaser rendered using the application's actual dark theme.
3. **`no_image`** — an article teaser with no featured image, exercising a legitimate text-only layout.
4. **`empty_feed`** — the feed's successful-empty-content state, distinct from loading, offline, or backend-error behavior.

**Target suite:** five distinct scenarios including `long_headline`. The four new scenarios are an **approved expansion target**, not a claim that fixtures, UI, goldens or passing tests already exist. Preserve all current working tests and approved reference images.

**Why:** The employer's challenge explicitly describes a news feed with breaking-news banners, teaser cards with/without images, light/dark modes, and offline/error-like states; it additionally asks for an adapted sample application that can mimic a feed with a breaking-news banner. The expansion exercises **different kinds of UI risk**, not four variations of the same headline. These are representative options, not four separate mandatory employer requirements. A paywall/premium scenario is **deliberately outside this expansion** because no authentic premium/paywall implementation has been verified in the selected VVP SUT.

## 2. Evidence and boundaries

### Employer task (authoritative PDF)

- A **1–3-page cross-platform Android/iOS strategy** plus a runnable mocked-data screenshot demo on **at least one platform**; a few representative components/screens and approved golden PNGs.
- Explicit examples include **breaking-news banners**, teaser cards **with and without images**, premium items, long German headlines, dark mode, large fonts, and offline/error states.
- Both Appium/Maestro on emulators and off-device native snapshots are acceptable; cloud execution is optional. A deliberate regression and diff is highly desirable, not compulsory.
- No employer codebase was supplied. The permitted adaptation must render **real application UI**, not simply compare fabricated/static pictures.

### Already decided / previously observed

- **SUT:** Volksverpetzer `vvp_app` adapted from pinned upstream `prerelease` SHA `8b421753a17a18cd648447319adcca61a288f97f`.
- **Workspace:** `D:\Projects\visual_regression_qa_strategy`; application `app/`, visual runner intended in `qa_visual/`, documentation `docs/`, original fixture patch under `reference/patches/`, private employer documents in ignored `.project-private/`.
- **Fixture seam:** development-only QA scenario activated by `__DEV__` and `EXPO_PUBLIC_QA_SCENARIO` with a synthetic in-app feed; article data follows the WordPress mapper → feed → `GenericPost` → real `ArticlePost` UI path. This was rendered on Android in prior evidence. Fixture patch was already applied; **do not reapply it**.
- **Runner:** Appium + Python/pytest with Android UiAutomator2; reuse existing shared comparison/reporting rather than introduce another tool. iOS strategy can reuse high-level contracts but needs distinct XCUITest driver and platform goldens; no native iOS execution is claimed.
- **Existing `long_headline` Appium test:** **candidate now reports it implemented**. Exact current test source, baseline approval, last PASS, and CI status must be read from the implementation thread/repo; do not infer them from older, pre-implementation handoffs.
- **Local environment history:** Pixel_10 / Android API 37 previously suffered confirmed `LOW_MEMORY` process exits with 2 GB AVD RAM and nearly exhausted swap. Candidate changed AVD to **4 GB**, ran with `-gpu software`, and reported better sustained app stability. Repeatability in the latest environment and latest runner outcomes must still be verified, not inferred.

### Source-dependent assumptions to verify before editing

- Pinned upstream includes `src/components/posts/AnnouncementCard.tsx`, `ArticlePost.tsx`, `src/components/views/EmptyComponent.tsx`, `src/screens/Home/components/Feed.tsx`, and `src/hooks/useAppColorScheme.ts`. These are **inspection leads**, not proof of correct post-patch behavior or exact current component API.
- VVP is **not verified to have a production-equivalent breaking-news banner** or a premium/paywall workflow. Build only the minimum honest QA sample-app extension necessary for `breaking_news`.
- The current `qa-article-card-ready` marker was designed around image `onLoad`; it **cannot automatically serve** an image-less card or empty feed. Adapt scenario-specific readiness signals.

## 3. Scenario acceptance contracts

### A. `breaking_news` — highest priority

**Editorial example:** a fixed German `EILMELDUNG` banner with an intentionally long but readable headline, stable metadata/time if shown, and a fixed article below for layout context. Use **synthetic** content, not live politics or real breaking news.

**Expected real UI:** A native React Native banner with distinctive urgency treatment, rendered by the actual adapted VVP feed layout. Inspect the existing feed-header/announcement implementation for a suitable insertion point. Do not simply rename a generic announcement and claim that VVP already provides a breaking-news feature.

**Test intent / checks:**
- Banner visible only for its selected fixture; correct visual treatment and no overlap/clipping with header, feed card or navigation.
- Long German headline wraps without truncation; label, headline and optional timestamp remain readable.
- If the banner is tappable/dismissible, avoid flaky transitions: either keep it static within QA mode or pin its initial state; no random expiry or live updates.
- Screenshot the **banner element** if a stable element boundary exists, plus optionally a non-compared full-screen context screenshot. If its critical risk is **interaction with the feed**, use a stable containing feed-region screenshot as an additional assertion; avoid excessive duplicate baselines.

**Suggested selectors:** `qa-breaking-banner-ready`, `qa-breaking-banner-title` (exact naming flexible; reuse repo conventions).

**Done when:** mock fixture → real banner + feed → stable readiness → two comparable native captures → reviewed golden → visual PASS; deliberate title/spacing change produces meaningful FAIL and diff at least once in the expanded suite.

**Key honesty boundary:** Label the banner as a **sample-app extension implemented for the challenge**, not an existing VVP production feature or Axel Springer implementation.

### B. `dark_article` — reuse the real article teaser

**Fixture:** preferably identical headline, author/date, image, category and metadata to `long_headline`; only the **theme** changes. This isolates color/theme regression risk.

**Expected real UI:** The actual `ArticlePost` and surrounding native UI rendered through VVP's supported color scheme; do not simulate dark mode with a dark screenshot overlay.

**Test intent / checks:**
- Background, headline, metadata, tag/border and any icon colors meet the intended dark palette; no dark-on-dark/invisible text.
- Theme selection is explicit and consistent on repeat runs, independent of emulator/user preference leftovers.
- Fixed media assets, font size, locale and device profile match the baseline contract.
- Reuse existing article title/readiness selector when valid; theme changes must settle before capture.

**Implementation caution:** Verify whether `useAppColorScheme()`/settings persist a user preference. Use the smallest reliable **development-only QA override or explicit setup** and restore normal behavior outside QA mode. `adb shell cmd uimode night yes` may not override an app-pinned preference; verify the **rendered UI** rather than assuming system dark mode took effect.

**Done when:** on-screen actual dark theme is proven, repeated captures are stable, and a **separate dark-theme golden** passes. Never compare against the light screenshot or silently overwrite the original golden.

### C. `no_image` — text-only article teaser

**Fixture:** WordPress-like synthetic article with **absent/null featured media** and otherwise fixed title, summary, date and author. Do not simulate absence by returning a broken URL unless explicitly testing image failure (not the intended scope).

**Expected real UI:** The **same** production-style `ArticlePost` component displays a supported no-image layout. Avoid cloning the card into a test-specific substitute. If current code assumes an image always exists, add a small conditional branch that behaves sensibly for normal data as well, preserving production code paths.

**Test intent / checks:**
- No blank reserved image panel, indefinite loading skeleton, broken-image glyph, or unintended media request.
- Title/metadata/summary remain visible, ordered and correctly spaced; card height is appropriate for text-only content.
- Card and list boundaries remain intact; no neighbor overlap.
- Readiness is **data/render-state driven**; specifically **not** gated by image `onLoad`.

**Suggested selectors:** `qa-article-no-image-ready` or a generalized ready marker that is emitted after the relevant render/settled state; maintain `qa-article-title` if already used.

**Done when:** deterministic absent-media fixture yields the real text-only teaser, repeated native screenshots compare successfully to a reviewed **new** golden, and the existing image-bearing case still passes unchanged.

### D. `empty_feed` — successful empty content state

**Fixture:** A **successful fetch result containing zero items**, with known feed identifier; no live WordPress/social calls, no waiting spinner and no deliberate HTTP/network failure. This specifically tests an empty response, not a disconnected device.

**Expected real UI:** Use the existing feed container and an appropriate real VVP empty-state component (`EmptyComponent` is an inspection lead). It may require proper empty-state handling at the fetcher/render boundary. Don't replace the whole application view with a static poster.

**Test intent / checks:**
- Meaningful, deterministic empty-state title/message/graphic (if any) positioned consistently; app header/navigation remain intact.
- State exits loading reliably; no lingering skeleton, spinner, old cached cards, announcement, test fixture article or stale list item.
- Reopening or rerunning after another scenario should not leak previously cached content.
- Differentiate **zero items** from **loading/error/offline** in code and test naming.

**Suggested selector:** `qa-empty-feed-ready` on the rendered empty-state region, emitted only after successful-empty completion.

**Done when:** app displays its real successful-empty state from injected fixture data, repeatable capture, approved golden and passing comparison; a normal non-empty fixture can still render afterward.

## 4. Scenario matrix and baseline partitioning

| Scenario ID | Data condition | Theme | Primary visual unit | Separate golden? | Status |
|---|---|---|---|---|---|
| `long_headline` | Long headline + fixed local image | Light/pinned current contract | Real article-card element | Existing, if already approved | Existing Appium implementation **reported** |
| `breaking_news` | Urgent banner + stable feed content | Light | Banner (and context if warranted) | **Yes** | To implement |
| `dark_article` | Same deterministic article as existing test | **Dark** | Real article card | **Yes** | To implement |
| `no_image` | Article without featured media | Light | Real article card | **Yes** | To implement |
| `empty_feed` | Successful feed result = `[]` | Light | Empty-state/feed region | **Yes** | To implement |

**Baseline naming:** Match the real repository's existing layout. Example only:

```text
qa_visual/
  baselines/android/pixel10-api37/
    long_headline.png                  # existing; do not overwrite
    breaking_news.png
    dark_article.png
    no_image.png
    empty_feed.png
  artifacts/android/pixel10-api37/     # actuals, diffs, JSON, diagnostics; ignored
```

If the profile name does not capture **theme, locale, font scale, OS/API and screen geometry**, record those in an accompanying pinned environment manifest/test metadata. Keep Android/iOS goldens separate even if the fixture schema is shared. Exact folders/filenames should follow the existing implementation, not force an unnecessary migration.

**Important:** The count of *five scenarios* does **not** necessarily mean only five screenshots: some may have a contextual diagnostic screenshot. Only intentional assertion images become goldens. Avoid a full-screen golden if a stable cropped component catches the intended regression more precisely.

## 5. Fixture and runner design: extend, don't rebuild

### Fixture contract

Prefer one typed catalog/registry for scenario selection, e.g. `long_headline`, `breaking_news`, `dark_article`, `no_image`, `empty_feed`, selected via existing `EXPO_PUBLIC_QA_SCENARIO` under `__DEV__`. Shared synthetic article builders can override only the fields under test:

- **Common:** article IDs, headings, publication time, author, category, summary, bundled static assets, sort order, feed selection, and stable locale.
- **Breaking:** explicit banner payload/content and display flag; stable banner ordering.
- **Dark:** same article payload; explicit QA appearance state.
- **No image:** nullable featured media (not a failed remote image).
- **Empty:** successful empty posts list and completed-loading state.

Keep QA-only data selection disabled in normal release/production builds. Explicitly avoid external network and app-level asynchronous side effects where they can alter the captured UI. Do not introduce a mock HTTP server simply because we are adding scenarios; the already-approved in-app fixture seam is sufficient if it covers the target states.

### Appium/pytest design

- **Reuse:** existing Appium session fixture, Android adapter, image comparator, golden lookup, JSON/diff reporting and helper that validates ready + captures element screenshot.
- **Parameterize carefully:** scenario selection/capture can be data-driven, but **not** at the expense of reliable Metro/app restart and clean fixture state. Env variables exposed to Metro may be read at bundle start; switching them from pytest does not necessarily update an already running app. Confirm real lifecycle and use a deterministic start/reload contract. If scenario switching requires separately started Metro sessions, document and orchestrate that honestly rather than claim one `pytest` command automatically changes four runtime scenarios.
- **Selectors:** unique, non-overlapping `testID`s exposed through UiAutomator2; fail with diagnostics if selector or readiness is absent. No blind `sleep()` as the primary synchronization mechanism.
- **Isolation:** clear/reset only the state that affects screenshots (feed caches, theme selection, announcements, persistence) and preserve reproducibility across test order. Validate both individual scenario runs and the whole suite.
- **Capture geometry:** compare the intended element/region, not inconsistent emulator status bars; record screenshot dimensions and reject shape mismatches.
- **Visual comparison:** keep existing channel tolerance/changed-pixel threshold unless repeatability evidence supports a scoped change. Never loosen thresholds to hide a real UI issue.

## 6. Incremental execution plan for the coding agent

**Gate 0 — inspect and protect the existing implementation**

1. Read current `AGENTS.md`, `CLAUDE.md`, `docs/02_DECISIONS.md`, `docs/03_HANDOFF.md`, relevant `04_AI_PROMPT_LOG.md`, `app/` fixture/theme/feed components, and the **actual installed** `qa_visual/` code and README.
2. Record repository status/branch and current package commands. Confirm current `long_headline` test source, selection contract, baseline path, whether golden exists, its last verified PASS, and any intentionally failing demonstration. Do not rely on the older starter ZIP's outdated directory paths.
3. Pin and record emulator/device and session information; confirm Pixel_10 4 GB setting and software rendering if currently used. Preserve existing goldens, fixture patch, and production behavior.
4. If the current test is already passing, run it as regression guard. If not, do not start changing multiple components until its status is understood.

**Increment 1 — `breaking_news`**

Inspect real feed and announcement path → add development-gated banner fixture + minimal real UI extension → add stable testID/readiness → Appium capture → repeatability check → human-reviewed golden → PASS/failure artifacts. Preserve headline baseline.

**Increment 2 — `dark_article`**

Prove theme-control mechanism → pin dark appearance without leaking state → reuse article fixture/component → dedicated dark golden → verify light case still passes.

**Increment 3 — `no_image`**

Add absent-media fixture → conditionally render real card without image → independent readiness from image load → capture + golden → verify existing image case.

**Increment 4 — `empty_feed`**

Inject successful empty result → ensure loading/cached-feed isolation → render existing empty-state region → capture + golden → verify re-entry to populated feed.

**Final regression sweep**

Run every scenario from a known state; verify repeatable captures and overall suite; capture **one deliberately introduced UI regression** with failing diff and restoration to passing state (the existing long-headline example may already satisfy this; do not manufacture another if evidence exists). Update README with exact checked commands to run individual/all tests, select fixtures, and intentionally regenerate goldens **only with review**. Record environment pin, commands, outputs, failures and limitations. Update project handoff and **material** AI prompt disclosures; routine debugging chat need not be logged verbatim.

### Per-increment acceptance gate

- [ ] Scenario uses real rendered app UI and fixed synthetic data/assets.
- [ ] QA-only activation and production/non-QA behavior are preserved.
- [ ] Explicit ready condition, no network/animation/cached-state surprise affecting the capture.
- [ ] Two same-environment captures agree within the existing tolerance.
- [ ] Human reviews the actual PNG **before** approving a new golden.
- [ ] Appium assertion passes against that approved reference; actual/diff/JSON saved on failure.
- [ ] Existing `long_headline` test remains passing; no accidental baseline overwrite.
- [ ] Changed files, commands and results are recorded with truthful evidence.

## 7. Decisions, trade-offs, and non-goals

| Decision | Rationale | Trade-off / guardrail |
|---|---|---|
| Four **different UI risks**, not many headline permutations | Better representative newsroom coverage | More fixture states, baseline maintenance; keep scope capped |
| Appium + existing Python comparator | Real Android rendering and shared cross-platform high-level test intent | Slower than native component snapshots; keep PR suite small |
| In-app development-only fixtures | Already proven route to real article UI; no backend service to run | Must control app lifecycle, theme, caches and startup side effects |
| Minimal breaking-banner extension | Directly relevant to employer's suggested feed | Disclose that it is added to the sample app, not a verified upstream feature |
| Real theme and real optional-media states | Tests product behavior, not synthetic image manipulation | Could require small robust app changes; inspect before editing |
| Successful empty feed, **not** offline/error | Distinct visual state with low test data complexity | Does not demonstrate offline behavior; name it accurately |
| Separate approved references | Avoid accidental baseline drift and masking regressions | Requires deliberate human review for every UI change |

**Explicit non-goals for this expansion:** paywall/premium entitlement logic, live ticker, video/ad rendering, dynamic type matrix, multiple AVD/OS/device profiles, paid visual-testing service, native iOS execution, and wholesale framework rewrite. These are possible future risk-based scenarios, **not** implied deliverables or claims.

## 8. CI and cross-platform implications

For a CI-oriented presentation, the five Android tests form a targeted visual smoke suite on a **pinned emulator + deterministic QA build/fixtures**. Unexpected diffs fail the job and retain actual/reference/diff/metrics/log artifacts. New goldens are changed only through reviewed commits; a failing build must **not** self-heal by replacing its baseline. Wider device/theme/OS coverage belongs in nightly/release suites if justified by cost and defects.

For iOS, keep the same **scenario names, synthetic article/empty/banner contracts, visual test intent, comparison/report conventions and baseline review policy**, while using a macOS simulator, Appium XCUITest and **distinct platform selectors/goldens**. This is **strategy scope** until actually implemented and run; don't claim equivalent iOS execution from the Android suite.

CI workflow files are not proof of passing CI. Report actual successful runs only after observing them.

## 9. Handoff instructions for the existing implementation thread

**Instruction to the implementation agent:**

> Treat this document as the human-approved **test-scenario expansion decision**. The candidate confirms `long_headline` is already implemented in Appium. Do **not** reopen SUT or main runner selection. First inspect the actual current repository and reconcile any differences with this document. Preserve existing fixtures, goldens, test interfaces and production behavior. Implement the four scenarios in the agreed order as bounded, reviewable increments. Present source-level findings and any needed deviations, then verify each with real native screenshots and Appium evidence. Never auto-accept a golden, claim native iOS or CI success without execution, or add paywall functionality as part of this scope.

**Suggested first response in that thread:** concise inventory of current test/fixture files; implementation feasibility and any necessary modifications for all four scenarios; order of work; first proposed incremental patch. **Do not** start by recreating the prior strategy from scratch.

**Document management:** Add this as a *new* project/repo document at `docs/08_VISUAL_SUITE_EXPANSION_DECISION.md`. In the implementation thread, reflect the accepted scope in `02_DECISIONS.md` and after each work session update `03_HANDOFF.md` with actual status and verification. Those source-of-truth updates require complete revised Markdown copies if maintained as ChatGPT Project Sources; creating this file does not automatically update those uploaded sources.

---

## 10. Final state summary

**Approved now:** one existing `long_headline` scenario plus new `breaking_news`, `dark_article`, `no_image`, `empty_feed` scenarios, using the same Android Appium/Python screenshot-test framework and deterministic VVP QA fixture approach.

**Not yet established by this decision document:** the latest repository state, implementation of the four new scenarios, their reviewed baseline PNGs, test PASS/FAIL evidence, repeatability measurements, native iOS coverage, or a passing CI job. Verification belongs in the current execution thread.

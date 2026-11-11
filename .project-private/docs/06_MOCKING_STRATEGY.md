# Planning task 2 — Deterministic mock-data injection

> **Active `vvp_app`-first inspection (2026-11-01):** human authorized a bounded SUT/mock feasibility spike; neither fixture-provider nor HTTP mocking has been approved. Earlier JetNews-first mock examples below are reference options, not the active default.

**Status:** OPEN; choose jointly with SUT, *before* automating screenshots. This is not the same as screenshot capture: **Appium drives the app but does not replace API responses by itself.**

## Requirement from PDF

Employer's worked examples construct real UI with fixed fixture models. Its alternative running-app path specifically allows **(a) local mock server/embedded stub** or **(b) launch argument/build flavor switching app data to fixtures** (PDF p.3). Production APIs and employer source are not supplied.

## Three implementation patterns (choose one primary)

| Pattern | Mechanism | Good fit | Risks |
|---|---|---|---|
| **A. Test-only fixture repository** (**provisional default**) | In test build, app data provider returns bundled synthetic models/assets | Existing repository/provider seam or React Native shared application logic | Requires SUT source changes, test-only routing, isolation from release build |
| **B. Local mock HTTP API** | Test configuration points API base URL to WireMock/embedded service; responses come from versioned JSON | Existing network-facing app, separate Android/iOS apps can share API contract | Emulator-host networking, HTTPS/auth, API coupling, images, startup synchronization |
| **C. Network interception/proxy** | Replace live responses with local fixtures | App API cannot easily be configured but interception is supported | TLS pinning/certificates, unstable CI, complexity; fallback only |

**Don't** modify the production content server. **Don't** build a separate fake UI instead of the real component. Using manually fabricated PNGs as expected and actual screenshots is invalid.

## Shared fixture contract (proposal, not yet code)

```text
fixtures/
  breaking_news.json
  long_headline.json
  premium_article.json
  assets/
    fixed_teaser.png
```

A fixture record should be a controlled model with stable IDs, article type, headline, preview, premium badge, absolute timestamp or relative-time formatter override, fixed local image ID, and explicit `state` (loaded/error/offline as relevant). Use synthetic content and assets.

**Example** (illustrative, app schema will differ):

```json
{
  "id": "article-001",
  "type": "breaking",
  "headline": "Beispiel: Eine lange deutsche Schlagzeile für den Layouttest",
  "publishedAt": "2023-11-14T12:00:00Z",
  "premium": false,
  "imageAsset": "fixtures/assets/fixed_teaser.png"
}
```

## Appium ↔ mock control contract

Test automation must select a **known scenario** deterministically. Options, depending on SUT:

- Test-only deep link or launch argument (`newsapp-test://feed?scenario=breaking_news`).
- Build flavor / environment pointing the app at a deterministic repository.
- Local mock service reset-and-select endpoint before each test (`POST /__test/reset`, `POST /__test/scenario/{name}`), accessible to emulator and runner.

These are **design patterns**, not existing endpoints or proven SUT capabilities. Never expose test-control endpoints publicly or in a production release. The scenario should be visible through a stable UI-ready signal or accessibility ID rather than `sleep(5)`.

## Mocking validation gates

1. **Data reaches real UI:** change fixture headline → observed rendered text changes; no duplicate/mock UI.
2. **Live API isolation:** tests use fixed fixtures even if actual news server changes or is unavailable. Ideally validate by blocking external network access after fixture selection.
3. **Repeated run:** same device/build/fixture gives equivalent screenshot on consecutive runs within documented comparison tolerance.
4. **Scenario isolation:** each case resets app/mock state; `premium` does not leak into `breaking`.
5. **Render stability:** pinned timestamp/timezone, locale, font/density/theme, deterministic images/ads, disabled animations, explicit loading completion.
6. **Cross-platform plan:** share scenario IDs and fixture/schema where practical, but injection can be a small platform adapter in separate native apps.

## Proposed test matrix (start tiny)

| Scenario | Data-controlled state | Visual risk |
|---|---|---|
| `breaking_news` | Breaking banner, fixed headline/time | Padding/contrast/regression |
| `long_headline` | Long German headline, image present or absent | Truncation/wrapping |
| `premium_article` | Premium true, badge/paywall teaser visible | Badge missing or incorrect placement |

For a 1-day demo, **one fully verified end-to-end fixture/screenshot cycle is more valuable than three incomplete scenarios**. Expand only after it passes.

## Evidence to keep

Selected seam file/path; fixture JSON; exact test-only mode invocation; running UI screenshot; baseline PNG; diff output; log of data isolation/repeatability check. Record what was verified and what was only designed.


---

## 2026-11-01 coupled mock design — source-informed, NOT implemented

### Option A (recommended for JetNews): test-only fixed `PostsRepository`

**Observed existing boundary:** `FakePostsRepository` implements `PostsRepository`; its `getPostsFeed()` supplies `posts` to existing `HomeScreens.kt` components (`PostListTopSection` / `PostCardTop`, `PostListSimpleSection` / `PostCardSimple`). It currently has a simulated 800 ms delay and every-fifth-request failure. That behavior must be removed/bypassed for screenshot mode, not mistaken for deterministic success.

**Proposed path, not existing feature:** `test scenario ID` → **test-only** app configuration/`AppContainer` repository selection → `ScreenshotPostsRepository(scenario)` returns a named `PostsFeed` with synthetic strings/assets → existing home UI → explicit ready marker → screenshot. Confirm actual `AppContainer` wiring after checkout. Keep release builds unable to enable this mode. Use one fixed scenario per fresh app session or an isolated reset hook; no per-test mutable global state. Initially use native Kotlin builders that match the existing model rather than introducing JSON parsing just to claim reuse; keep portable scenario descriptions/fixture contract in JSON if needed by future iOS adapters.

**Proposed scenario-control tradeoff:**
- Appium running-app mode: optional debug-only launch intent extra (`screenshotScenario=breaking_news`, implementation/behavior **does not exist yet**) with a stable UI-ready accessibility marker and verified Compose tag mapping.
- Native component snapshot mode: instantiate real `PostCardTop` or other existing Composable directly with fixed `Post`/`PostsFeed` data, bypassing launch control. Prefer this if emulators block delivery.

**First two target cases:** (1) highlighted post with controlled German headline/image; (2) long German headline via existing recommendation card. A true **breaking** banner or **premium** badge requires limited UI adaptation and must not be falsely described as already present. Add third only after one end-to-end golden and comparison passes.

**Validation:** prove changing only a fixture headline changes the UI text; no production API calls in test; repeat two captures in one pinned environment; reset favorites/cache; control locale `de-DE`, timezone, clock/relative timestamps, fonts, theme, fixed local asset, transitions, font scale, density, window/status bars. A `ready` marker is required; no blind sleeps.

### Option B (`vvp_app` conditional): provider override or mock HTTP API

Source confirmed only that `vvp_app` is Expo/React Native with a separately published server repository; **the app's actual fetch path and configurable base URL are unverified**. First trace a specific article list screen → hook/service/API client → response mapper → card component. Prefer test-only provider/cache injection if easy; otherwise a mock server with a test-only base-URL override and fixed JSON/assets. Account for emulator host routing, auth, TLS, remote images, WebView/embedded content, React Query caches/animations and error/offline states. Do **not** claim mock HTTP is already supported; do not rely on packet interception/TLS proxies by default.

### Selection rule

- **Approve no mock until source-to-view trace and a viable scenario control method are agreed.** JetNews + test-only repository is the provisional preferred *SUT + mock pair*.
- For independent iOS/Android codebases, share **scenario identifiers and data semantics**, not necessarily fixtures' internal class shapes or injected provider implementations.
- Synthetic data and bundled image assets are non-negotiable for clean references/reuse rights. Never re-record goldens automatically during verification.

**References:** JetNews source `FakePostsRepository.kt` and `HomeScreens.kt` linked in `05_SUT_SELECTION.md`; employer PDF p.3 permits both fixture replacement and mock HTTP servers.

---

## Active `vvp_app` mocking feasibility (2026-11-01, NOT APPROVED)

**Human has prioritized inspecting `vvp_app`, not selected a mock mechanism.** GitHub root documents React Native/Expo and `.env`; F-Droid describes a fixed distributed backend dependence. Actual source fetch/hook/client/component boundary is **still unknown**. Do not claim endpoint override, repository injection, or a named deep link is already supported.

### Two leading alternatives, assessed only after source trace

**A — Test-only in-app fixture provider (provisional preference if low change):** Trace feed screen → hook/query/state provider → article models → unchanged real component. In a **test build/config**, substitute that provider/cache with versioned synthetic articles and local assets. Named scenario selection might be launch argument/deep link/test-only config, provided the app's router supports it or a tiny controlled seam can be added; reset query caches, persisted favorites and timestamps between runs. Good: same React Native source path can potentially serve Android and iOS without mock server/network. Risk: app architecture may intertwine client/cache/UI; needs evidence and leakage prevention. No actual provider file identified yet.

**B — Local mock HTTP service (conditional only):** Use this only if the source reveals one central configurable API client or a small test-build base-URL override. Simulate the real response schema and bundled/local images, isolate auth/push/analytics, reset scenarios, route emulator to the mock service, and forbid live fallback. F-Droid's end-user non-configurability means a working source-level override **must be demonstrated**, not assumed. Risk: Android emulator/host networking, TLS, non-API image URLs, production hooks and asynchronous loading.

**Avoid** network interception/TLS proxy as primary plan: higher short-deadline and CI flakiness risk. Avoid testing static PNGs/Jest JSON snapshots as though they were native app screenshot goldens. An Expo web screenshot is also not an Android-native proof.

### Minimum fixture contract — proposal only

- `scenario_id`: `long_headline` first (easiest existing card state if present); `breaking_news` or premium only if real UI support/adaptation is safe.
- Fixed synthetic article ID, long German headline, paragraph, absolute timestamp, `image` mapped to bundled custom fixture, and explicit loaded/failed state. Premium/breaking flags only if UI supports them; do not invent existing badges.
- Test-only startup/reset signal and stable `testID`-based UI-ready marker, when achievable; no blind fixed sleep. Force `de-DE`, fixed theme/font scale/density/window, fixed time/relative timestamp formatting, animations off and no remote media.
- Validate a two-value fixture text swap **in the same existing component**, no live feed calls, clean repeat screenshots, and no cache contamination. No test code, fixture file or proof exists yet.

### Architecture exit gate

Require exact repository SHA and source paths for model/provider/API client and visual card, then ask the human for **one coupled SUT + mock + runner implementation approval**. If no low-change path emerges within the bounded spike, report the blocker and pivot recommendation to JetNews/owned sample; do not force `vvp_app` just for shared React Native code.


---

## `vvp_app` source-traced mock proposal — 2026-11-01 (NOT IMPLEMENTED)

The uploaded exact-commit archive **resolves the earlier API-boundary uncertainty**. Main news article data comes from configured WordPress sites via `WordPressAPI.create(entry.handle)` → `WordPressFetcher.createFetchers(api)` → `mapArticleToPost` → `Feed`/`GenericPost` → existing `ArticlePost` React Native UI. **FOSS-only `getApiUrl()` redirects `ServerAPI` only**, not these WordPress clients. Source evidence is sufficient to propose the seam; no injected fixture has been run.

### Option A (recommended if Android builds): test-only feed provider / fetcher injection

- Keep `ArticlePost`, `GenericPost` and `Feed` intact. In a test-only/debug build, provide a deterministic fetcher through the `HomeScreen` `feedprops.fetchers` / `WordPressFetcher.createFetchers` boundary. Return fixed `LoadArticlePostProperties` objects (see `src/types/posts.ts:35-69`), optionally using the **existing** `WordPressFetcher.mapArticleToPost()` conversion to guarantee the real component path.
- Use one explicit scenario ID (`long_headline` first), fixed article id/slug/date, long synthetic German headline, excerpt, category and author, and deterministic local imagery. Bypass all other WordPress/Instagram/YouTube/etc. fetchers for this test mode, rather than assuming mock overrides their URLs. Never enable test fixtures in production releases.
- `ArticlePost.getImages()` separately calls `WordPressAPI.getFeatureImage` if `_links["wp:featuredmedia"]` exists; therefore a fixture must deliberately supply a **controlled static image path** or an explicit deterministic no-image state, not rely on a remote URL or animated loading GIF. The exact no-image rendering/static asset implementation needs design/verification during EXECUTION. Also disable/replace view-count network, audio/background activity, announcements, changelog and permissions where necessary; clear saved reading-progress/cache and fix theme/font/locale/window/animation.
- Suggested scenario selection is build-time test flag plus one selected fixture per clean app session; test-only launch/deep-link parameter is an option if Expo Router and the runner can select it reliably. Neither control exists today. Add a unique card `testID` and an explicit ready marker **after** data, fonts and assets settle; `article-progress-bar` by itself is insufficient. The test must show changing just the fixture headline changes actual `ArticlePost` text, with no live API fallback.
- For an even narrower first proof when HomeScreen startup/other feeds are hard to isolate, a **debug-only preview route** mounting the **unchanged actual** `ArticlePost` with fixed props is valid under the employer's representative-component example; it does not exercise the complete feed network pipeline. Label that narrower coverage transparently.

### Option B (secondary): WordPress HTTP mock

- Requires an additional **test-only WordPress base URL/client override** for every enabled WordPress `entry.handle`, or a test-only API constructor. Existing `src/helpers/apiUrl.ts` HTTPS-only FOSS UI override is for a separate auxiliary backend and is **not sufficient**.
- Must provide deterministic `/wp-json/wp/v2/posts` JSON, WordPress media metadata (`getFeatureImage()`), actual image bytes, pagination/search if exercised, emulator-host routing/HTTPS setup, and block unmocked social/news dependencies. Higher setup cost and API-contract value. Do not use TLS proxy as a time-saving assumption.

**Recommendation for approval after successful native build:** `vvp_app` + A, one `long_headline` scenario on Android, real rendered existing `ArticlePost`, platform-specific golden and deliberate failed diff if achievable. Runner still OPEN (Appium/pytest vs Maestro). No project source modification in this checkpoint.

---

## 2026-11-01 — bounded `vvp_app` fixture spike: patch prepared (LATEST)

**Authorization is scoped to a feasibility experiment, not a final architecture decision.** The assistant prepared `vvp_qa_fixture.patch` for user application on pinned commit `8b421753a17a18cd648447319adcca61a288f97f`. The native live app renders per user; the patched fixture mode has **not yet run** on the user's emulator.

**Proven code seam (source):** `HomeScreen` can pass only `{fetcher: qaFeedFetcher}` into existing `Feed`; `qaFeedFetcher` calls `WordPressFetcher.mapArticleToPost` on fixed `LoadArticlePostProperties`, leading through `GenericPost` into the **real** `ArticlePost`. There is no parallel mock-card UI. The QA-only path is conditional on `__DEV__ && EXPO_PUBLIC_QA_SCENARIO === 'long_headline'`; normal production feed selection remains unchanged otherwise.

**Prepared deterministic boundaries:** fixed synthetic German long headline, author, `2026-10-12` timestamp, ID, slug, excerpt; a generated local 1200×615 PNG used by the real article image component; no media metadata HTTP; no social/WordPress home fetchers; no in-feed announcement, article view-count, share bar or reading-progress restoration for fixture article; no notification request/changelog overlay. Readiness `testID` after local image `onLoad`, title `testID`. Date rendering uses fixed absolute date rather than current-relative formatting. No application setting or secret is required to enable scenario apart from the environment variable.

**Evidence still needed:** patch application result; full project `pnpm check:ts`; Metro bundle; fixture headline and image actually visible on native emulator; no unexpected root network/debug toast; repeated render and headline change; driver-selectable test IDs; golden/diff. The patch does *not* prove complete application-wide offline behavior. Do not claim production-safe isolation until platform build/guards are exercised and reviewed.

**Next:** collect Windows proof and obtain combined SUT/mock/runner/scope sign-off; maintain alternate fallback if the fixture render or tooling fails within deadline.

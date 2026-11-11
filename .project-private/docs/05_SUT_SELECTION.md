# Planning task 1 — Finalize the system under test (SUT)

> **CURRENT PLAN OVERRIDES EARLIER PRIORITY:** On 2026-11-01 the human approved **`vvp_app`-first bounded feasibility**. Earlier JetNews-first sections below are retained as historic comparison. SUT + mock + runner decisions remain OPEN; see active runbook at bottom.

**State:** OPEN. This is the first planning activity, **before** choosing Appium or a native screenshot tool. The selection must prioritize fixture control and runnable native UI over aesthetic similarity.

## Selection goal

Find an app whose **actual rendered UI** (existing component/screen) can show predictable synthetic news content without calling a live backend during tests. An adapted open-source app or small sample app is explicitly permitted by employer PDF p.4. The employer's own codebase is unavailable.

## Candidates, not recommendations until verified

| Candidate | Why inspect | Main uncertainty / risk | Initial role |
|---|---|---|---|
| [JetNews](https://github.com/android/compose-samples/tree/main/JetNews) | Native article/feed UI with a plausible component-test seam | Build/Kotlin/Gradle and where fake data is injected; no iOS demo | **Candidate A** |
| [Volksverpetzer `vvp_app`](https://github.com/Volksverpetzer/vvp_app) | Actual journalism app with React Native shared UI; relevant to cross-platform vision | Expo/Android launch, API/auth/images and how to swap data; maintainers' license/build docs to confirm | **Candidate B** |
| [Now in Android](https://github.com/android/nowinandroid) | Illustrates existing fake data + screenshot CI concepts | Larger app; already includes tests; hard to show novel work | **Architecture reference** |
| [Kotlin KMP production RSS sample](https://github.com/Kotlin/kmp-production-sample) | Shared logic with platform-specific UI illustrates portable fixture contract | Complex build; limited time | **Research reference only** |
| Tiny owned news sample | No third-party build/injection uncertainties; full control | Less impressive real-world integration story | **Deadline fallback** |

These are **research leads from earlier conversation**, not claims of successful build, licensing clearance, or tested mock injection. Check README and license before reuse. If using a third-party repository, document attribution and modified source; don't publish the employer PDF.

## Feasibility gate: test at most two candidates

Perform a bounded spike (target **60–90 minutes total per promising candidate**, shorten if trouble appears; do not lose the demo deadline). Capture actual commands/results in `docs/03_HANDOFF.md`.

1. **Toolchain:** Confirm host Windows, Android SDK/adb, emulator/Java/Node/pnpm versions as needed. Check actual commands, don't infer readiness from earlier projects.
2. **Real UI:** Find a specific breaking-banner/teaser/article component and where it obtains data. Name the path.
3. **Mock seam:** Is there a repository/service/provider, a base-URL override, or a component fixture constructor? Identify exact files/entry point. Prefer no invasive production UI changes.
4. **Run:** Can a test build or component render locally without credentials and unstable network dependencies? Record launch command and observation.
5. **Determinism:** Can we substitute fixed headline/date/image and force one visual state on demand? Demonstrate from the rendered UI, not just a JSON file.
6. **Automation:** Can automation target a stable screen/element and obtain a screenshot? If Appium candidate, check accessibility/test IDs and runtime prerequisites.
7. **Reuse permission:** Verify repository license/attribution and no copyrighted news assets/credentials in committed fixtures.

### Scoring rubric (0 = fails, 1 = uncertain/work, 2 = demonstrated)

| Criterion | Weight | Why |
|---|---:|---|
| Runnable native Android UI under current environment | 3 | Must deliver working demo |
| Clean deterministic data injection | 3 | Employer's core requirement |
| First automated screenshot obtainable | 3 | Proves vertical slice |
| Setup and debugging effort within deadline | 2 | Time risk |
| News UI scenarios with stable assets | 2 | Credible challenge examples |
| Path to cross-platform reuse | 1 | Strategy must cover iOS; demo only one |
| Maintainable/attributable code and license | 1 | Safe public sharing |

**Hard reject:** cannot run native UI; no workable fixture seam; needs credentials; must use live changing content; takes disproportionately long to build. The scoring is planning aid, not a license to ignore hard rejects.

## Minimum useful SUT slice

- Existing **feed or article card** UI with one breaking state and one premium/long-headline state (aim for three scenarios if trivial).
- Named deterministic fixture selection (`breaking`, `long_headline`, `premium`).
- Fixed text, timestamps, images/assets, font/theme, system device configuration.
- Explicit *UI-ready* condition so Appium doesn't capture a loading state.
- One successful baseline capture, comparison and preferably one deliberate visual-regression diff.

**Decision output:** selected repository/path, mock injection seam, screenshot runner feasibility, fallback, approval. Record in `docs/02_DECISIONS.md`, not only in chat.


---

## 2026-11-01 read-only repository feasibility assessment (NEW; no runtime proof)

**Status:** Public README/source inspection completed. No app checkout/build/emulator test, fixture change, native screenshot, or license-asset audit executed on the candidate's Windows machine. The source inspection is **not** an implementation approval. Reference branches must be pinned to commit SHAs after checkout.

| Criterion | Google JetNews (`android/compose-samples/JetNews`) | Volksverpetzer `vvp_app` |
|---|---|---|
| Source/build | Native Kotlin/Compose independent `JetNews` Gradle project with wrapper (`gradlew.bat`). README: import in Android Studio; `connectedCheck`/`testDebug` documented. Windows JDK/SDK/Gradle sync **not validated**. | React Native/Expo/TypeScript app with `pnpm-lock.yaml`, `.nvmrc`, Expo configs and EAS profiles. README specifies Node **24.x+**, pnpm, `pnpm install`, `pnpm android`; development/standalone build differences. `.env.sample` appears in repo while README text refers to `.env.example`: inspect, do not assume configuration. Android native build **not validated**. |
| Data seam | **Confirmed source-level:** `PostsRepository` abstraction and `FakePostsRepository.kt` that serves hardcoded `posts`. `getPostsFeed()` injects artificial `delay(800)` and deliberately fails **every fifth request**. Replace/parameterize for screenshot runs. `PostsData.kt` is indicated as static model data (verify on checkout). | Repo and separately listed `vvp_app_server` suggest a network data path, but **exact article fetch function, API URL override, auth needs and image fetch paths NOT verified**. Do not assert an injectable API seam until traced to rendered screen. |
| Real UI | `HomeScreens.kt` renders `postsFeed.highlightedPost` via `PostListTopSection` → `PostCardTop`, and `recommendedPosts` via `PostListSimpleSection` → `PostCardSimple`. **Existing highlighted post is not automatically a breaking-news banner**; premium badge is not confirmed. | Published real journalism app, React Native screen/component source exists, but exact target card component/route has not been traced. |
| Selectors | `HomeScreens.kt` inspected; no `testTag` string found in this file. For device automation add a limited `Modifier.testTag` at target component + root `testTagsAsResourceId` or evaluate UiAutomator2 `mapTestTagToResourceId`. Inspect accessibility tree before declaring stability. | React Native `testID`/accessibility labels for article card and ready state **not verified**. Must inspect and potentially add small test-only/stable identifiers. |
| Rights | README states Apache-2.0. Retain license/attribution, audit `JetNews/ASSETS_LICENSE`, and use synthetic image/text fixtures (do not blindly republish sample art). | GitHub identifies code as MIT. Retain license/attribution. **Editorial photos, article text, logos, branding and third-party asset rights separately unverified**; use synthetic assets and neutral branding in deliverable unless cleared. |
| Android screenshot estimate, **not measured** | ~1–3 h **after** functional Android SDK/Gradle/environment is available, dependent on dependency downloads and selector/mock work. | ~2–5+ h **after** toolchain available; Expo/native modules and network seam may dominate. |
| iOS relevance | Written iOS strategy requires separate implementation/adapter, which employer permits. | Genuine shared RN view implementation is a plus if an Android native build and fixture seam can be proven; does not make native iOS setup or baselines free. |

**Evidence URLs (reviewed online, not locally built):**
- JetNews README: https://github.com/android/compose-samples/tree/main/JetNews
- JetNews existing repository: https://github.com/android/compose-samples/blob/main/JetNews/app/src/main/java/com/example/jetnews/data/posts/impl/FakePostsRepository.kt
- JetNews feed UI: https://github.com/android/compose-samples/blob/main/JetNews/app/src/main/java/com/example/jetnews/ui/home/HomeScreens.kt
- vvp app README and source tree: https://github.com/Volksverpetzer/vvp_app (public page displayed `prerelease` as selected branch during review)
- Android UiAutomator–Compose tags: https://developer.android.com/develop/ui/compose/testing/interoperability
- Appium driver tag setting: https://appium.github.io/appium-uiautomator2-driver/latest/troubleshooting/

### Feasibility outcome / recommendation (not approved)

**Provisional lead: JetNews** because the repository seam and real feed rendering are supported by actual source-level evidence, rather than a presumed remote API replacement. **Conditional alternative:** `vvp_app` only if one bounded source trace identifies the real article fetch path, fixed-data substitution, and Android launch quickly. **Deadline fallback:** a tiny owned Android news app (production-like actual Compose UI; fixture provider, no fake PNG rendering). Now in Android remains architecture reference, not a third competing spike.

### Bounded spike to request human authorization for (maximum ~90 min)

1. **0–15 min, Windows environment inventory (non-invasive):** `git --version`, `java -version`, `adb version`, `adb devices -l`, `emulator -list-avds`, `node --version`, `pnpm --version`, `python --version` as applicable; inspect `ANDROID_HOME`, SDK, virtualization, disk, Android Studio and available Android device/emulator. Capture missing commands/errors instead of assuming availability.
2. **15–55 min, JetNews first:** clone/pin SHA; inspect `PostsRepository`, `FakePostsRepository`, `PostsData`, container wiring and target Composable; attempt Gradle sync/build and emulator launch **only if spike authorized**. Trace scenario selection point. No automation framework adoption here.
3. **55–80 min, conditional `vvp_app` check:** only if JetNews fails hard or the user prioritizes true shared RN views, inspect install/config and trace the network/data response into a specific real card; stop quickly on undocumented auth/remote service/native build blockers.
4. **80–90 min, decision evidence:** record commands, versions, failures, start-to-screen, screenshot feasibility, identified fixture injection and rights. Present SUT + injection + runner decision once; no additional development without approval.

**Strict gates:** real UI launch or feasible off-device render; named deterministic fixture in real component; clear copyright situation; no required live news API. Do not give a 2/2 rubric score for something that was only found in source—runtime, fixture and screenshot are **UNVERIFIED**.

---

## Active spike — `vvp_app` FIRST (human-directed; 2026-11-01)

**Supersession:** The prior JetNews-first 0–90-minute schedule and JetNews preferred selection above describe *earlier research* only. The human explicitly authorized `vvp_app` priority for this bounded PLANNING spike, not a final SUT decision.

### Public evidence versus unknowns

| Dimension | Supported by public source | Must verify locally / in exact source |
|---|---|---|
| Platform and setup | Expo + TypeScript, Node **24.x+**, pnpm, `pnpm install`, `pnpm start`, `pnpm android`, EAS/local APK profiles (GitHub README) | Working Android SDK/JDK, native module installation, emulator, build time/error, local app launch, exact checkout SHA |
| Repo configuration | Root lists `.env.sample`; README says `.env.example`, and `APP` selects Volksverpetzer/Mimikama | Real tracked env template and non-secret required values; build credentials/Expo account requirements; **do not print `.env` secrets** |
| Backend | Public F-Droid metadata says distributed app depends on `volksverpetzer-app.de`, with no configurable service exposed to end users | Source-level URL/client and whether changing build config or replacing a query/data provider is simple; REST vs other transport not yet proven |
| UI and selectors | Actual published news reader and React Native UI code; official RN/Maestro docs support `testID` as a mechanism | Exact feed/card component, screen route, `testID` values, UI-ready event, deterministic image loading |
| Reuse rights | GitHub labels source code **MIT** | Confirm tracked LICENSE/notice; don't assume that trademark, logos, live article text/photos or remote media are covered |
| Running app proof | F-Droid distributes Android releases, not a local demonstration | Actual debug build on candidate Windows PC and real screen with source pin and deterministic override |

**Current source-access limit:** GitHub root and README opened publicly; GitHub web child `/tree/prerelease/src` and direct raw source URL returned cache misses. Assistant's container `git ls-remote` failed DNS (`Could not resolve host: github.com`); this does **not** reflect the candidate's Windows connectivity. The exact data seam **is not identified**; don't invent paths, `testID`s, endpoints or a working mock.

### Bounded 90-minute Windows feasibility runbook (no implementation)

**0–15 min — prerequisites and checkout.** In Windows PowerShell, outside any existing project, run:

```powershell
node --version
pnpm --version
git --version
java -version
adb version
adb devices -l
emulator -list-avds
$env:ANDROID_HOME
```

Absent commands/errors should be recorded, not silently fixed with a large tooling installation. If Git/Node/pnpm work, checkout only the vvp repository:

```powershell
git clone --branch prerelease --single-branch https://github.com/Volksverpetzer/vvp_app.git
cd vvp_app
git rev-parse HEAD
git status --short
Get-ChildItem -Name .env*
```

Branch `prerelease` is displayed publicly; if not present or inaccessible, record the failure and use the default branch rather than force-changing source. Do not expose `.env` contents, tokens or credentials.

**15–45 min — source seam trace.** Run fast read-only searches:

```powershell
git grep -n -E 'fetch\(|axios|useQuery|useInfiniteQuery|createApi|BASE_URL|API_URL|https?://' -- src | Select-Object -First 120
git grep -n -E 'testID|accessibilityLabel|FlatList|FlashList|Article|PostCard|Feed' -- src | Select-Object -First 120
Get-ChildItem src -Directory | Select-Object Name
```

Then identify exact call chain **feed route/component → query/hook/store/service → remote response/cache → rendered card** and a viable test-mode replacement point. Confirm that required images can be replaced with bundled synthetic assets. Record the actual file paths and snippets, not assumptions.

**45–75 min — local build feasibility, only if prerequisites are already ready.** Read root `package.json` scripts and tracked env sample, then try `pnpm install --frozen-lockfile` and `pnpm android` using an already available Android device/emulator. These are source-independent build checks, **not implementation**. Stop if native dependencies, login, SDK, auth or network are a major time sink. Record exit codes, first visible app screen or blocker; do not publish test packages, use EAS/cloud builds or commit generated files without consent.

**75–90 min — gate decision.** Is there (1) a runnable Android app, (2) a concrete, low-change scenario fixture path to real UI without live backend, (3) stable target selectors/ready state, (4) rights-safe synthetic assets? If yes, present paired `vvp_app + fixture provider` or `vvp_app + mock HTTP` alternatives. If not, switch the proposal to JetNews with its known `PostsRepository` seam, then the small owned news app if necessary. No Appium/Maestro approval is inferred.

**Source links:** https://github.com/Volksverpetzer/vvp_app ; https://f-droid.org/de/packages/de.volksverpetzer.app/ ; https://docs.maestro.dev/get-started/supported-platform/react-native .


---

## Active Windows feasibility checkpoint #1 (2026-11-01; user-supplied console evidence)

The `prerelease` repository cloned successfully; HEAD is **`8b421753a17a18cd648447319adcca61a288f97f`**. Installed Node is **22.12.0** (below documented `24.x+`); global pnpm became available at **12.11.2** (not checked against the repository's `packageManager` and lockfile). `adb devices -l` returned no devices, while the Android emulator enumerated **`Pixel_10`**. No Java/SDK readiness, emulator boot, Android build or running real UI has yet been demonstrated.

**Next read-only PowerShell probes** (run inside checked-out `vvp_app`; share output but never `.env` secrets):

```powershell
git status --short
Get-Content .nvmrc
$pkg = Get-Content package.json -Raw | ConvertFrom-Json
$pkg | Select-Object packageManager,engines
$pkg.scripts | Format-List
Get-Content pnpm-lock.yaml -TotalCount 12
Get-ChildItem -Name .env*
java -version
adb version
$env:ANDROID_HOME
$env:JAVA_HOME

git grep -n -E 'fetch\(|axios|useQuery|useInfiniteQuery|createApi|BASE_URL|API_URL|graphql|https?://' -- src | Select-Object -First 100
git grep -n -E 'testID|accessibilityLabel|FlatList|FlashList|Article|PostCard|Feed|Teaser' -- src | Select-Object -First 100
```

To let another agent inspect the exact **public tracked code** without lengthy console logs, run this optional *read-only* Git archive command in `vvp_app` and upload the resulting ZIP:

```powershell
git archive --format=zip --output ..\vvp_app_prerelease_8b42175_source.zip HEAD
```

`git archive` includes tracked files at HEAD, not the local `.git` directory, `node_modules` or ordinarily untracked `.env`; verify `.env` is not tracked before sharing if it contains anything sensitive. The archive may include third-party editorial/branding assets; use it only privately for the feasibility review.

**Gate still open:** identify exact real feed/article UI → hook/query/service → response; decide whether a low-change test-only fixture provider or test-only mock endpoint is appropriate. `pnpm install`/`pnpm android` and any implementation are not reported executed. Choosing Appium/Maestro is deferred.


---

## Latest SUT feasibility result — pinned `vvp_app` source archive (2026-11-01)

**Target:** `Volksverpetzer/vvp_app`, `prerelease`, HEAD `8b421753a17a18cd648447319adcca61a288f97f`; archive `vvp_app_prerelease_8b42175_source.zip` supplied and inspected. **Source-only PASS for identifiable UI and seam; native build/render NOT YET VERIFIED.** User's `git status --short` clean.

| Gate | Exact file/evidence | Result |
|---|---|---|
| Source/tool versions | `.nvmrc=24`, `package.json` Node `24.x` / pnpm `12.11.2`, RN `0.86.3`, Expo `57.0.30` | Confirmed source; host Node 22 mismatch; JDK 11 mismatch versus RN JDK17 guidance |
| App entry | `src/app/(tabs)/home.tsx:35-60,96-108` | Enabled-feed functions passed to actual `Feed`; onboarding/theme/permissions require control |
| WordPress feed binding | `src/screens/Home/fetchers/FeedFetcher.ts:20-28` → `WordPressFetcher.createFetchers(WordPressAPI.create(entry.handle))` | Confirmed central, replaceable **fetcher interface** in source |
| Article mapping | `src/screens/Home/fetchers/WordPressFetcher.ts:18-49,61-94` | `mapArticleToPost` produces `Post` with real `ArticlePost` |
| Network source | `src/helpers/network/WordPressAPI.ts:59-82,273-324`; config `config/volksverpetzer.config.ts:72-103` | WordPress `/wp-json/wp/v2/posts`, site-specific `entry.handle` URLs; multi-source + dynamic timestamp |
| Real UI rendering | `src/screens/Home/components/Feed.tsx:110-129,203-215,259-321`; `src/components/posts/GenericPost.tsx:42-80`; `src/components/posts/ArticlePost.tsx:220-309` | Source-confirmed native RN component tree; not yet seen on emulator |
| Additional nondeterminism | `ArticlePost.tsx:103-135,220-253,278-286` | Separate featured-media HTTP, animated GIF placeholder, saved scroll state/view counter; need deterministic media and suppression |
| Selectors | `ArticlePost.tsx:250` | `article-progress-bar` testID exists; no unique card-ready signal located in examined home/card source |
| Existing tests | `__tests__/helpers/fetchers/WordPressFetcher.test.tsx` and `__tests__/components/posts/ArticlePost.test.tsx` | Helpful patterns and sample article schema; Jest stubs expo-image, **not native PNG screenshots** |
| Server override caveat | `src/helpers/apiUrl.ts`, `src/helpers/network/ServerAPI.ts` | FOSS-only HTTPS app-server override does **not** automatically redirect WordPress article clients |
| Rights | `LICENSE.md` MIT | Code reuse with notice, asset/branding rights require audit; use synthetic text/static owned assets |
| Host Android | `ANDROID_HOME` present, `Pixel_10` AVD configured; `adb` no device; Java11 | Native build/emulator screenshot NOT VERIFIED |

### Time-boxed next activity

Bring Node to 24.x, `JAVA_HOME` to JDK 17, start existing AVD and verify `adb`; create local `.env` from tracked `.env.sample` if needed (README incorrectly names `.env.example`). Attempt `pnpm install --frozen-lockfile`, `pnpm android` under actual Windows prerequisites; capture error/first on-screen screenshot evidence only as a build check, **not a golden regression test**. Switch recommendation to JetNews or owned app if native build is a material deadline blocker. Do not implement fixture injection or runner before coupled human approval.

**Revised provisional SUT conclusion:** prioritize `vvp_app` (real existing shared RN UI plus now-confirmed fetcher injection boundary), conditional on build; JetNews remains lower-risk alternative if Expo setup blocks. Runner undecided.

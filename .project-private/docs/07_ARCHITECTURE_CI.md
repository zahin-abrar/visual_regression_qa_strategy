# Planning task 3 — Shared-core visual testing and scalable CI

> **Active SUT inspection priority: `vvp_app`.** Runner remains OPEN (Appium + Python/pytest **or** Maestro + screenshot assertion after fixture proof). JetNews-specific native Compose approaches below are historical contingent options, not a direct solution for React Native.

**Status:** Design preference / evaluation guide, not built. **Source distinction:** the AI-assisted build-frequency/QA-capacity problem was **reported by the candidate from the first interview**. The employer PDF independently asks for deterministic PR tests, Android/iOS, stability, and team-scale rollout.

## North-star objective

**Reduce repeated manual visual checks per fast-moving build while keeping visual-regression feedback trusted and economical.** Maximize **practical** sharing, not 100% code identity. A few small platform adapters are preferable to a brittle universal abstraction.

## Proposed logical layers

```text
Shared test repository (proposed Appium + Python/pytest)
  scenarios / fixtures / business-level actions / visual assertions
  baseline handling / reporting / CI orchestration
                   |
        platform driver adapters
        /                     \
  Android UiAutomator2       iOS XCUITest
        |                     |
     Android app              iOS app
        \                     /
       test-only fixture provider or common mock API
                   |
           real UI rendering
                   |
        screenshots and comparisons
          Android/iOS-specific goldens
```

**Share:** scenario names, fixture schema/data, test intent, comparison logic, report generation, CI configuration templates. **Allow differences:** driver/capabilities, locators/accessibility IDs, app reset/launch mechanism, fixture adapter, device configuration, and golden PNGs. For independent native app codebases, the same schema does not mean the same injection code. Avoid assuming the employer uses any particular UI framework.

## Candidate paths and trade-offs

| Path | Benefit | Weakness | Placement |
|---|---|---|---|
| **Appium + pytest + image diff** | Shared high-level Android/iOS suite, real rendering/navigation, fits candidate skills | Emulator/simulator cost, slower/flakier than isolated unit snapshots | Leading **demo candidate**; approve only after SUT/mock spike |
| **Paparazzi/Roborazzi + swift-snapshot-testing** | Fast isolated component images and easy fixture passing | Two platform test implementations, may miss integrated navigation | Scalable **production layer** / alternative demo |
| **Hybrid** | Fast broad component suite + smaller Appium end-to-end visual suite | Multiple tools to own, must govern overlaps and test selection | **Production strategy proposal**, not a promised full demo |

No paid visual diff or device cloud required by PDF. Use local emulator first for working proof where environment permits; document how macOS runner/device cloud extends iOS.

## CI/CD design (proposed, not implemented)

**PR path:** build test variant → start deterministic fixtures/mock service → boot pinned Android emulator (or iOS simulator on macOS) → run focused visual smoke suite → compare to approved platform-specific goldens → fail on unexpected diff → publish expected/actual/diff artifacts + report → reviewer decides fix vs intentional baseline update.

**Nightly/release path:** more variants (premium, dark, long text, dynamic type, offline/error), device sizes and OS versions, using parallel jobs and pinned baseline partitions. Keep broader matrix off the critical path for most PRs. If a native component snapshot layer exists, run it on every PR and reserve Appium for highest-value screens.

**Baseline location example:** `baselines/android/<device-os-theme>/<scenario>.png` and `baselines/ios/<device-os-theme>/<scenario>.png`. Golden changes go through human approval; automated tests must not silently overwrite them.

**Flakiness controls:** fixture isolation, fixed image assets/fonts/date/locale/timezone/font scale/theme, suppress animation, explicit UI-ready event, stable rendering environment, per-device baselines, controlled app reset, tight retry policy (diagnosis not masking), crash/log capture.

**Scale and maintenance controls:** reusable domain actions, thin platform adapters, ownership for visual baselines, deduplicated scenarios, change-impact/risk-based selection based initially on mapped component paths (not unvalidated AI-only test selection), CI artifacts and failure classification, track run duration/false-positive rate/device cost and manual verification effort. Include developer/PO/design review in Scrum and a staged opt-in/mentoring rollout.

## Feasible minimum for this take-home

- **Must demonstrate if Appium route approved:** native Android app + mock scenario + screenshot + committed golden + comparison; runnable locally.
- **High-value proof:** intentional visual change → failing assertion + diff and baseline review.
- **CI proof if feasible:** real successful GitHub Actions or equivalent job; otherwise supply a clearly labeled workflow proposal and avoid claiming CI runs.
- **iOS:** coherent XCUITest driver/runner/mock-contract adaptation and platform baseline plan **without falsely claiming execution**.

### Proposed measurements (no invented results)

PR feedback latency, test execution time/cost, screenshot false-positive rate, manual verification effort per build, cross-platform maintenance overhead, and escaped visual defects. Record baselines and measure improvements after rollout.

## Interview-level rationale

Appium is an execution tool, **not a mocking solution**. Shared tests reduce duplicated test maintenance but cannot erase native UI differences. Fast native snapshot checks may outperform device-based automation for many UI-state permutations. The design choice must be justified by evidence of reliability/throughput, not by shared-code percentage alone.


---

## 2026-11-01 SUT-conditioned path (PROPOSAL ONLY)

### Route 1 — JetNews + test repository + Appium/pytest (conditional preferred shared-suite demo)

Preconditions: `JetNews` actually builds; Android device/emulator and `adb` usable; debug-only scenario selection works; semantic/test tags are exposed to UiAutomator2; Python/Appium dependencies can be installed promptly. Share `scenario_id`/fixture semantics, pytest assertions, report and diff code. Keep Android driver/capabilities/locators/injection and Android baselines separate from future iOS XCUITest adapter/Swift or app-specific provider. Use pixel match or defined small tolerance only after two same-environment captures establish stability. Save actual/reference/diff plus logs as CI failure artifacts. **Nothing has been executed**.

### Route 2 — JetNews + direct Compose snapshots (time-saving demo fallback)

If Android SDK emulator, Appium setup or stable UI-ready selectors become blocking, feed fixed `Post` models directly into existing Compose UI in **Roborazzi** (natural candidate given documented JetNews Robolectric tests) or Paparazzi, subject to matching plugin/Gradle versions. This still tests real rendered UI and can be a fast PR screenshot gate; it does **not** deliver one shared Android/iOS driver, so share scenario contract/review/report practices and use swift-snapshot-testing on iOS. Do not integrate both Roborazzi and Paparazzi for this demo.

### Production rollout recommendation distinct from demo

Many fast native component snapshots for permutations (long headlines, font sizes, light/dark, premium flags, offline/error), plus a deliberately **small** cross-platform Appium smoke suite for genuine app-level rendering/navigation/launch integration. Use a pinned Android job and macOS-hosted iOS simulator job; nightly/release matrix for more OS/device/theme combinations. Explicit reviewer sign-off for golden updates; missing fixtures, wrong version/size, transient animation and network content should block baseline approval. Measure feedback latency, false-positive rate, flaky reruns, manual recheck effort and CI machine cost before expanding.

**Source-based caution:** JetNews `HomeScreens.kt` did not reveal `testTag`; Android's documented `testTagsAsResourceId` (or Appium UiAutomator2 `mapTestTagToResourceId`) is a *proposed* way to expose new stable IDs, not proof they work already. Source: https://developer.android.com/develop/ui/compose/testing/interoperability and https://appium.github.io/appium-uiautomator2-driver/latest/troubleshooting/.

**Build/CI state: NONE verified.** No local Android test, iOS native test, baseline PNG, diff, or green CI job exists from this session. GitHub Actions YAML is only configuration until a job passes.

---

## `vvp_app`-conditioned runner/CI evaluation (2026-11-01, all OPEN)

User authorized only a `vvp_app`-first **SUT/mock feasibility spike**. Do not silently carry forward the earlier JetNews + Appium recommendation as the new implementation decision. For React Native/Expo, native Compose tools such as Roborazzi/Paparazzi **are not drop-in screenshot engines for RN JS views**. Jest/React Test Renderer snapshots are structural/JSON tests, not the required screenshot PNGs of real native UI.

After proving deterministic fixtures within the real app, compare **two** realistic runners:

| Runner | Benefit | Risk/CI implication |
|---|---|---|
| **Appium + Python/pytest + platform baselines** | User's leading shared-test-code approach, Python comparison/reporting, UiAutomator2 Android and XCUITest iOS adapters; tests running real RN-native screen | Need working standalone/development build, stable RN `testID`/accessibility IDs, emulator/session startup and explicit ready state; network and animations must be controlled |
| **Maestro + built-in `assertScreenshot` (or controlled PNG diff)** | Single readable YAML flows on Android/iOS, React Native `testID` support and documented `takeScreenshot`/`assertScreenshot`; potentially less custom driver plumbing | Visual thresholds/baseline behavior must be validated, host Java/CLI/Android readiness still required, Python shared-core ambition is different; capture artifacts, explicit review and platform baseline governance still needed |

No automated baseline regeneration. Store separate Android/iOS approved reference images even when app JS is shared; pin device OS/size/density/theme/locale/font/animation. Use PR smoke only after reproducibility is verified; publishing actual/reference/diff and logs is expected, but a workflow configuration is not evidence of a passing CI job. Use a macOS runner/simulator for iOS written strategy. Wider device/OS/theme matrix belongs in nightly/release runs, not every PR. Production hybrid discussion remains useful but depends on actual app and should not be built for the demo unless justified.

**External official references:** https://docs.maestro.dev/get-started/supported-platform/react-native ; https://docs.maestro.dev/reference/commands-available/takescreenshot ; https://docs.maestro.dev/reference/commands-available/assertscreenshot .

**Exit evidence before runner approval:** source-pinned native Android build and real visual card, named fixed fixture rendered without live dependency, accessible stable UI target, actual screenshot capture path and candidate PR job cost. No result exists yet; environment is the candidate's Windows machine, not this assistant sandbox.


---

## `vvp_app` actual-source implications for runner/CI (2026-11-01)

**SUT not yet built.** React Native `0.86.3` / Expo `57.0.30` and the `WordPressFetcher` seam are source-confirmed. The app provides `testID="article-progress-bar"` but not a demonstrated unique card selector or content/asset-ready signal on its main article card; both must be implemented and validated if we choose device automation. Native Compose-only Paparazzi/Roborazzi is not a direct renderer for these RN cards. Jest component tests are useful but stub `expo-image` and cannot stand in for emulator screenshots.

**Appium + Python/pytest** remains the leading shared-code runner: shared fixture IDs/intent/reporting/diff and thin Android UiAutomator2/iOS XCUITest selector/launch adapters, separate Android/iOS baselines. **Maestro** remains the lightweight alternative for cross-platform flow and screenshot assertions, with its own threshold/diff behavior to confirm on first real snapshot. Neither is adopted yet. Mocking must be test-only feed injection independent of runner; Appium/Maestro do not mock source content by themselves.

**Feasible PR scope if build passes:** Android native debug/test build → deterministic scenario selection and ready state → pinned Pixel_10 emulator screenshot → compare approved Android golden → emit expected/actual/diff and test logs → fail PR for unexpected change, manual review for intentional baseline update. A bigger production solution can add macOS iOS runner/Simulator, shared RN data scenarios but distinct golden sets, and risk-selected broader nightly matrix. **No visual test, PNG, CI YAML or green CI has been created/executed yet.** JDK 17/Node 24, emulator boot and native install remain prerequisites. Keep performance and flakiness claims hypothetical until measured.

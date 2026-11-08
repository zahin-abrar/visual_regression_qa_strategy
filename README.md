# Mobile Visual Regression QA

A focused demonstration of mobile screenshot testing with a real React Native news application. It pairs one executed Android prototype with a proposed cross-platform strategy; the proposal is not presented as an implemented or tested iOS runner.

## Project overview

The repository contains the Volksverpetzer application with a development-only deterministic fixture, a Python/pytest/Appium visual runner, and supporting documentation. The executed Android scope on Pixel_10/API 37 includes five human-approved visual scenarios: `long_headline`, `breaking_news`, `dark_article`, `no_image` and `empty_feed`. Each is selected by an explicit runtime cold launch (`qa_scenario=<id>`) and has passed local native regression comparisons against its reviewed reference. iOS is proposed scope only; there is no iOS implementation or execution. See the [cross-platform strategy (PDF)](deliverables/strategy.pdf) and [editable Markdown source](deliverables/strategy.md).

## What has been demonstrated

- The real Volksverpetzer React Native app rendered the deterministic `long_headline` fixture.
- Appium with UiAutomator2 captured the native outer article-card element.
- A small Python/pytest POM separates screen-level access (`HomeScreen`) from component-level readiness and capture (`ArticleCard`, `BreakingBanner`, `EmptyFeedState`).
- Five runtime-selected Android scenarios are verified against human-approved references:
  - `long_headline`: outer article card, 1028 × 1237.
  - `breaking_news`: development-only banner, 1028 × 493.
  - `dark_article`: the same card in the real VVP dark palette, 1028 × 1237.
  - `no_image`: the card with genuinely absent featured media, 1028 × 711.
  - `empty_feed`: the real empty-state message region after a successful zero-item fetch, 1028 × 309.
- In EXEC-032, six separate cold launches through one Metro process covered all five scenarios, including two `empty_feed` runs. Every launch passed with zero changed pixels, and the two `empty_feed` captures were byte-identical. This was local sequential execution, not CI.
- A marker-controlled intentional failure demonstration (`-m intentional_failure`, excluded by default) captures the real `breaking_news` banner and compares it with a deliberately incorrect, channel-swapped reference. It genuinely fails at the comparison assertion (exit 1, 92.41% of pixels changed) and writes actual, diff and JSON artifacts, while the normal `breaking_news` test passes before and after. This is a reference-mismatch demonstration, not an application regression. See the [runner guide](qa_visual/README.md#intentional-visual-failure-demonstration).
- Two reviewed native captures were byte-identical at 1028 × 1237 pixels.
- After an explicit human-reviewed migration to the runtime-selected baseline, two independent cold-launch visual tests each reported **1 passed**, exit 0, and 0 of 1,271,636 changed pixels (0.0%).
- Each run writes a diff image and comparison-metrics JSON under `qa_visual/artifacts/android/pixel10-api37/`. This directory is Git-ignored, so a fresh clone has no artifacts until the tests are run locally.

The golden path `qa_visual/baselines/android/pixel10-api37/long_headline.png` is tracked. Its approved runtime-selected replacement was committed in local checkpoint `f0b38e9`, and the previous environment-fallback golden remains recoverable in Git history. This intentional migration preserves comparison thresholds; legacy fallback may no longer match, and the underlying native layout-rounding cause remains unresolved. No CI pipeline or native iOS execution has been demonstrated.

The breaking-news banner is a development-only sample-app extension for the challenge, not a verified upstream VVP production feature. After explicit human approval and byte-for-byte promotion, two independent banner regressions passed with zero changed pixels; their 1028 x 493 captures were byte-identical. The long-headline regression also passed against its unchanged reference. The breaking-news baseline was committed in local checkpoint `f0b38e9`. See the [runner guide](qa_visual/README.md#breaking-news-banner-approved-android-reference) for the exact breaking-news launch command and review policy.

## Architecture overview

- `app/` — Volksverpetzer React Native application and development-only fixture provider.
- `qa_visual/` — Android Appium visual tests in `tests/`, Python unit tests in `unit_tests/`, device-specific goldens and Pillow comparison. Root `pytest.ini` supports discovery from either working directory.
- The `HomeScreen` Screen Object and the `ArticleCard`, `BreakingBanner` and `EmptyFeedState` Component Objects own screen access, scenario-specific readiness, content lookup and native element capture.
- `visualqa/android.py` configures the Android Appium session; `visualqa/image_diff.py` compares PNGs and writes diff/metrics artifacts.
- Goldens are stored by platform and device profile. The current goldens belong to Android `pixel10-api37` and are not iOS references.

See [the runner README](qa_visual/README.md) for implementation details and setup.

## Setup from a fresh checkout

This project has been run only on one Windows 11 host with PowerShell. Nothing below has been re-executed from a clean clone; the table separates what was exercised on that host from what is only documented. Other operating systems are untested.

| Step | Status |
| --- | --- |
| Prerequisites: Git, Node 24.x (`app/.nvmrc`), pnpm 12.11.2 (`packageManager` in `app/package.json`), Java 17, Android SDK (platform-tools, emulator), Python 3.11-3.13 (3.13.1 used), Appium 3.3.0 with the `uiautomator2` driver 7.1.2 | Versions observed on the host; installation not repeated |
| 1. App dependencies: `cd app`, then `pnpm install` (optionally copy `.env.sample` to `.env`; `APP=volksverpetzer` is the variant tested) | Documented by the upstream app; not run from a clean clone |
| 2. Emulator: an AVD named `Pixel_10`, API 37, 1080 x 2424 at 420 dpi. Verified runs used `emulator -avd Pixel_10 -no-snapshot-load -gpu software` | Launch verified; AVD creation (Android Studio Device Manager) not documented or tested here |
| 3. Development build: with the emulator running, `cd app`, then `pnpm android` (`expo run:android`) installs the dev client `de.volksverpetzer.app` | Script exists in `app/package.json`; a clean build was not run. The host already had the app installed |
| 4. Metro: from `app/`, `pnpm.cmd exec expo start --dev-client --localhost --port 8081 --clear`, then `adb reverse tcp:8081 tcp:8081` | Verified (see Quick start) |
| 5. Appium: `appium --address 127.0.0.1 --port 4723` in its own terminal | Verified |
| 6. Python environment: `cd qa_visual`, `py -3.13 -m venv .venv`, then `.\.venv\Scripts\python.exe -m pip install -r requirements.txt` | Verified |
| 7. Tests (from `qa_visual/`): five normal visual tests, six-test run with the intentional failure, complete default suite, Allure and failure evidence | Verified; commands in the [pytest command matrix](qa_visual/README.md#verified-pytest-command-matrix-exec-040), [Allure reporting](qa_visual/README.md#allure-reporting-exec-038) and [retained failure evidence](qa_visual/README.md#retained-failure-evidence-exec-040b) |

The emulator, Metro and Appium are started by hand; the tests do not start them. Goldens are tied to the `pixel10-api37` profile above. Intermittent mismatches and Appium transport errors observed on the verified host are described in the runner README.

## Quick start

Once the Android emulator and installed development app are ready, start Metro with the fixture enabled in one PowerShell terminal:

```powershell
Set-Location .\app
$env:EXPO_PUBLIC_QA_SCENARIO = 'long_headline'
$env:NODE_OPTIONS = "--dns-result-order=ipv4first"
pnpm.cmd exec expo start --dev-client --localhost --port 8081 --clear
```

Preserve an existing healthy Metro process and its environment. With the Appium server ready and `adb reverse tcp:8081 tcp:8081` in place, run the visual tests from a second terminal. Each test declares its scenario (`@pytest.mark.qa_scenario(...)`) and cold-launches the app into it, so no launch URL needs to be set:

```powershell
Set-Location .\qa_visual # From the repository root.
.\.venv\Scripts\python.exe -m pytest .\tests\test_long_headline.py -v -s   # one scenario
.\.venv\Scripts\python.exe -m pytest .\tests -m visual -v                  # all five scenarios
.\.venv\Scripts\python.exe -m pytest .\unit_tests -q                       # unit tests; no Android required
.\.venv\Scripts\python.exe -m pytest -v                                    # all normal tests
```

In PyCharm, the normal Run action on a visual test file works with the `qa_visual/.venv` interpreter and no extra environment variables.

For emulator, app, Appium, Python environment, golden review and troubleshooting instructions, see [qa_visual/README.md](qa_visual/README.md).

To regenerate a candidate, run the corresponding `test_<scenario>.py` command above;
it saves a fresh native `artifacts/android/pixel10-api37/<scenario>.actual.png` and
context before comparison. Follow the [capture, human review and safe promotion steps](qa_visual/README.md#review-and-manually-promote-a-replacement)
to preserve evidence, approve its hash and back up an existing reference before replacement.
Tests never update goldens. Runner defaults require no `.env` file; see the
[configuration inventory](qa_visual/README.md#configuration-ownership-and-precedence)
for optional environment overrides and future CI usage.

## Optional Allure reports

Visual tests can emit an [Allure](https://allurereport.org/) report showing, per scenario, the approved golden, the actual native screenshot, the red diff, the comparison JSON and the pixel metrics; the intentional reference-mismatch demo is reported separately. It is optional: normal pytest and PyCharm runs need neither the Allure CLI nor any flag. Quick start (from `qa_visual/`; Allure Report 2 CLI 2.36.0 verified):

```powershell
.\.venv\Scripts\python.exe -m pytest -m visual --alluredir=artifacts/allure-results/visual --clean-alluredir --junitxml=artifacts/junit/visual.xml
allure generate artifacts/allure-results/visual -o artifacts/allure-report/visual --clean
allure open artifacts/allure-report/visual
```

Results and reports are written under the Git-ignored `qa_visual/artifacts/`. See [Allure reporting](qa_visual/README.md#allure-reporting-exec-038) for the intentional-failure report, attachments, CI notes and limitations. No CI job has run.

## GitHub Actions: Android build and advisory visual tests

Two independent, manually triggered workflows (`workflow_dispatch` only). Neither uses secrets, EAS or Expo/Play credentials; both use only the built-in `GITHUB_TOKEN`.

| Workflow | File | Purpose | Permissions |
| --- | --- | --- | --- |
| Android debug build | [`android-build.yml`](.github/workflows/android-build.yml) | Builds the debug APK on `ubuntu-24.04` (`pnpm install --frozen-lockfile`, Expo prebuild, Gradle `assembleDebug` x86_64) and uploads `android-debug-apk-x86_64` (kept 7 days). | `contents: read` |
| Android visual tests (advisory) | [`android-visual-tests.yml`](.github/workflows/android-visual-tests.yml) | Downloads an APK from an earlier build run, boots a headless emulator, starts Metro and Appium and runs only `python -m pytest -m visual -v` (five approved scenarios; no unit tests, no intentional-failure demo). **Never rebuilds the app.** | `contents: read`, `actions: read` |

Build and test are separate because the native compile takes about 34 minutes and one APK can be reused for many visual runs.

**1. Build an APK (when you need a new one):** GitHub > Actions > "Android debug build" > Run workflow on `main`.

**2. Find the run ID:** open the finished build run; the ID is the number in its URL (`.../actions/runs/<run id>`).

**3. Run the visual tests:** Actions > "Android visual tests (advisory)" > Run workflow, enter `source_run_id` (or `gh workflow run android-visual-tests.yml --ref main -f source_run_id=<run id>`).

**4. Re-run on the same APK:** start the visual workflow again with the same run ID while the artifact is still available. Artifacts expire after 7 days; then run the build again and use the new ID.

**Source checks (run first, fail clearly):** the ID must be numeric; the run must belong to this repository, be the Android build workflow and have completed successfully; the artifact must exist, be unexpired and non-empty. The source commit must be an ancestor of the commit under test, and none of these may have changed between them: `app/` (except Markdown), `qa_visual/baselines/`, `demo_assets/`, `visualqa/`, `tests/`, `conftest.py`, `requirements.txt` or `pytest.ini`. Workflow, script and documentation changes do not invalidate an APK. If the check fails, rebuild the APK from the current revision. The source run ID, source commit, visual workflow commit and APK SHA-256 are written to the job summary.

**5. Inspect results:** the visual job's Summary shows passed / comparison mismatch / other failure / error / not-executed counts with the provenance. Artifacts:

| Artifact | Contents | Retention |
| --- | --- | --- |
| `visual-evidence` | actual, reference, diff, comparison metadata and retained failure packages | 14 days |
| `visual-allure-report` | Allure HTML report (open `index.html` via a local server, for example `allure open <dir>`) | 14 days |
| `visual-allure-results` | raw Allure results and JUnit XML | 14 days |
| `visual-infra-logs` | emulator, Appium, Metro, pytest and logcat logs, environment metadata | 7 days |

**Why visual failures are advisory:** the pytest step has `continue-on-error`, so the job can be green while the step is red. The real exit code stays visible (failed step, warning annotation, summary banner); a green job does not mean five passing comparisons, so read the summary. Setup problems (source checks, artifact download, no KVM, emulator not booting, Appium or Metro not ready, app not starting) fail the job. There are no retries, and CI never changes goldens or thresholds.

**Cross-environment limitation:** the goldens were reviewed on a Windows-hosted Pixel_10 emulator. CI uses the same API 37 image, 1080x2424, 420 dpi and software rendering (`swiftshader_indirect`; local runs used `-gpu software`), but host OS, emulator build, image revision and GPU backend differ. A mismatch is **unresolved**: environment drift, the documented intermittent rendering instability, or a real regression. A CI-specific baseline strategy needs separate human review.

**Implemented versus GitHub-verified:** the build workflow passed on GitHub (run #2, 33m 38s). The visual workflow and its source checks are implemented and checked locally only (synthetic cases); they have not run on GitHub, so nothing here claims they work or that the goldens match on Linux. No iOS testing and no required PR check.

## Documentation

- [Android runner, setup and golden workflow](qa_visual/README.md)
- [Notice: provenance, licenses and brand-asset limitation](NOTICE.md)
- [Cross-platform Android/iOS screenshot-testing strategy (PDF)](deliverables/strategy.pdf) ([editable Markdown](deliverables/strategy.md))

## Results and limitations

The local Android visual test passed against the human-reviewed golden after repeat-capture verification. The current implementation covers five Android fixture scenarios (`long_headline`, `breaking_news`, `dark_article`, `no_image`, `empty_feed`) with human-approved references. They are captured as native element screenshots of the outer card, the banner or the empty-state message region; full-screen context images are diagnostic only. The capture targets depend on the current UiAutomator2 accessibility hierarchy. Comparison thresholds are unchanged: channel delta >12 and a maximum changed-pixel ratio of 0.002. The first three references were committed in local checkpoint `f0b38e9` and `no_image` in `8c54f0f`. The `empty_feed` reference and its implementation are also tracked in Git. Rendering consistency depends on using the matching app and emulator profile. There is no executed iOS test or verified CI job. A marker-controlled intentional failure demonstration (EXEC-033) fails against a deliberately incorrect reference; it shows the failure path and artifacts, not a detected application UI regression.

## Attribution and license

The application is adapted from [Volksverpetzer/vvp_app](https://github.com/Volksverpetzer/vvp_app), upstream `prerelease` commit `8b421753a17a18cd648447319adcca61a288f97f`. The app directory includes [its MIT license and notice](app/LICENSE.md); retain the upstream attribution and license terms. MIT covers the code, not logos, trademarks, mascot artwork or animations; see [NOTICE.md](NOTICE.md) for the unresolved brand-asset limitation. This does not establish redistribution clearance for every logo, image, or other third-party asset bundled with the app.


The additional `dark_article` implementation reuses the same article and real VVP
dark palette through a development-only, nonpersistent theme override. The exact reviewed native PNG was human-approved and promoted in EXEC-028;
independent cold-launch comparisons passed against its separate dark reference. See the [dark-article runner notes](qa_visual/README.md#dark-article-approved-android-reference).

The `no_image` scenario (EXEC-029) renders the same synthetic article through the real
`ArticlePost` with genuinely absent featured media and no image panel. This is a
deliberate, challenge-scoped, development-only QA adaptation keyed to an explicit QA
media contract; it is not verified upstream VVP production support for image-less
cards, and normal production article rendering is unchanged. The exact reviewed native
PNG was human-approved and promoted in EXEC-030; two independent cold-launch comparisons
passed against it with zero changed pixels. See the
[no-image runner notes](qa_visual/README.md#no-image-approved-android-reference).

The `empty_feed` scenario (EXEC-031) is a challenge-specific, deterministic
**successful-empty** case: one configured synthetic feed source resolves successfully
with zero articles. The real feed then shows VVP's existing empty-state message. It is
not offline, error or loading coverage. A development-only outcome record separates a
successful empty response from a failed fetch, which the production utilities also turn
into an empty list. The reference captures only the empty-state message region (icon and
text) and excludes the donation card below it. The exact reviewed native PNG was
human-approved and promoted byte for byte in EXEC-032. Two independent cold-launch
comparisons then passed against it with zero changed pixels, as did the four other
scenarios. The reference is tracked in Git. See the
[empty-feed runner notes](qa_visual/README.md#empty-feed-approved-android-reference).

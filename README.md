# Mobile Visual Regression QA

## Overview

This project demonstrates automated screenshot testing on a real Android news application adapted from Volksverpetzer. Using Appium and pytest, each test loads a predictable, development-only news scenario, captures the rendered React Native UI and compares it with a human-approved reference image (a *golden*).

Five scenarios are implemented and have passed local Android comparisons. The demonstration has not been implemented or executed on iOS.

## Prerequisites

The documented local environment is Windows 11 with PowerShell 5.1 or later. Install Git, Node.js 24.x, pnpm 12.11.2 (the version in `app/package.json`), Java 17 and Python 3.13. Put Java and Android SDK tools on `PATH`, and set `JAVA_HOME` to the Java installation.

Use Android Studio Device Manager to configure an x86_64 AVD named `Pixel_10`: API 37, 1080 x 2424, 420 dpi, font scale 1.0. On the tested host, ADB assigned the serial `emulator-5554`; that serial can differ on another machine or when multiple emulators are running. Android SDK platform-tools (`adb`) and emulator tools must be available.

**One-time setup**, starting at the repository root:

```powershell
npm install -g appium@3.3.0
appium.cmd driver install uiautomator2@7.1.2
appium.cmd driver doctor uiautomator2

Set-Location .\app
pnpm.cmd install --frozen-lockfile
Set-Location ..\qa_visual
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
Set-Location ..
```

An Android **development build** of `de.volksverpetzer.app` must be installed. If absent, first start the emulator as below, then run this from the repository root:

```powershell
Set-Location .\app
pnpm.cmd android
Set-Location ..
```

The app script invokes `expo run:android` and may start Metro. If it does, reuse that server only when it has the settings shown under **Run the demo**; otherwise stop it before starting Terminal 2. Do not run two Metro servers on port 8081, or rebuild an already working development app just to run tests.

Dependency installation and Android compilation have been exercised separately, including a tracked-only checkout with warm caches. The complete clean-host installation and `pnpm android` build/install/start sequence have **not** been verified end to end. AVD provisioning and the installation commands above remain setup guidance.

No runner `.env` is required. The app defaults to the tested `volksverpetzer` variant. Do not put credentials in client-visible `EXPO_PUBLIC_*` variables.

## Run the demo

Open each terminal at the repository root. Keep healthy existing services running; tests do not start them. The commands below use the existing installed development app.

**Terminal 1 — Android emulator**

```powershell
emulator -avd Pixel_10 -no-snapshot-load -gpu software
```

**Terminal 2 — Metro development server**

```powershell
Set-Location .\app
$env:EXPO_PUBLIC_QA_SCENARIO = 'long_headline'
$env:NODE_OPTIONS = '--dns-result-order=ipv4first'
pnpm.cmd exec expo start --dev-client --localhost --port 8081 --clear
```

`EXPO_PUBLIC_QA_SCENARIO` provides a development fallback. Each pytest test selects its own scenario when launching the app, so you do not need to change this variable or restart Metro between tests.

**Terminal 3 — Appium**

```powershell
appium.cmd --address 127.0.0.1 --port 4723
```

**Terminal 4 — checks and test execution**

```powershell
adb devices -l
adb -s emulator-5554 shell getprop sys.boot_completed
adb -s emulator-5554 reverse tcp:8081 tcp:8081
```

Wait for `emulator-5554 device`, boot status `1`, Metro ready on port 8081 and Appium ready on port 4723. Leave runner overrides unset, especially `VVP_QA_LAUNCH_URL`, `VVP_GOLDEN_PROFILE`, `VVP_CHANNEL_TOLERANCE` and `VVP_MAX_CHANGED_RATIO`.

**Machine-specific values:** The commands use the tested AVD name `Pixel_10` and ADB serial `emulator-5554`. On another host, run `adb devices -l` to identify the actual serial and adjust the ADB commands; use the configured AVD name when launching the emulator. **The golden-capture helper currently requires both `Pixel_10` and `emulator-5554`**, so changing these command values alone does not make that helper compatible with a different device. The documented API level, resolution, density and font scale must also match the reference profile.

From this same terminal, still at the repository root:

```powershell
# All five normal visual scenarios
.\qa_visual\.venv\Scripts\python.exe -m pytest .\qa_visual\tests -m visual -v

# One scenario: substitute another name from the table below
.\qa_visual\.venv\Scripts\python.exe -m pytest .\qa_visual\tests\test_breaking_news.py -v -s

# Python unit tests only; emulator, Metro and Appium are not required
.\qa_visual\.venv\Scripts\python.exe -m pytest .\qa_visual\unit_tests -q
```

These test selections have been exercised locally. Each visual test cold-launches its own scenario and checks identity and readiness before capture. No manually assembled deep link or Metro restart between scenarios is needed.

## Test scenarios

| Scenario | Component captured |
| --- | --- |
| `long_headline` | Article teaser with a long German headline |
| `breaking_news` | Development-only breaking-news banner |
| `dark_article` | Dark-theme article teaser |
| `no_image` | Text-only article teaser with absent media |
| `empty_feed` | Message after a successful empty-feed response |

Goldens capture specific UI components, not the full phone screen. Full-screen context is diagnostic only. `empty_feed` excludes donation controls and does not cover offline/error behavior; `no_image` is a test-only adaptation, not general production optional-media support.

Optional intentional reference-mismatch demonstration, from the repository root:

```powershell
.\qa_visual\.venv\Scripts\python.exe -m pytest .\qa_visual\tests\test_intentional_visual_failure.py -m intentional_failure -v -s
```

This is **expected to fail with exit code 1** against a deliberately incorrect reference. It demonstrates comparison failure evidence, not an application defect, and is excluded from normal runs.

## Regenerate golden images

The two PowerShell helpers keep **candidate capture**, **human review** and **golden promotion** separate. Both support the five scenarios above and only the `pixel10-api37` profile. The profile name does not guarantee identical rendering; the helpers check observable device settings.

**Verification status:** 50 mocked safety checks passed, but the helpers have **not** been tested end to end with real ADB/native screenshot capture. Keep default runner settings; unset `PYTEST_ADDOPTS` and `PYTEST_PLUGINS` for capture, and do not run other pytest/device operations concurrently. The helper lock cannot control unrelated processes.

**1. Capture a candidate** — With the emulator, Metro and Appium running, execute from the repository root:

```powershell
.\scripts\goldens\capture-candidate.ps1 -Scenario breaking_news
```

The command preserves previous rolling artifacts and reports a unique review folder under `qa_visual/artifacts/review/` with the candidate, hashes, provenance, JUnit results and logs. It does **not** change approved goldens. It accepts a captured comparison mismatch or missing golden only with consistent evidence; startup, readiness, cleanup and ambiguous failures are rejected.

**2. Review the candidate** — Open the reported folder. Compare `candidate.png`, `context.png`, the existing `reference.png` (if present), and available `diff.png`/comparison metrics. Check content, capture boundaries, headline wrapping, theme and image rendering. Make a second independent capture to check stability before approving a visual change. Record the reason for the change and the **exact candidate SHA-256** printed by the helper. A passing comparison is not approval. Keep the reviewed packet unchanged.

**3. Promote only after approval** — Use the reviewed folder and exact approved hash:

```powershell
.\scripts\goldens\promote-golden.ps1 `
  -ReviewDir "<review-directory>" `
  -ApprovedHash "<approved-sha256>"
```

Review the displayed destination and hashes, then type `PROMOTE` only if you approve that specific candidate. The helper verifies the hash, rejects a changed original reference, backs up the existing golden, protects any prior backup and checks the copied bytes. It never stages, commits or pushes.

**4. Verify before committing** — Promotion reports `PROMOTED  NATIVE VERIFICATION PENDING`. Run the printed scenario-specific pytest command and destination hash check, require a passing native comparison, and review the Git diff before committing the image. If verification fails, preserve the candidate, promoted reference, backup and failure evidence; there is **no automatic retry, rollback or approval**. Any restoration requires a separate human decision.

If Windows blocks `.ps1` execution, consult the applicable PowerShell execution-policy guidance rather than changing a machine-wide policy solely for this demo.

## Review results

After a test, inspect its actual screenshot and visual difference. A passing comparison means the image matches the approved golden within the configured tolerance. If a comparison fails, review the images to decide whether the change is intentional; if the app fails before capture, investigate the startup diagnostics instead.

Normal test output is under the Git-ignored `qa_visual/artifacts/android/pixel10-api37/`:

- `<scenario>.actual.png`: native component screenshot.
- `<scenario>.diff.png` and `.comparison.json`: visual difference and metrics, written when comparison runs.
- `<scenario>.context.png`: uncompared full-screen diagnostic context.
- `failures/<unique-directory>/`: best-effort retained comparison/missing-golden evidence and manifest.
- `launch-diagnostics/<scenario>/` or `failure-*` files: available startup, hierarchy and driver diagnostics.

Approved goldens are in `qa_visual/baselines/android/pixel10-api37/`. Ordinary artifact filenames roll over on later runs; preserve evidence before rerunning. Helper review packets are isolated under `qa_visual/artifacts/review/`.

A visual mismatch means capture reached comparison. A missing golden means capture completed without an approved reference; no new diff is produced. Setup, identity, readiness, driver and application failures are separate failures and must not be accepted as golden candidates. Check current logs and timestamps rather than interpreting leftover images as a completed run.

The unchanged comparison policy counts a pixel when any RGB channel differs by more than 12, allows at most 0.2% changed pixels and fails different image dimensions. Do not adjust tolerances or accept a new golden to hide an unexplained mismatch.

### Allure reporting — inspect screenshots and comparisons

Allure provides a browsable view of the test run: **pass/fail status, scenario details and visual evidence** in one place. For completed visual captures, open a test to inspect the approved reference, actual native screenshot, highlighted diff, full-screen context and comparison metrics (where available). Evidence is attached before the visual assertion, so an intentional comparison failure retains its images. Allure shows captured evidence **after it is produced**, not a live video of the emulator.

**Run the complete demo suite**, including unit tests, all five normal visual scenarios and the intentionally failing comparison. With the emulator, Metro and Appium ready, run from the repository root:

```powershell
.\qa_visual\.venv\Scripts\python.exe -m pytest -m "unit or visual or intentional_failure" -v `
  --alluredir=qa_visual/artifacts/allure-results/full-demo `
  --clean-alluredir `
  --junitxml=qa_visual/artifacts/junit/full-demo.xml
```

**An exit code of 1 is expected for this demonstration** because the intentional test compares a real screenshot with a deliberately incorrect reference. In a previously verified local run, the selection produced 79 passes and one intentional failure; results can differ if a real test or infrastructure problem occurs. The normal passing suite remains the command under **Run the demo**.

**Start the Allure report server** to generate the report and open it in your browser:

```powershell
allure serve qa_visual/artifacts/allure-results/full-demo
```

For a persistent HTML report instead, use:

```powershell
allure generate qa_visual/artifacts/allure-results/full-demo -o qa_visual/artifacts/allure-report/full-demo --clean
allure open qa_visual/artifacts/allure-report/full-demo
```

Use the **Allure Report 2 CLI** (version 2.36.0 verified; Java required), distinct from the `allure-pytest` package installed with the Python requirements. `allure serve` uses a temporary report directory; `allure generate` saves a report under Git-ignored `qa_visual/artifacts/`. Stop the local server with `Ctrl+C`. Neither Allure nor the intentional failure changes goldens or comparison thresholds; regular pytest runs do not require the Allure CLI.

## GitHub Actions

Two independent workflows are manually triggered through **Actions → Run workflow**:

1. Run [Android debug build](.github/workflows/android-build.yml) when a new APK is needed. It builds and uploads `android-debug-apk-x86_64` for seven days.
2. Open the successful build run and copy the numeric run ID from its URL.
3. Run [Android visual tests (advisory)](.github/workflows/android-visual-tests.yml), supplying that ID as `source_run_id`.
4. Choose `visual_scope`: `all` (five normal scenarios), `breaking_news` or `no_image`.
5. Inspect the summary, actual pytest results and artifacts: `visual-evidence`, `visual-allure-results`, `visual-allure-report` and `visual-infra-logs`.

The visual workflow reuses the APK rather than rebuilding it. Source/run compatibility and artifact availability are checked first; rebuild if the source is incompatible or the artifact has expired. The summary records APK and source provenance.

**Workflow status is not pytest status.** Visual pytest failures are advisory (`continue-on-error`), so a green job can contain failing tests. Setup failures fail the job. Neither workflow changes goldens or thresholds.

Recorded hosted evidence: APK build `42616325655` succeeded; isolated `breaking_news` run `42620071563` passed with zero changed pixels. A full-suite execution passed comparisons for `breaking_news`, `dark_article`, `empty_feed` and `long_headline`; `no_image` crashed natively before comparison. **The hosted five-scenario suite has not passed.** No full-suite run ID is claimed here.

There is no pull-request-triggered blocking visual check or native iOS execution.

## Known limitations

- Reference images were reviewed on a Windows-hosted emulator. Differences in emulator images, host rendering, font settings or GPU behavior can affect comparisons even when the display profile appears to match.
- Intermittent local rendering mismatches and Appium transport errors remain unresolved. Repeating a test is not proof that the underlying issue has been fixed.
- The demo uses an Expo development client and Metro, not a verified standalone release build. It does not demonstrate app-wide network isolation or native iOS execution.

The outstanding hosted `no_image` crash, manual/advisory CI scope and unverified clean-host/helper onboarding are described where those workflows are introduced above.

## Attribution

Adapted from [Volksverpetzer/vvp_app](https://github.com/Volksverpetzer/vvp_app), pinned upstream revision `8b42175` on `prerelease`. Retain the application's [MIT code license and copyright notice](app/LICENSE.md).

MIT licensing of code does not establish rights to logos, trademarks, illustrations or animations. Brand-asset redistribution rights remain unresolved; see [NOTICE.md](NOTICE.md).

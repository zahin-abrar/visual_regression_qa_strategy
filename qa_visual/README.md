# Android visual regression demo

This runner checks one deterministic visual scenario in the real Volksverpetzer React Native application. The `long_headline` fixture feeds synthetic article data through the app's normal React Native components; Appium/UiAutomator2 captures the rendered outer article card from Android. Pillow compares that PNG with a reviewed golden.

The implemented demo is Android only. There is no executed iOS test or verified CI pipeline.

## Implemented structure

- `tests/test_long_headline.py` owns the scenario, fixture-title assertion, screenshot paths and visual assertion.
- `visualqa/screens/home_screen.py` exposes the `HomeScreen` Screen Object.
- `visualqa/components/article_card.py` locates the ready article, reads its title, waits for readiness and captures its containing card element. The capture checks the parent and ready-element rectangles before taking the native element screenshot.
- `visualqa/android.py` configures the Android UiAutomator2 session and writes diagnostic screen/hierarchy files after a failure.
- `visualqa/image_diff.py` is the Pillow comparison utility. It compares RGB pixels, writes a diff overlay and can write JSON metrics; it never creates or updates a golden.

The component uses the app accessibility identifiers `qa-article-card-ready` and `qa-article-title`. The ready identifier is on an inner pressable; on the verified Pixel_10 hierarchy, the direct parent contains the complete visible card. That parent relationship depends on the current Android accessibility hierarchy and is checked at runtime.

## Verified host and emulator profile

The following versions and settings were observed on the execution host. They describe the verified profile, not minimum or exclusive compatible versions:

| Component | Verified value |
| --- | --- |
| Python | 3.13.1 |
| Appium server | 3.3.0 |
| UiAutomator2 driver | 7.1.2 |
| Appium-Python-Client | 5.2.4 |
| pytest | 8.4.2 |
| Pillow | 11.3.0 |
| Node.js / pnpm | 24.22.2 / 12.16.1 observed; app manifest specifies Node 24.x and pnpm 12.11.2 |
| Java | 17.0.21 observed; Appium doctor found Java/JAVA_HOME available |
| Android target | Pixel_10 AVD, API 37, `emulator-5554` |
| Emulator display | 1080 × 2424 at 420 dpi |
| Emulator memory | 4,008,492 kB `MemTotal` (approximately 4 GB) |

Python packages are pinned in `requirements.txt`. Android automation also requires Android SDK platform tools (`adb`), an Android emulator, Java, an installed development build of the app, Metro, Appium and the UiAutomator2 driver. The installed app package and runner defaults are `de.volksverpetzer.app`, device name `Pixel_10`, UDID `emulator-5554`, activity `.MainActivity`, and Appium URL `http://127.0.0.1:4723`.

## Windows setup and startup

These instructions describe the local setup. Python environment creation and dependency installation were exercised on this host; the full clean-machine Android build/startup sequence below was not rerun end-to-end for this README update.

### 1. Android tooling and emulator

Install/configure Android SDK platform tools, an Android emulator and a Java 17 toolchain. `JAVA_HOME` must point to the Java installation. The UiAutomator2 doctor passed required checks for `adb`, `emulator`, Java and `JAVA_HOME`; optional warnings were reported for `bundletool.jar` and GStreamer screen-streaming tools.

Start the existing AVD and check it is available and booted:

```powershell
emulator -avd Pixel_10
adb devices -l
adb shell getprop sys.boot_completed
adb shell wm size
adb shell wm density
```

The expected device is listed as `emulator-5554 device`, boot status is `1`, display is 1080×2424 and density is 420 dpi. Configure an equivalent profile before using this profile's golden; changed resolution, density, font scale, theme or app layout can invalidate comparisons.

### 2. Start the fixture-enabled development app

The fixture is enabled only when the app is a development build (`__DEV__`) and `EXPO_PUBLIC_QA_SCENARIO` equals `long_headline`. Start Metro from `app/` with the variable set in that PowerShell process:

```powershell
$repo = 'D:\Projects\visual_regression_qa_strategy' # Set this to your checkout root.
Set-Location (Join-Path $repo 'app')
$env:EXPO_PUBLIC_QA_SCENARIO = 'long_headline'
pnpm.cmd start --clear
```

Leave Metro running. The test activates the already-installed app through Appium; Metro alone does not install/build the native application. If no development build is installed, the app manifest provides `pnpm.cmd android` to build/install it, but that clean setup/build sequence is documented and was not re-executed for this task. Do not rebuild an existing working app just to run the visual test.

### 3. Start Appium

Install Appium and the driver only on a new host that does not already have them. These installation commands are documented setup steps, not part of the verified test run:

```powershell
npm install -g appium
appium.cmd driver install uiautomator2
appium.cmd driver doctor uiautomator2
```

Start the server in a separate terminal and leave it running:

```powershell
appium.cmd --address 127.0.0.1 --port 4723
```

The server startup, driver load and `/status` readiness were verified on this host. Do not start a duplicate server if port 4723 is already serving Appium.

### 4. Create the Python environment

From `qa_visual/`, create the environment and install the exact pins from `requirements.txt`:

```powershell
$repo = 'D:\Projects\visual_regression_qa_strategy' # Set this to your checkout root.
Set-Location (Join-Path $repo 'qa_visual')
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

This was exercised with Python 3.13.1: the pinned packages installed, `pip check` found no broken requirements, and pytest/unit verification succeeded. No global Python packages are required by this runner.

## Run the checks

Run these commands from `qa_visual/`:

```powershell
# Unit tests do not start an Appium session.
.\.venv\Scripts\python.exe -m pytest -m unit -q

# Show which tests pytest discovers; collection does not run the visual scenario.
.\.venv\Scripts\python.exe -m pytest --collect-only -q

# Run the single native Android scenario; requires the running emulator, app,
# fixture-enabled Metro and Appium server described above.
.\.venv\Scripts\python.exe -m pytest .\tests\test_long_headline.py -m visual -v -s
```

The unit suite and collection command passed during prior execution. The visual command also passed after promotion of the reviewed baseline. A run with no baseline deliberately fails after capturing the actual and context screenshots, with a `Golden missing` message; this is not a successful comparison.

## Golden images and comparison

The test's default Android golden is:

```text
baselines/android/pixel10-api37/long_headline.png
```

This reviewed golden is committed in the repository. Its source was Capture A, a native Appium outer-card screenshot reviewed for its complete boundary and repeatability, then explicitly approved for promotion. Android/device profiles use separate directories; do not reuse this image for iOS or a different device/rendering profile.

The test captures the Appium element screenshot to `artifacts/android/<profile>/long_headline.actual.png`, then compares it to the golden. The full-screen context PNG is diagnostic only and is not compared because items such as the status-bar clock can change. The default policy counts a pixel as changed when any RGB channel differs by **more than 12**, and passes only if no more than **0.2%** of pixels are changed. Different dimensions always fail. The test writes a red-overlay diff and comparison JSON when it reaches comparison; thresholds can be overridden with environment variables, but changing them is not a substitute for investigating a mismatch.

### Review and manually promote a replacement

Golden updates are explicit human decisions. The following is a documented procedure; the complete replacement/regeneration sequence has not been run end-to-end. It does not make the test update a golden automatically.

1. Confirm the app/fixture and emulator profile are correct. From `qa_visual/`, run the single visual test command above. It captures `actual.png` and `context.png` before comparison. If the current golden differs, pytest may fail; retain that failure and its diff/JSON as review evidence.
2. Inspect the new `actual.png` against the full-screen `context.png`, checking fixture content, headline wrapping, image load, metadata, summary and the complete card boundary. Review the generated `diff.png` and `comparison.json` against the current golden. Do not promote a screenshot with unexplained rendering changes.
3. Only after an authorized reviewer approves the exact `actual.png`, preserve the existing golden and interactively confirm the replacement. Example for the default profile:

   ```powershell
   $baseline = '.\baselines\android\pixel10-api37\long_headline.png'
   $candidate = '.\artifacts\android\pixel10-api37\long_headline.actual.png'
   $backup = '.\artifacts\android\pixel10-api37\long_headline.previous-approved.png'

   if (Test-Path $backup) { throw "Backup already exists: $backup" }
   Copy-Item -LiteralPath $baseline -Destination $backup
   Get-FileHash $candidate -Algorithm SHA256
   Copy-Item -LiteralPath $candidate -Destination $baseline -Confirm
   Get-FileHash $baseline -Algorithm SHA256
   ```

   Check candidate dimensions/readability with Pillow and compare the copied hash with the candidate hash. The `-Confirm` prompt is deliberate. If there is no existing baseline, create the parent directory and copy the reviewed candidate only after approval; still verify its hash and image dimensions.
4. Run the same visual test once more. A passing comparison must be observed; then verify the golden hash remains unchanged. Keep the previous approved image and review artifacts according to project retention needs. Never use an automatic “update golden” mode or replace a baseline merely to make a test pass.

## Artifacts and failure diagnosis

For the default profile, runner output is under `artifacts/android/pixel10-api37/`:

- `long_headline.actual.png` — native screenshot of the outer article-card element.
- `long_headline.context.png` — full-screen context; not used for comparison.
- `long_headline.diff.png` — red-overlay difference image generated by the comparator.
- `long_headline.comparison.json` — dimensions, changed-pixel count/ratio, configured tolerances and pass result.
- `failure-full-screen.png` and `failure-page-source.xml` — diagnostics written when capture/setup inside the Appium test fails.

A **missing/unapproved baseline** means the native capture completed, but there is no approved reference to compare; pytest reports `Golden missing`. A **visual regression** means the test captured the fixture and compared it with an existing baseline, but the size/pixel policy failed. Appium connection, locator, readiness or fixture-title errors are earlier failures; inspect the failure screenshot and XML rather than treating them as visual comparison results.

Useful read-only checks include `adb devices -l`, `adb shell getprop sys.boot_completed`, `appium.cmd driver list --installed`, and `http://127.0.0.1:4723/status`. For selector/readiness failures, check that the app is a development build, Metro was started with the correct environment variable, and the fixture's local image has loaded. Do not add sleeps or fall back to a full-screen crop as a golden.

## Scope and limitations

- One Android `long_headline` fixture and one Pixel_10/API 37 profile are implemented and verified.
- There is no native iOS execution, iOS baseline, or verified CI pipeline.
- The card screenshot target resolves the ready element's direct parent based on the current UiAutomator2 hierarchy. Bounds checks guard the captured relationship, but a future app/accessibility-tree change may require inspection and a new reviewed golden.
- Snapshot consistency depends on matching app build, emulator resolution/density, font scale, theme, assets and rendering environment.
- The approved Android golden is committed at `baselines/android/pixel10-api37/long_headline.png`.
- Installation/build instructions marked above as documented setup steps were not all re-run end-to-end during this documentation task. Refer to the task history for exact verified command outcomes.

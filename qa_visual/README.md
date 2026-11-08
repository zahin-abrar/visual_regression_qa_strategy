# Android visual regression demo

This runner captures five deterministic visual scenarios in the real Volksverpetzer React Native application. The `long_headline` fixture feeds synthetic article data through the app's normal React Native components; Appium/UiAutomator2 captures the rendered outer article card from Android. Pillow compares that PNG with a reviewed golden.

`long_headline`, `breaking_news`, `dark_article`, `no_image` and `empty_feed` each have an explicitly human-approved Android reference and passing local native comparisons. The implemented demo is Android only. There is no executed iOS test or verified CI pipeline.

## Implemented structure

- `tests/` contains five normal Appium visual tests and the explicitly selected intentional-failure demo. Each test owns its scenario, UI assertions and native component capture.
- `unit_tests/` contains Python tests that require no Android services. The five original unit files retain their assertions; focused artifact/lifecycle tests cover the shared helpers.
- Repository-root `pytest.ini` defines both test directories, markers and `pythonpath = qa_visual`, so discovery/imports work from either the repository root or `qa_visual/`.
- `conftest.py` reads the scenario marker; `visualqa/visual_check.py` owns `VisualArtifacts` (profile paths, context/hierarchy/metadata writing, comparison and failure messages). It never writes a reference.
- `android_session()` in `visualqa/android.py` wraps driver creation, failure diagnostics, termination and quit. Comparison runs after the session closes.
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

The compatibility fallback enables the fixture when the app is a development build
(`__DEV__`) and `EXPO_PUBLIC_QA_SCENARIO` equals `long_headline`. The runtime-selection
path below is now the verified launch contract for the approved reference.
For the compatibility procedure, start Metro from `app/` with the variable set in
that PowerShell process:

```powershell
$RepoRoot = (git rev-parse --show-toplevel) # Run from anywhere inside your checkout.
Set-Location (Join-Path $RepoRoot 'app')
$env:EXPO_PUBLIC_QA_SCENARIO = 'long_headline'
$env:NODE_OPTIONS = "--dns-result-order=ipv4first"
pnpm.cmd exec expo start --dev-client --localhost --port 8081 --clear
```

Leave an already healthy Metro process unchanged; do not start a duplicate. The explicit runtime launch below terminates and opens the already-installed app through Appium; Metro alone does not install/build the native application. If no development build is installed, the app manifest provides `pnpm.cmd android` to build/install it, but that clean setup/build sequence is documented and was not re-executed for this task. Do not rebuild an existing working app just to run the visual test.

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
$RepoRoot = (git rev-parse --show-toplevel) # Run from anywhere inside your checkout.
Set-Location (Join-Path $RepoRoot 'qa_visual')
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
```

This was exercised with Python 3.13.1: the pinned packages installed, `pip check` found no broken requirements, and pytest/unit verification succeeded. No global Python packages are required by this runner.

## Run the checks

### Self-launching visual tests (current workflow, EXEC-035)

Each visual test declares its own scenario, for example
`@pytest.mark.qa_scenario("breaking_news")`. The `qa_scenario` fixture in
`conftest.py` reads that marker. `make_driver(scenario)` builds the development-client
deep link (`build_launch_url` in `visualqa/scenario_launch.py`), terminates the app,
cold-launches it with that `qa_scenario` and waits for the exact `qa-scenario:<id>`
identity, all before the feed-specific readiness and capture. No per-scenario
`VVP_QA_LAUNCH_URL` is needed. Run from `qa_visual/`:

```powershell
.\.venv\Scripts\python.exe -m pytest .\tests\test_breaking_news.py -v -s   # one scenario
.\.venv\Scripts\python.exe -m pytest .\tests -m visual -v                  # all five scenarios
.\.venv\Scripts\python.exe -m pytest -v                                   # unit + visual; intentional demo deselected
```

**PyCharm:** use the normal green Run icon (or *Run 'pytest in test_…'*) on a visual test
file or function, with `qa_visual/.venv` as the interpreter. No environment variables or
extra arguments are needed. Repository-root `pytest.ini` is found from the test's path; its
`pythonpath = qa_visual` makes framework imports independent of the working directory. This also works when the working
directory is the repository root, which was checked from the command line. Only the
intentional-failure demo needs `-m intentional_failure` (see below).

External prerequisites remain: emulator `emulator-5554` booted with the development app
installed, Metro running (port 8081), the Appium server (port 4723) and
`adb reverse tcp:8081 tcp:8081`.

Optional overrides:

- `VVP_METRO_HOST` and `VVP_METRO_PORT` (defaults `127.0.0.1` and `8081`) change the Metro
  address placed in the launch link.
- `VVP_QA_LAUNCH_URL` is still accepted for compatibility, but only if its `qa_scenario`
  equals the scenario the test declares. A stale or conflicting value fails with a
  `ValueError` before any Appium session opens; it never silently selects another fixture.
- The existing `VVP_APPIUM_URL`, `VVP_ANDROID_*` and `VVP_GOLDEN_PROFILE` settings are
  unchanged.

The per-scenario examples further down that set `VVP_QA_LAUNCH_URL` record how earlier
evidence was produced. They still work, because a matching URL is accepted, but they are
no longer required.

Verified in EXEC-035 (local Pixel_10/API 37, not CI) with `VVP_QA_LAUNCH_URL` unset:

- Each of the five visual files, run alone, selected its own scenario and passed (exit 0)
  with 0 changed pixels; every actual was byte-identical to its golden.
- `pytest tests -m visual -v`: 5 passed (exit 0), as separate cold launches in the order
  breaking_news, dark_article, empty_feed, long_headline, no_image, with 0 changed pixels.
- Historical pre-separation `pytest tests -v`: 46 passed, 1 deselected, exit 0. Since EXEC-037, use `pytest -v` for unit + visual; `pytest tests/` runs visual tests only.
- `-m intentional_failure`: failed as intended (exit 1, 468,349 / 506,804 changed).
- A stale `VVP_QA_LAUNCH_URL` (`long_headline` for the `breaking_news` test) failed
  immediately with the conflict message. A matching URL passed.

### Test organization and coding conventions (EXEC-037)

From `qa_visual/`, using the existing interpreter:

```powershell
.\.venv\Scripts\python.exe -m pytest -v                 # all normal unit + visual tests
.\.venv\Scripts\python.exe -m pytest unit_tests/ -v     # no Android services needed
.\.venv\Scripts\python.exe -m pytest -m unit -q         # same unit suite by marker
.\.venv\Scripts\python.exe -m pytest tests/ -v          # five normal visual tests
.\.venv\Scripts\python.exe -m pytest -m visual -v       # same visual suite by marker
.\.venv\Scripts\python.exe -m pytest --collect-only -q
.\.venv\Scripts\python.exe -m pytest tests/test_dark_article.py::test_dark_article_android_card_matches_reviewed_golden -v
.\.venv\Scripts\python.exe -m pytest tests/test_intentional_visual_failure.py -m intentional_failure -v -s
```

The final command deliberately exits 1 at the comparison assertion. The demo remains
excluded by default, including when the `tests/` directory is selected. From the
repository root use `qa_visual\.venv\Scripts\python.exe -m pytest`; for explicit
paths prefix `qa_visual/` (for example `qa_visual/unit_tests/`). No custom runner is used.
PyCharm can select an individual file/function with this interpreter and either working
directory; GUI interaction itself has not been verified.

Conventions for Python contributions: standard-library, third-party, then local imports;
4-space indentation; snake_case functions/variables, PascalCase classes and uppercase
constants; annotate shared helper interfaces and test scenario parameters. Use `Path`,
UTF-8 text output and named metadata fields. Keep UI assertions in tests, locators and
native screenshot bounds in components, and pixel calculations in `image_diff.py`.
Preserve the original body/launch exception object and traceback. Diagnostic or cleanup
failures are attached as exception notes with their tracebacks; termination and `quit()`
are both attempted. If the body succeeds, the first cleanup failure propagates and any
later failure is attached as a note. Driver creation failure before a usable driver exists
propagates directly. Ordinary tests report through pytest assertions;
explicit console output remains only for the intentional demonstration and comparator CLI.
Long metadata expressions are split across lines. The original 41 unit-test assertions are preserved.

Ruff was evaluated but is not installed or required. This bounded refactor uses manual
style review and pytest, avoiding a formatting-only sweep of untouched components. A
future dedicated tooling change can pin one Ruff version and configuration; there is no
lint/format command claimed as verified here.

The duplicate-code warning in article tests corresponds to shared path setup, comparison,
artifact writes and cleanup, now extracted into small helpers. Readiness, title, theme,
missing-image and empty-feed assertions remain explicit. Capture operations stay in the
existing Component Objects; no generic scenario engine or inheritance was introduced.

Tolerance asymmetry is retained deliberately for compatibility: long/dark/no-image/empty
call `compare(use_environment_tolerances=True)`; breaking news and the intentional demo
call `compare()` with the unchanged comparator defaults (12 and 0.002). History shows the
banner tests were added using defaults; no separate product requirement for this difference
was found. Keep overrides unset for the approved suite. A future policy change could unify
this explicitly after review, but extracting helpers must not silently change behavior.

Initial EXEC-037 local verification: 50 unit tests passed (the original 41 plus nine helper
checks); both visual selection commands passed all five scenarios with zero changed
pixels; default execution passed 55 tests with the intentional demo deselected. An
individual dark-article test function passed. Explicit intentional-failure execution
returned exit 1 at the real comparator assertion (468,349/506,804 changed pixels,
92.4123%). Collection succeeded from both working directories. All six protected
reference hashes remained unchanged. PyCharm GUI itself was not exercised.

The subsequent EXEC-037 exception-preservation audit exposed a misleading lifecycle
assertion that expected diagnostic-error masking. Bounded remediation corrected that
contract and verified 22 focused lifecycle cases and 68 total unit tests. Default
collection selects 73 normal tests and excludes the demo; all five native comparisons
passed again with zero changed pixels, and the intentional demo again failed at the
real comparison assertion (exit 1). Reference hashes and comparison policy are unchanged.

### Configuration ownership and precedence

**No runner `.env` file is needed or loaded.** Python reads the inherited process
environment when creating a driver or executing a test. PyCharm Run works with the
existing interpreter and defaults; optional overrides belong in its run configuration's
environment field. The CLI equivalent was verified; the PyCharm GUI itself was not.
An extra `.env.example` or dotenv dependency would duplicate this table without adding
loading behavior, so neither is introduced.

| Runner variable | Default | Effect / validation |
| --- | --- | --- |
| `VVP_METRO_HOST` | `127.0.0.1` | Host inserted into the development-client URL. Must be reachable from Android. |
| `VVP_METRO_PORT` | `8081` | Port inserted into that URL; does not start or configure Metro or ADB reverse. |
| `VVP_QA_LAUNCH_URL` | unset | Compatibility override, not required. Nonempty full URL takes precedence over host/port; exactly one matching `qa_scenario` is required before opening Appium. Empty value uses generated URL. |
| `VVP_APPIUM_URL` | `http://127.0.0.1:4723` | Existing Appium endpoint; server address/port are configured separately at server startup. |
| `VVP_ANDROID_DEVICE` | `Pixel_10` | Appium device name. |
| `VVP_ANDROID_UDID` | `emulator-5554` | Actual Android target. |
| `VVP_ANDROID_PACKAGE` | `de.volksverpetzer.app` | Installed package, termination and package-aware locators. Does not install an APK. |
| `VVP_ANDROID_ACTIVITY` | `.MainActivity` | Appium capability; explicit scenario launch uses the development-client URL. |
| `VVP_GOLDEN_PROFILE` | `pixel10-api37` | Both baseline and artifact directory. Requires `[a-z0-9_-]+`; does not change screen/OS configuration. |
| `VVP_CHANNEL_TOLERANCE` | `12` | Existing override in long/dark/no-image/empty tests only; integer 0–255, validated by comparator after capture. |
| `VVP_MAX_CHANGED_RATIO` | `0.002` | Same four tests only; float 0–1. `breaking_news` and the intentional demo always use comparator defaults. |

Leave both tolerance variables **unset** for the approved five-scenario policy. Their
existing asymmetry is documented, not changed in this audit. The comparator CLI accepts
its own `--channel-tolerance` / `--max-changed-ratio` arguments and does not read these
environment variables. Pixel comparison considers RGB, not alpha; dimension mismatch
always fails. Invalid numeric conversions/ranges fail, but host/port/endpoint/package
overrides do not have comprehensive early validation. A malformed URL with a matching
scenario can pass the override check and fail at native launch; inspect the error rather
than interpreting it as a visual mismatch. Empty values generally override defaults,
so remove unwanted variables instead of setting them to empty strings.

**App/Metro configuration is separate.** `app/.env.sample` documents `APP=volksverpetzer`
and `EXPO_NO_TELEMETRY=1`; it is a template, not a runner configuration file. Expo's
existing loader reads app `.env` files, with inherited process variables taking priority.
`APP` is read when Expo evaluates `app.config.ts` (default `volksverpetzer`; any other
value currently selects Mimikama, so use the documented value). `BUILD_FOSS_ONLY=true`
and optional `BUILD_LABEL` affect app config/builds, not screenshot selection.
`google_services` / `google_services_mimikama` are optional native service-file paths;
those files and signing credentials remain private and are not needed as Python options.

`EXPO_PUBLIC_QA_SCENARIO` is bundled by Expo/Metro and used only as the development
fallback when the initial URL omits `qa_scenario`. Normal tests send an explicit scenario,
which takes precedence; `none` disables the fallback. Selection is resolved once before
providers/feed mount. `__DEV__` gates QA behavior, and the theme override is nonpersistent.
Do not change Metro's environment between scenarios. `NODE_OPTIONS=--dns-result-order=ipv4first`
is the documented local Node startup setting for IPv4 connectivity. None of the listed
visual-runner settings are secrets; **never put credentials in `EXPO_PUBLIC_*`**, which
is client-visible. Do not print local `.env` contents in diagnostics.

**Future CI (proposed):** supply non-sensitive runner values as job environment variables,
then run the same pytest commands after separately provisioning the emulator, installed
development app, Metro and Appium. Keep profile/rendering settings aligned with references,
leave tolerance overrides unset, and archive `artifacts/` even on failure. Supply any
future build credentials through the CI secret store, not committed files or public Expo
variables. Independent jobs need isolated devices/output directories; the current rolling
artifact names are not safe for concurrent workers in one checkout. No CI execution is
claimed. Root/nested ignore rules exclude real `.env`/`.env.*`, generated outputs and
credential files while permitting reviewed `.env.sample` / `.env.example` templates;
ignore rules do not replace a staged-content review.

### Runtime-selected cold launch (verified Android contract)

The development-only startup gate now resolves React Native's initial launch URL
before mounting the app providers and feed. The URL query `qa_scenario` overrides
`EXPO_PUBLIC_QA_SCENARIO`; absent URL selection retains that environment fallback.
`qa_scenario=none` explicitly disables the fallback. Without either selection the
normal application runs. Release builds bypass the gate and ignore QA selections.
`long_headline`, `breaking_news`, `dark_article`, `no_image` and `empty_feed` are
capture-supported, and each has a human-approved Android reference. A registered scenario marked not capture-supported would show an unavailable
screen; unknown/empty/duplicate selections show an invalid-selection screen.
Neither state mounts the feed or emits article-ready identifiers.

The selection is immutable for the JS launch. No URL-change listener or persistent
scenario setting is used. Fast Refresh, foreground activation and a warm deep link
are not scenario reset mechanisms. Use the explicit launch URL for visual comparison (the tests now build it automatically); environment-fallback activation is compatibility behavior and may not match this reference.

**Verified on the installed Android development client (EXEC-024):**
with Metro, the installed app, emulator and Appium already available, run from
`qa_visual/`:

```powershell
# Android must reach the same Metro address (this example uses adb reverse).
adb -s emulator-5554 reverse tcp:8081 tcp:8081
$env:VVP_QA_LAUNCH_URL = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=long_headline'
try {
    .\.venv\Scripts\python.exe -m pytest .\tests\test_long_headline.py -m visual -v -s
} finally {
    Remove-Item Env:VVP_QA_LAUNCH_URL -ErrorAction SilentlyContinue
}
```

In this opt-in mode the driver terminates the prior app, opens the link via
UiAutomator2 `mobile: deepLink`, then waits for accessibility identity
`qa-scenario:long_headline` **before** the existing article-ready wait and capture.
The compatibility activation path also checks this identity before returning the
driver. The identity is a transparent 1px accessibility element outside the card region;
its Android exposure and ordering before card readiness were verified. Test cleanup
terminates the app before quitting the session. Bounds, title assertion and comparison
policy are unchanged; the golden was intentionally migrated as documented below.
Save rolling artifacts under distinct diagnostic filenames before a second execution;
never replace a golden without approval.

For negative/launch-order inspection, this is a documented ADB example (the exact
copy-and-paste command below was not rerun during baseline migration):

```powershell
adb -s emulator-5554 shell am force-stop de.volksverpetzer.app
$launch = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=empty_feed'
adb -s emulator-5554 shell "am start -W -a android.intent.action.VIEW -d '$launch' de.volksverpetzer.app"
```

Cold-launch separately with `long_headline`, `empty_feed`, an unknown ID, and
`none`; inspect identity/unavailable markers and absence of false article readiness.
(Historical note: when this procedure was written `empty_feed` was not yet
capture-supported; since EXEC-031 it is an active scenario, so use an unknown ID
for the negative case.)
Keep Metro's environment unchanged throughout. `none` must suppress even a
Metro environment fallback; a launch without a query can legitimately use it.
Do not use `pm clear` or wipe storage. The development-client wrapper explicitly
loads Metro and retains the outer scenario query; the guarded native-intent route
maps this QA wrapper to `/home`. Source inspection shows a plain app scheme can
open the launcher chooser on a cold start; it is not the documented dev-client
procedure. Wrapper delivery, exact identity and consecutive cold launches were
verified on the installed Android development client. Unknown/unsupported/none
behavior was exercised in EXEC-021; these negative checks were not repeated during
EXEC-024. If the launcher consumes the URL or opens its chooser, stop rather than
sending a delayed live-switch event.

Cold launch resets in-memory pagination, scroll and pending requests by destroying
the process. Stored theme, settings, badges and onboarding remain intact. Existing
fixture suppressions of announcements, notifications and article network effects
remain in place; this is not app-wide network isolation. A development-only, nonpersistent
theme override selects dark for `dark_article` and light for the other four supported scenarios.
Missing-media and successful-empty behavior are described in their scenario sections below. A development-client procedure
is not proof of a standalone CI-ready QA build; no CI or iOS execution is claimed.

Run these commands from `qa_visual/`:

```powershell
# Unit tests do not start an Appium session.
.\.venv\Scripts\python.exe -m pytest -m unit -q

# Show which tests pytest discovers; collection does not run the visual scenario.
.\.venv\Scripts\python.exe -m pytest --collect-only -q

# Run one native Android scenario; requires the running emulator, app,
# Metro and Appium server described above. The test selects its own scenario.
.\.venv\Scripts\python.exe -m pytest .\tests\test_long_headline.py -v -s
```

The unit suite and collection command passed during prior execution. The visual command also passed after promotion of the reviewed baseline. A run with no baseline deliberately fails after capturing the actual and context screenshots, with a `Golden missing` message; this is not a successful comparison.

## Breaking-news banner: approved Android reference

This is a development-only **sample-app extension created for the challenge**,
not a verified upstream VVP production breaking-news feature. `AnnouncementCard`
is not reused: it has dismiss/action/impression behavior unsuitable for this
static scenario. `QaBreakingBanner` uses real React Native views and the existing
Typography/spacing primitives, a fixed red treatment, `EILMELDUNG`, and a synthetic
German headline. No animation, dismissal, live timestamp, remote media or banner
analytics is added.

The same immutable launch gate selects `qa_scenario=breaking_news`. The typed
registry enables it; `qaActiveScenario` controls the QA-only feed header. The banner
scenario reuses the original deterministic WordPress-mapped article underneath,
without changing its data or image. The banner requires `__DEV__`,
active fixture mode and exact breaking-news selection; normal/release execution
renders no banner. Production gating was tested at source/unit level, not by
running a release APK.

From `qa_visual/`, with the existing services ready:

```powershell
$env:VVP_QA_LAUNCH_URL = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=breaking_news'
try {
    .\.venv\Scripts\python.exe -m pytest .\tests\test_breaking_news.py -m visual -v -s
} finally {
    Remove-Item Env:VVP_QA_LAUNCH_URL -ErrorAction SilentlyContinue
}
```

The test verifies `qa-scenario:breaking_news`, waits for
`qa-breaking-banner-ready` (positive container and title onLayout measurements),
then observes unchanged banner bounds across consecutive Appium polls. It asserts
the exact `qa-breaking-banner-title`, checks label/title containment and viewport
bounds, and screenshots the banner element itself. `HomeScreen.breaking_banner`
exposes this separate Component Object; no article-parent assumption is reused.

The human reviewed the EXEC-025 banner candidate and full-screen context and
explicitly approved its exact PNG on November 7, 2026. EXEC-026 copied those bytes
without modification to `baselines/android/pixel10-api37/breaking_news.png`.
This approved reference was committed in local checkpoint `f0b38e9`.

Approved SHA-256:
`E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F`.

After promotion, two independent runtime-selected cold-launch pytest executions
each passed (exit 0), with zero changed pixels against the new reference. Both
actual PNGs were 1028 x 493 RGBA at `[26,720][1054,1213]`, byte-identical and
decoded-pixel-identical to each other and the approved image. Raw and
comparator-adjusted repeat differences were both zero; thresholds remain channel
delta >12 and maximum changed ratio 0.002. The headline wraps in four readable
lines, with the banner below the header and above the deterministic article.
The earlier EXEC-025 missing-baseline failures remain historical capture evidence;
they do not describe the current approved-reference status.

The `long_headline` test also passed after promotion (exit 0, zero changed pixels)
against its unchanged approved image. A future intentional baseline update still
requires reviewing the exact newly captured PNG/hash, context and comparison
evidence before replacement, followed by native verification. No automatic golden
regeneration or acceptance is supported.

Local review materials were kept under a gitignored `debug-logs/exec025/review/` directory in the original author's checkout; they are not in Git and do not exist in a fresh clone.
These are historical diagnostic material, not required checkout dependencies.
Runner artifacts under `artifacts/android/pixel10-api37/` include
`breaking_news.actual.png`, `.context.png`, `.capture.json`, `.hierarchy.xml`,
`.diff.png` and `.comparison.json`. EXEC-026 run evidence was preserved separately
in `exec026-breaking1/`, `exec026-breaking2/` and `exec026-long-headline/` under that
artifact profile in the original author's checkout; `artifacts/` is gitignored, so a
fresh clone contains none of these until the tests are run. iOS and CI execution remain unverified.

## Golden images and comparison

The test's default Android golden is:

```text
baselines/android/pixel10-api37/long_headline.png
```

### Human-reviewed runtime baseline migration (November 7, 2026)

The tracked reference path now contains the explicitly approved runtime-selected
native screenshot, copied byte for byte from the reviewed candidate. This migration
was committed in local checkpoint `f0b38e9`. It replaces the previous legacy environment-fallback
reference; the original remains recoverable from Git history at commit
`ae07a0a7cbfae8be329d2e1a63d32ede575f32c9` using this same baseline path.

- Current approved SHA-256: `6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC`.
- Previous SHA-256: `E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629`.
- Both native card PNGs are 1028 × 1237 RGBA. The image region is 526 px high under
  runtime selection versus 527 px in the legacy rendering. The earlier difference
  was 11,640 changed pixels (0.915356%); human review explicitly accepted this
  measured rendering difference after inspecting the originals and comparison aids.
- Two independent runtime cold-launch pytest executions passed against the new
  reference, exit 0 each, with zero changed pixels. Both actual PNGs were byte-identical
  to the approved candidate and to each other in this verification.
- The comparator remains RGB channel difference >12, maximum changed ratio 0.2%.
  Legacy fallback may no longer visually match the runtime-selected reference.
- Startup-dependent geometry is observed; the underlying native fractional-layout
  rounding mechanism remains unresolved. This is an intentional reviewed baseline
  migration, not a proven native-layout fix or a claim of universal byte repeatability.

Android/device profiles use separate directories; do not reuse this image for iOS
or a different device/rendering profile.

The test captures the Appium element screenshot to `artifacts/android/<profile>/long_headline.actual.png`, then compares it to the golden. The full-screen context PNG is diagnostic only and is not compared because items such as the status-bar clock can change. The default policy counts a pixel as changed when any RGB channel differs by **more than 12**, and passes only if no more than **0.2%** of pixels are changed. Different dimensions always fail. The test writes a red-overlay diff and comparison JSON when it reaches comparison; thresholds can be overridden with environment variables, but changing them is not a substitute for investigating a mismatch.

### Review and manually promote a replacement

Regeneration means **capture a fresh candidate, review it, explicitly approve its hash,
then promote and verify**. A green comparison alone is not approval. Tests never write
references. The commands below apply to all five scenario names: `long_headline`,
`breaking_news`, `dark_article`, `no_image`, `empty_feed`.

**1. Capture and preserve.** With the existing services ready, run from `qa_visual/`.
Use the matching device profile; the profile variable names directories and does not
configure the emulator. Remove a stale full-URL override before changing scenarios.

```powershell
$scenario = 'breaking_news' # Choose one of the five names above.
$env:VVP_GOLDEN_PROFILE = 'pixel10-api37'
Remove-Item Env:VVP_QA_LAUNCH_URL -ErrorAction SilentlyContinue
$profile = $env:VVP_GOLDEN_PROFILE
$output = Join-Path $PWD "artifacts/android/$profile"
$captureStarted = Get-Date
.\.venv\Scripts\python.exe -m pytest ".\tests\test_$scenario.py" -v -s
$captureExit = $LASTEXITCODE
Write-Host "pytest exit: $captureExit"
$actual = Join-Path $output "$scenario.actual.png"
if (!(Test-Path $actual) -or (Get-Item $actual).LastWriteTime -lt $captureStarted) {
    throw 'No fresh native capture; inspect the test failure before continuing.'
}
$review = Join-Path $PWD ("artifacts/review/" + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $review -ErrorAction Stop | Out-Null
Get-ChildItem -LiteralPath $output -Filter "$scenario.*" -File |
    Where-Object { $_.LastWriteTime -ge $captureStarted } |
    Copy-Item -Destination $review -ErrorAction Stop
$candidate = Join-Path $review "$scenario.actual.png"
.\.venv\Scripts\python.exe -c "from PIL import Image; import sys; im=Image.open(sys.argv[1]); im.load(); print(im.format, im.size, im.mode)" $candidate
Get-FileHash -LiteralPath $candidate -Algorithm SHA256
Write-Host "Review packet: $review"
```

The test verifies identity, readiness and content before native element capture. Inspect
its outcome: a missing golden or pixel mismatch can be expected when proposing a change;
an earlier Appium/readiness failure is not a valid candidate. A missing golden writes
actual/context but no new diff/metrics. Compare timestamps so old rolling artifacts are
not mistaken for new results. A mismatch writes diff/JSON and exits 1; a pass exits 0.

**2. Review.** Inspect candidate, context, approved reference, diff and comparison JSON.
Check complete capture boundaries, content, theme, wrapping, media and readability.
For `empty_feed`, review the message only; donation controls remain outside its reference.
Repeat capture into a separate review directory to check stability when changing visuals.
Record the reviewer's approval of the exact candidate SHA-256 and the reason for change.
Keep the preserved candidate unchanged during review.

**3. Promote only after approval.** In the same PowerShell session, the following block
requires the approved hash and explicit confirmation. Existing references get a verified
backup in the review directory; an existing backup stops the operation. To rehearse,
set `$baseline` to a path in a fresh `artifacts/rehearsal/` directory instead.

```powershell
$baseline = Join-Path $PWD "baselines/android/$profile/$scenario.png"
$backup = Join-Path $review "$scenario.previous-approved.png"
$approvedHash = Read-Host 'Paste the SHA-256 explicitly approved by the reviewer'
if ($approvedHash -notmatch '^[0-9a-fA-F]{64}$' -or
    (Get-FileHash -LiteralPath $candidate -Algorithm SHA256).Hash -ne $approvedHash) {
    throw 'Candidate does not match the approved hash.'
}
$confirmation = Read-Host "Type PROMOTE to authorize copying the reviewed candidate to $baseline"
if ($confirmation -cne 'PROMOTE') { throw 'No promotion authorized.' }
$replacing = Test-Path -LiteralPath $baseline
if ($replacing) {
    $previousHash = (Get-FileHash -LiteralPath $baseline -Algorithm SHA256).Hash
    [IO.File]::Copy($baseline, $backup, $false) # Fails if backup already exists.
    if ((Get-FileHash -LiteralPath $backup -Algorithm SHA256).Hash -ne $previousHash) {
        throw 'Backup verification failed.'
    }
}
[IO.Directory]::CreateDirectory((Split-Path -Parent $baseline)) | Out-Null
[IO.File]::Copy($candidate, $baseline, $replacing) # Overwrite only after confirmation + backup.
if ((Get-FileHash -LiteralPath $baseline -Algorithm SHA256).Hash -ne $approvedHash) {
    throw 'Destination verification failed; retain the backup and investigate.'
}
Get-FileHash -LiteralPath $baseline -Algorithm SHA256
```

**4. Verify.** After a real, approved promotion, run the same native test again and check
the reference hash is unchanged. Require a passing comparison before committing the
reviewed PNG and its approval record. A rehearsal comparison validates the byte-copy
procedure only and does not approve a reference:

```powershell
.\.venv\Scripts\python.exe -m pytest ".\tests\test_$scenario.py" -v -s
if ($LASTEXITCODE -ne 0) { throw 'Post-promotion native comparison failed.' }
if ((Get-FileHash -LiteralPath $baseline -Algorithm SHA256).Hash -ne $approvedHash) {
    throw 'Reference changed during verification.'
}
```

EXEC-036 verified fresh native captures for all five scenarios and rehearsed this
promotion block against temporary files, including absent/existing destinations,
backup preservation, declined authorization and wrong-hash rejection. No approved
reference was replaced during that verification.

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

- Android `long_headline`, `breaking_news` and `dark_article` have approved references and passing local native comparisons on Pixel_10/API 37. `no_image` (a development-only, challenge-scoped absent-media variation; no production-wide optional-media support is claimed) also has an approved reference and passing comparisons. `empty_feed` (a successful
zero-item fetch, not offline or error coverage) has an approved message-region reference
and passing comparisons, and is tracked in Git.
- There is no native iOS execution, iOS baseline, or verified CI pipeline.
- The [intentional failure demonstration](#intentional-visual-failure-demonstration) fails against a deliberately incorrect reference. It demonstrates the failure path and its artifacts, not a detected application UI regression.
- The card screenshot target resolves the ready element's direct parent based on the current UiAutomator2 hierarchy. Bounds checks guard the captured relationship, but a future app/accessibility-tree change may require inspection and a new reviewed golden.
- Snapshot consistency depends on matching app build, emulator resolution/density, font scale, theme, assets and rendering environment.
- The golden path is tracked; the approved runtime migration at `baselines/android/pixel10-api37/long_headline.png` was committed in local checkpoint `f0b38e9`. The previous reference remains in Git history.
- Installation/build instructions marked above as documented setup steps were not all re-run end-to-end during this documentation task. Refer to the task history for exact verified command outcomes.


## Dark article: approved Android reference

`qa_scenario=dark_article` reuses exactly the existing synthetic WordPress article,
bundled cover, mapper, Feed, GenericPost and ArticlePost. No duplicate article UI
or modified image is used. Before the app providers/feed mount, the immutable QA
selection enables a read-only override in `useAppColorScheme()`: dark for this
scenario, light for `long_headline` and `breaking_news`. It bypasses device/stored
appearance preferences only while the development QA fixture is active; it never
calls the persistent theme setter. Normal/release appearance logic remains intact.
No release build was executed to prove that boundary at runtime.

From `qa_visual/`, with the existing emulator, fixture-enabled Metro and Appium ready:

```powershell
$env:VVP_QA_LAUNCH_URL = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=dark_article'
try {
    .\.venv\Scripts\python.exe -m pytest .\tests\test_dark_article.py -m visual -v -s
} finally {
    Remove-Item Env:VVP_QA_LAUNCH_URL -ErrorAction SilentlyContinue
}
```

The test verifies exact scenario identity, image-loaded article readiness,
`qa-theme:dark` (the effective hook result on the article), the complete expected
QA-FIXTUR title, repeated stable outer/title bounds and viewport containment.
The existing parent-element screenshot method retains its containment/larger-bottom
checks. Theme accessibility metadata introduces no visible element or layout change.
Artifacts use `dark_article.actual.png`, `.context.png`, `.capture.json` and
`.hierarchy.xml`; `.diff.png` / `.comparison.json` are written only when an approved
baseline exists and comparison runs.

EXEC-027: dark -> light long_headline -> dark cold launches used the same Metro
process/environment. Both dark PNGs were 1028 x 1237 RGBA, bounds
[26,720][1054,1957], byte-identical, with zero raw or tolerance-adjusted pixel
differences. Their SHA-256 is
`6FD667E87476F941F7CB7A8152F60FFB8C51A3FD4217A7E993300AB32EB62A96`.
Those historical EXEC-027 pytest runs exited 1 **only for the then-missing approved golden**.
EXEC-028 subsequently promoted the exact human-approved PNG and verified passing reference regressions. The existing
long_headline and breaking_news regressions each passed with zero changed pixels;
both approved golden hashes remained unchanged.

The local review packet (`debug-logs/exec027/review/`) is gitignored: it exists only in the original author's checkout, not in a fresh clone.
It contains the candidate, context, repeatability diff/JSON and review notes.
On November 7, 2026, the human explicitly approved that exact candidate/hash.
EXEC-028 copied its bytes without pixel modification to
`baselines/android/pixel10-api37/dark_article.png`. The addition was committed in
local checkpoint `f0b38e9`. Any replacement still requires explicit human review; the
runner never regenerates or approves references automatically.
The unchanged real dark palette includes background #050D0F, text #F7F7F7 and muted
text #AAAAAA. The stored themePreference was observed as `system` before the light
and second dark launches and after; tests also cover opposing stored/device themes
without writes. Other persisted state still survives cold launch. No CI or iOS
execution is implied.


EXEC-028 post-promotion verification: two independent dark cold-launch tests
passed (exit 0, 20.52s / 17.21s), each with 0 of 1,271,636 pixels changed.
Actual PNGs were byte-identical and decoded-RGBA-identical; raw differences 0,
maximum channel delta 0, tolerance-adjusted differences 0. Both light regressions
passed with zero changed pixels and observed effective light appearance. A third
dark launch after the light scenarios also passed (exit 0, 17.14s), byte-identical
to the first dark. All three golden hashes remained correct. Stored themePreference
remained `system`; no setting was changed. Evidence was preserved (in the gitignored
`artifacts/` directory of the original author's checkout, not in a fresh clone) under
`artifacts/android/pixel10-api37/exec028-dark1/`, `exec028-dark2/`,
`exec028-long-light/`, `exec028-breaking-light/` and `exec028-dark-after-light/`.
Each includes actual/context/diff/comparison JSON and logs; dark runs additionally
include capture metadata and hierarchy. Repeatability metrics are in the ignored
root `debug-logs/exec028/` directory (gitignored, local to the original author's checkout; not present in a fresh clone). These are local Android results, not CI or
native iOS execution.

## No-image: approved Android reference

`qa_scenario=no_image` (EXEC-029) feeds a second synthetic WordPress article with the
same title, author, date and summary as `long_headline`, but **genuinely absent featured
media**: no `wp:featuredmedia` link, no `imageUrl`, and a distinct slug `qa-no-image`.
An explicit, development-only QA media contract (`getQaArticleMedia` in
`app/src/screens/Home/fixtures/qaScenario.ts`) maps that slug to `"none"` only while
`no_image` is the active launch scenario; it returns `undefined` for every production
article and in release builds.

The real `ArticlePost` then omits its image wrapper (no image, placeholder, spinner or
reserved height). Readiness is `qa-article-no-image-ready`, set from the text block's
`onLayout`, never from image `onLoad`. Production articles keep the unchanged image path.
This is a challenge-scoped QA adaptation, **not** verified upstream VVP support for
image-less teaser cards and not a general optional-media change.

The test (`tests/test_no_image.py`) asserts the exact scenario identity, effective light
theme, exact title, text-layout readiness, stable bounds, **zero native `ImageView`
descendants inside the outer card**, and that the image-bearing ready marker is absent.

```powershell
$env:VVP_QA_LAUNCH_URL = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=no_image'
.\.venv\Scripts\python.exe -m pytest .\tests\test_no_image.py -m visual -v -s
Remove-Item Env:VVP_QA_LAUNCH_URL
```

EXEC-029 produced two byte-identical 1028 × 711 RGBA native captures. On November 7,
2026 the human reviewed the candidate and its full-screen context and explicitly approved
only SHA-256 `AC5BD84B93778F4773B3A38ABD391A89483295446A2E096DD59E21CA288B3012`. The
apparent lack of outer padding in the PNG is intentional: the golden is an **element
screenshot of the outer card only**, while the diagnostic `no_image.context.png` (never
compared, because the status bar is dynamic) shows the surrounding feed margins.

EXEC-030 copied those exact bytes to `baselines/android/pixel10-api37/no_image.png`
(no regeneration). Two independent `no_image` cold-launch comparisons then passed with
0 / 730,908 changed pixels (byte-identical actuals, card bounds `[26,837][1054,1548]`,
zero `ImageView`s in the card), and `dark_article`, `long_headline` (after dark) and
`breaking_news` also passed with zero changed pixels. Thresholds are unchanged (channel
delta >12, maximum changed-pixel ratio 0.002). The EXEC-029/030 review packets and
metrics are under gitignored `debug-logs/` directories local to the original author's
checkout (not present in a fresh clone). Native iOS and CI execution remain unverified.

## Empty feed: approved Android reference

`qa_scenario=empty_feed` (EXEC-031) is a deterministic **successful-empty** scenario: the
home feed keeps exactly one configured synthetic source (`qaFeedFetcher`), and that source
resolves successfully with `[]`. It is **not** offline, HTTP-error, loading or
zero-configured-feeds coverage, and it makes no WordPress request.

Because the production `FetcherUtilities` converts fetch exceptions into `[]`, an empty
list alone cannot prove success. A development-only outcome record (`getQaFeedOutcome` /
`isQaSuccessfulEmptyFeed` in `app/src/screens/Home/fixtures/qaFeed.ts`) is written only
when the fixture source resolves; `Feed` clears it before every request, so a failed or
stale request can never satisfy readiness.

The real `Feed` renders its normal `ListEmptyComponent` (`EmptyComponent`). In this
scenario only, the message region (icon + "Keine Ergebnisse. ..." text) receives
`qa-empty-feed-ready` once the outcome is a successful zero-item fetch, initial loading and
refresh have finished, there are no posts and the region has a measured layout. Production
and other scenarios pass no QA props, so the empty state is unchanged there.

The capture boundary is that message region only. The sibling donation card (amount
picker, payment buttons) and the full screen are excluded; the full-screen
`empty_feed.context.png` is diagnostic only. The test (`tests/test_empty_feed.py`) asserts
identity `qa-scenario:empty_feed`, light theme, readiness, stable bounds, the exact
message, and zero article markers, fixture titles, breaking-banner elements, loading text,
progress bars and pending empty markers.

```powershell
$env:VVP_QA_LAUNCH_URL = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=empty_feed'
.\.venv\Scripts\python.exe -m pytest .\tests\test_empty_feed.py -m visual -v -s
Remove-Item Env:VVP_QA_LAUNCH_URL
```

EXEC-031 ran long_headline, empty_feed, long_headline, empty_feed as separate cold launches
through the same Metro process. Both empty captures were byte-identical (1028 × 309 RGBA,
bounds `[26,825][1054,1134]`, 0 raw changed pixels). Both populated runs passed, and no
articles or banners from the populated runs appeared in the empty runs.

On November 7, 2026 the human reviewed the candidate and its full-screen context. They
explicitly approved only SHA-256
`903B971081AC2EA2FEB2A37D1B73473602E176A8E9FFE046074E7D3BDE5FA795`. They also approved
the message-only boundary, which excludes the donation card, payment controls, the
dynamic status bar and development warnings. EXEC-032 copied those exact bytes to
`baselines/android/pixel10-api37/empty_feed.png` with no regeneration.

EXEC-032 then ran six separate cold launches through the same Metro process, in this
order: `empty_feed`, `long_headline`, `breaking_news`, `dark_article`, `no_image`,
`empty_feed`. Every launch passed (exit 0) with zero changed pixels, and every actual
was byte-identical to its golden. The two `empty_feed` actuals were byte-identical
(0 / 317,652 changed). No article, banner or dark-theme state leaked into a later
scenario. Thresholds are unchanged. This is local sequential execution, not CI. The
`empty_feed` golden and implementation are tracked in Git.

### Running all five approved scenarios

Each scenario is a separate cold launch through the same running Metro process; no
Metro restart or environment change is needed between them. Each test selects its own
scenario. From `qa_visual/`:

```powershell
.\.venv\Scripts\python.exe -m pytest .\tests -m visual -v
```

Baselines change only after explicit human review of the exact candidate PNG and its
SHA-256; tests never create or update a golden.

## Intentional visual failure demonstration

`tests/test_intentional_visual_failure.py` shows what a **real visual-comparison failure**
looks like, including its artifacts. It is an **intentional reference-mismatch
demonstration, not an application UI regression**: the app, fixture and styling are
unchanged and render correctly. The test runs the normal `breaking_news` cold launch,
identity, readiness, title check and native banner capture. It then compares the capture
with a deliberately incorrect reference,
[`demo_assets/intentional_mismatch_breaking_news.png`](demo_assets/intentional_mismatch_breaking_news.png),
which has its red and blue channels swapped. The comparator, thresholds (channel delta
>12, maximum ratio 0.002) and the approved `breaking_news.png` golden are all unchanged.
The test is expected to **FAIL with exit code 1** at the comparison assertion; it does not
use `xfail`, `skip` or an inverted assertion.

The test is marked `@pytest.mark.intentional_failure` and requests its launch with
`@pytest.mark.qa_scenario("breaking_news")`. It does **not** carry the `visual` marker.
`pytest.ini` registers the
marker and adds `-m "not intentional_failure"` to `addopts`, so it is deselected by
default and excluded from `-m visual` and `-m unit`. Passing `-m intentional_failure` on
the command line overrides the default and selects exactly this one test. Running the file
without that argument reports `1 deselected` (pytest exit code 5).

### PowerShell: PASS → intentional FAIL → PASS

The prerequisites are the same as for `breaking_news`: emulator `emulator-5554` booted
with the development app installed, Metro on port 8081 (started as described above) and
Appium on port 4723. From `qa_visual/`:

```powershell
.\.venv\Scripts\python.exe -m pytest .\tests\test_breaking_news.py -v -s                                      # expected PASS, exit 0
.\.venv\Scripts\python.exe -m pytest .\tests\test_intentional_visual_failure.py -m intentional_failure -v -s # expected FAIL, exit 1
.\.venv\Scripts\python.exe -m pytest .\tests\test_breaking_news.py -v -s                                      # expected PASS, exit 0
```

No launch URL is needed; both tests cold-launch `breaking_news` themselves.

### PyCharm

Create a **pytest** run configuration (or edit the one the Run icon creates):

- Python interpreter: the existing project interpreter `qa_visual/.venv/Scripts/python.exe`.
- Target: script path `qa_visual/tests/test_intentional_visual_failure.py`.
- Additional arguments: `-m intentional_failure -v -s`. Without this, the test is
  reported as deselected.
- No environment variables are required. Emulator, Metro and Appium must already be
  running, as above.

The run should end red with one failed test (exit code 1). The console prints
`identity, readiness and title verified`, the changed-pixel count and an
`AssertionError: INTENTIONAL visual mismatch (demo reference, not an app regression)`.
For the normal PASS, use the Run icon on `tests/test_breaking_news.py`; no extra
arguments are needed.

### Artifacts and how to read them

Written to `artifacts/android/pixel10-api37/` (ignored by Git), separate from the
`breaking_news.*` files:

- `intentional_failure.actual.png`: the native banner capture. It is byte-identical to the
  approved golden, which shows the app itself did not regress.
- `intentional_failure.diff.png`: the capture with every changed pixel painted red-pink.
  Open it in any image viewer; here almost the whole banner background is marked, while
  the unchanged white text is not.
- `intentional_failure.comparison.json`: dimensions, changed pixels, ratio, thresholds and
  `"passed": false`.
- `intentional_failure.context.png` and `intentional_failure.capture.json`: uncompared
  full-screen context and capture metadata (rect, session, reference path).

Because the failure happens at the comparison assertion, no `failure-full-screen.png` or
`failure-page-source.xml` is written; those diagnostics appear only for earlier Appium,
locator or readiness failures.

Verified locally in EXEC-033 (Pixel_10/API 37, not CI): `breaking_news` PASS (0 changed
pixels) → intentional demo FAIL, exit 1, 468,349 of 506,804 pixels changed (92.41%) against
a 0.2% limit → `breaking_news` PASS (0 changed). All five normal scenarios then passed
with zero changed pixels. EXEC-035 repeated the explicit demonstration with no launch URL
set: it selected `breaking_news` itself and failed with the same 468,349 / 506,804 result
(exit 1).

To regenerate the demo reference deterministically from the approved golden (it checks
the golden's hash first and only reads it):
`.\.venv\Scripts\python.exe demo_assets\generate_intentional_mismatch.py`.

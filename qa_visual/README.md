# Android visual regression demo

This runner captures five deterministic visual scenarios in the real Volksverpetzer React Native application. The `long_headline` fixture feeds synthetic article data through the app's normal React Native components; Appium/UiAutomator2 captures the rendered outer article card from Android. Pillow compares that PNG with a reviewed golden.

`long_headline`, `breaking_news`, `dark_article`, `no_image` and `empty_feed` each have an explicitly human-approved Android reference and passing local native comparisons. The implemented demo is Android only. There is no executed iOS test or verified CI pipeline.

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
are not scenario reset mechanisms. Use the explicit launch URL for visual comparison; environment-fallback activation is compatibility behavior and may not match this reference.

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
theme override selects dark for `dark_article` and light for `long_headline` and `breaking_news`.
Missing-media and successful-empty behavior remain deferred. A development-client procedure
is not proof of a standalone CI-ready QA build; no CI or iOS execution is claimed.

Run these commands from `qa_visual/`:

```powershell
# Unit tests do not start an Appium session.
.\.venv\Scripts\python.exe -m pytest -m unit -q

# Show which tests pytest discovers; collection does not run the visual scenario.
.\.venv\Scripts\python.exe -m pytest --collect-only -q

# Run the single native Android scenario; requires the running emulator, app,
# fixture-enabled Metro and Appium server described above.
$env:VVP_QA_LAUNCH_URL = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=long_headline'
try {
    .\.venv\Scripts\python.exe -m pytest .\tests\test_long_headline.py -m visual -v -s
} finally {
    Remove-Item Env:VVP_QA_LAUNCH_URL -ErrorAction SilentlyContinue
}
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
registry enables it; `qaActiveScenario` controls the QA-only feed header. All three
supported scenarios reuse the original deterministic WordPress-mapped article
underneath, without changing its data or image. The banner requires `__DEV__`,
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
`.diff.png` and `.comparison.json`. EXEC-026 run evidence is preserved separately
in `exec026-breaking1/`, `exec026-breaking2/` and `exec026-long-headline/` under that
artifact profile. iOS and CI execution remain unverified.

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

Golden updates are explicit human decisions. The approved migration above was executed and verified twice. The generic interactive example below remains a documented procedure; that exact interactive command sequence was not executed end-to-end. It does not make the test update a golden automatically.

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

- Android `long_headline`, `breaking_news` and `dark_article` have approved references and passing local native comparisons on Pixel_10/API 37. `no_image` (a development-only, challenge-scoped absent-media variation; no production-wide optional-media support is claimed) also has an approved reference and passing comparisons. `empty_feed` (a successful
zero-item fetch, not offline or error coverage) has an approved message-region reference
and passing comparisons, and is tracked in Git.
- There is no native iOS execution, iOS baseline, or verified CI pipeline.
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
remained `system`; no setting was changed. Evidence is preserved under
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
Metro restart or environment change is needed between them. From `qa_visual/`:

```powershell
foreach ($scenario in 'long_headline', 'breaking_news', 'dark_article', 'no_image', 'empty_feed') {
    $env:VVP_QA_LAUNCH_URL = "exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=$scenario"
    .\.venv\Scripts\python.exe -m pytest ".\tests\test_$scenario.py" -m visual -v -s
}
Remove-Item Env:VVP_QA_LAUNCH_URL
```

Baselines change only after explicit human review of the exact candidate PNG and its
SHA-256; tests never create or update a golden.

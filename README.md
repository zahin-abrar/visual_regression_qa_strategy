# Mobile Visual Regression QA

A focused demonstration of mobile screenshot testing with a real React Native news application. It pairs one executed Android prototype with a proposed cross-platform strategy; the proposal is not presented as an implemented or tested iOS runner.

## Project overview

The repository contains the Volksverpetzer application with a development-only deterministic fixture, a Python/pytest/Appium visual runner, and supporting documentation. The executed scope is one Android `long_headline` scenario on a Pixel_10/API 37 emulator. iOS is proposed scope only; there is no iOS implementation or execution. See the [cross-platform strategy (PDF)](deliverables/strategy.pdf) and [editable Markdown source](deliverables/strategy.md).

## What has been demonstrated

- The real Volksverpetzer React Native app rendered the deterministic `long_headline` fixture.
- Appium with UiAutomator2 captured the native outer article-card element.
- A small Python/pytest POM separates the `HomeScreen` and `ArticleCard` responsibilities.
- Two reviewed native captures were byte-identical at 1028 × 1237 pixels.
- The reviewed local Android golden was promoted and the visual test passed: **1 passed**. The comparison reported 0 of 1,271,636 changed pixels (0.0%).
- The run produced a diff image and comparison-metrics JSON under `qa_visual/artifacts/android/pixel10-api37/`.

The approved golden is at `qa_visual/baselines/android/pixel10-api37/long_headline.png`. It exists locally; Git tracking/commit status has not been verified. No CI pipeline, native iOS execution, or deliberate failing visual regression has been demonstrated.

## Architecture overview

- `app/` — Volksverpetzer React Native application and development-only fixture provider.
- `qa_visual/` — Android Appium/pytest scenario, platform-specific golden, screenshots and Pillow comparison utility.
- `HomeScreen` and `ArticleCard` Screen/Component Objects own screen access, article-card readiness, title lookup and native element capture.
- `visualqa/android.py` configures the Android Appium session; `visualqa/image_diff.py` compares PNGs and writes diff/metrics artifacts.
- Goldens are stored by platform and device profile. The current golden belongs to Android `pixel10-api37` and is not an iOS reference.

See [the runner README](qa_visual/README.md) for implementation details and setup.

## Quick start

Once the Android emulator and installed development app are ready, start Metro with the fixture enabled in one PowerShell terminal:

```powershell
Set-Location .\app
$env:EXPO_PUBLIC_QA_SCENARIO = 'long_headline'
pnpm.cmd start --clear
```

Leave Metro running. With the Appium server ready, run the visual scenario from a second terminal:

```powershell
Set-Location .\qa_visual
.\.venv\Scripts\python.exe -m pytest .\tests\test_long_headline.py -m visual -v -s
```

For emulator, app, Appium, Python environment, golden review and troubleshooting instructions, see [qa_visual/README.md](qa_visual/README.md).

## Documentation

- [Android runner, setup and golden workflow](qa_visual/README.md)
- [Sanitized AI prompt disclosure](docs/ai_prompts_used.md)
- [Cross-platform Android/iOS screenshot-testing strategy (PDF)](deliverables/strategy.pdf) ([editable Markdown](deliverables/strategy.md))

## Results and limitations

The local Android visual test passed against the human-reviewed golden after repeat-capture verification. The current implementation covers one Android fixture and depends on the current UiAutomator2 accessibility hierarchy for the outer-card screenshot target. Rendering consistency depends on using the matching app and emulator profile. There is no executed iOS test, verified CI job, or demonstrated intentional visual-regression failure.

## Attribution and license

The application is adapted from [Volksverpetzer/vvp_app](https://github.com/Volksverpetzer/vvp_app), upstream `prerelease` commit `8b421753a17a18cd648447319adcca61a288f97f`. The app directory includes [its MIT license and notice](app/LICENSE.md); retain the upstream attribution and license terms. This does not establish redistribution clearance for every logo, image, or other third-party asset bundled with the app.

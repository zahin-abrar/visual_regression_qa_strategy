# Mobile Visual Regression QA

A focused demonstration of mobile screenshot testing with a real React Native news application. It pairs one executed Android prototype with a proposed cross-platform strategy; the proposal is not presented as an implemented or tested iOS runner.

## Project overview

The repository contains the Volksverpetzer application with a development-only deterministic fixture, a Python/pytest/Appium visual runner, and supporting documentation. The executed Android scope on Pixel_10/API 37 includes three human-approved visual scenarios, `long_headline`, `breaking_news` and `dark_article`, with passing native regression comparisons. iOS is proposed scope only; there is no iOS implementation or execution. See the [cross-platform strategy (PDF)](deliverables/strategy.pdf) and [editable Markdown source](deliverables/strategy.md).

## What has been demonstrated

- The real Volksverpetzer React Native app rendered the deterministic `long_headline` fixture.
- Appium with UiAutomator2 captured the native outer article-card element.
- A small Python/pytest POM separates the `HomeScreen` and `ArticleCard` responsibilities.
- Two reviewed native captures were byte-identical at 1028 × 1237 pixels.
- After an explicit human-reviewed migration to the runtime-selected baseline, two independent cold-launch visual tests each reported **1 passed**, exit 0, and 0 of 1,271,636 changed pixels (0.0%).
- The run produced a diff image and comparison-metrics JSON under `qa_visual/artifacts/android/pixel10-api37/`.

The golden path `qa_visual/baselines/android/pixel10-api37/long_headline.png` is tracked. Its approved runtime-selected replacement is a local, uncommitted change; the previous environment-fallback golden remains recoverable in Git history. This intentional migration preserves comparison thresholds; legacy fallback may no longer match, and the underlying native layout-rounding cause remains unresolved. No CI pipeline, native iOS execution, or deliberate failing visual regression has been demonstrated.

The breaking-news banner is a development-only sample-app extension for the challenge, not a verified upstream VVP production feature. After explicit human approval and byte-for-byte promotion, two independent banner regressions passed with zero changed pixels; their 1028 x 493 captures were byte-identical. The long-headline regression also passed against its unchanged reference. The approved baseline changes remain local and uncommitted. See the [runner guide](qa_visual/README.md#breaking-news-banner-approved-android-reference) for the exact breaking-news launch command and review policy.

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
$env:NODE_OPTIONS = "--dns-result-order=ipv4first"
pnpm.cmd exec expo start --dev-client --localhost --port 8081 --clear
```

Preserve an existing healthy Metro process and its environment. With the Appium server ready, run the explicit runtime-selected visual scenario from a second terminal:

```powershell
Set-Location .\qa_visual # From the repository root.
$env:VVP_QA_LAUNCH_URL = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=long_headline'
try {
    .\.venv\Scripts\python.exe -m pytest .\tests\test_long_headline.py -m visual -v -s
} finally {
    Remove-Item Env:VVP_QA_LAUNCH_URL -ErrorAction SilentlyContinue
}
```

For emulator, app, Appium, Python environment, golden review and troubleshooting instructions, see [qa_visual/README.md](qa_visual/README.md).

## Documentation

- [Android runner, setup and golden workflow](qa_visual/README.md)
- [Sanitized AI prompt disclosure](docs/ai_prompts_used.md)
- [Cross-platform Android/iOS screenshot-testing strategy (PDF)](deliverables/strategy.pdf) ([editable Markdown](deliverables/strategy.md))

## Results and limitations

The local Android visual test passed against the human-reviewed golden after repeat-capture verification. The current implementation covers four Android fixture scenarios (`long_headline`, `breaking_news`, `dark_article`, `no_image`) with human-approved references, captured as outer-element screenshots (full-screen context images are diagnostic only), and depends on the current UiAutomator2 accessibility hierarchy for the outer-card screenshot target. Rendering consistency depends on using the matching app and emulator profile. There is no executed iOS test, verified CI job, or demonstrated intentional visual-regression failure.

## Attribution and license

The application is adapted from [Volksverpetzer/vvp_app](https://github.com/Volksverpetzer/vvp_app), upstream `prerelease` commit `8b421753a17a18cd648447319adcca61a288f97f`. The app directory includes [its MIT license and notice](app/LICENSE.md); retain the upstream attribution and license terms. This does not establish redistribution clearance for every logo, image, or other third-party asset bundled with the app.


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

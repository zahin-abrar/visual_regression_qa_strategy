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
- `qa_visual/` — Android Appium/pytest scenario, platform-specific golden, screenshots and Pillow comparison utility.
- The `HomeScreen` Screen Object and the `ArticleCard`, `BreakingBanner` and `EmptyFeedState` Component Objects own screen access, scenario-specific readiness, content lookup and native element capture.
- `visualqa/android.py` configures the Android Appium session; `visualqa/image_diff.py` compares PNGs and writes diff/metrics artifacts.
- Goldens are stored by platform and device profile. The current goldens belong to Android `pixel10-api37` and are not iOS references.

See [the runner README](qa_visual/README.md) for implementation details and setup.

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
```

In PyCharm, the normal Run action on a visual test file works with the `qa_visual/.venv` interpreter and no extra environment variables.

For emulator, app, Appium, Python environment, golden review and troubleshooting instructions, see [qa_visual/README.md](qa_visual/README.md).

## Documentation

- [Android runner, setup and golden workflow](qa_visual/README.md)
- [Sanitized AI prompt disclosure](docs/ai_prompts_used.md)
- [Cross-platform Android/iOS screenshot-testing strategy (PDF)](deliverables/strategy.pdf) ([editable Markdown](deliverables/strategy.md))

## Results and limitations

The local Android visual test passed against the human-reviewed golden after repeat-capture verification. The current implementation covers five Android fixture scenarios (`long_headline`, `breaking_news`, `dark_article`, `no_image`, `empty_feed`) with human-approved references. They are captured as native element screenshots of the outer card, the banner or the empty-state message region; full-screen context images are diagnostic only. The capture targets depend on the current UiAutomator2 accessibility hierarchy. Comparison thresholds are unchanged: channel delta >12 and a maximum changed-pixel ratio of 0.002. The first three references were committed in local checkpoint `f0b38e9` and `no_image` in `8c54f0f`. The `empty_feed` reference and its implementation are also tracked in Git. Rendering consistency depends on using the matching app and emulator profile. There is no executed iOS test or verified CI job. A marker-controlled intentional failure demonstration (EXEC-033) fails against a deliberately incorrect reference; it shows the failure path and artifacts, not a detected application UI regression.

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

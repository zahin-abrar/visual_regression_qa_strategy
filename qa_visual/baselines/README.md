# Approved visual baselines

Baselines are reviewed reference images stored by platform and rendering profile. Keep device-specific references separate; do not reuse an Android image as an iOS or different-device baseline.

## Android: Pixel_10 / API 37

### long_headline

- Scenario: `long_headline`
- Reference: [`android/pixel10-api37/long_headline.png`](android/pixel10-api37/long_headline.png)
- Status: human-reviewed and explicitly approved on November 7, 2026; runtime migration verified locally; committed in local checkpoint `f0b38e9`
- Launch contract: explicit `qa_scenario=long_headline` cold launch; exact scenario identity before article readiness
- Image: PNG, 1028 × 1237 pixels, RGBA
- SHA-256: `6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC`

The previous environment-fallback reference (SHA-256 `E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629`) remains recoverable at this PNG path in Git commit `ae07a0a7cbfae8be329d2e1a63d32ede575f32c9`. The intentional migration accepts the reviewed 526 px image region instead of the legacy 527 px rendering; the 1028 × 1237 card boundary is unchanged. Legacy fallback may no longer match. Thresholds remain >12 per RGB channel and 0.2% changed pixels. The underlying native fractional-layout mechanism is unresolved. Two independent runtime-selected visual tests passed after promotion with zero changed pixels.

### breaking_news

- Reference: [`android/pixel10-api37/breaking_news.png`](android/pixel10-api37/breaking_news.png)
- Status: exact candidate explicitly human-approved on November 7, 2026; promoted byte for byte and verified locally; committed in local checkpoint `f0b38e9`
- Launch contract: explicit `qa_scenario=breaking_news` cold launch; exact scenario identity before measured banner readiness
- Image: PNG, 1028 x 493 pixels, RGBA; complete banner bounds `[26,720][1054,1213]`
- SHA-256: `E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F`

Two independent post-promotion Appium/pytest comparisons passed (exit 0), with
zero changed pixels. Captures were byte-identical and decoded-pixel-identical.
The banner is a development-only, challenge-specific sample-app extension, not
an existing upstream VVP production feature. It is not an iOS reference; native
iOS and CI execution remain unverified. The unchanged comparison policy is RGB
channel delta >12 with maximum changed-pixel ratio 0.002.

Replacing a baseline requires explicit human review of the newly captured native element screenshot and comparison evidence. Never update a reference automatically to make a test pass. See the [runner README](../README.md#review-and-manually-promote-a-replacement) for the documented capture and promotion procedure.


### dark_article

- Reference: [`android/pixel10-api37/dark_article.png`](android/pixel10-api37/dark_article.png)
- Status: exact candidate human-approved on November 7, 2026; copied byte for byte in EXEC-028; committed in local checkpoint `f0b38e9`
- Source: ignored EXEC-027 review packet, `dark_article.candidate.png`
- Launch contract: explicit `qa_scenario=dark_article` cold launch; exact scenario and effective dark-theme markers before capture
- Image: PNG, 1028 x 1237 pixels, RGBA; complete outer-card bounds `[26,720][1054,1957]`
- SHA-256: `6FD667E87476F941F7CB7A8152F60FFB8C51A3FD4217A7E993300AB32EB62A96`

This uses the unchanged article data, bundled image and real VVP dark palette.
The development-only QA theme override is nonpersistent; light and dark scenarios
have separate reference PNGs. Thresholds remain channel delta >12 and maximum
changed-pixel ratio 0.002. Review is required before any replacement. See the
[runner guide](../README.md#dark-article-approved-android-reference) for launch commands.
Native iOS and CI execution remain unverified.


EXEC-028: two independent dark reference comparisons passed with zero changed
pixels; the two light regressions and a subsequent dark launch also passed.
All dark actuals were byte-identical to the exact approved reference. Both existing
reference hashes remained unchanged. All three approved references are distinct
scenario files; no light/dark reference sharing or automatic updates occur.


### no_image

- Reference: [`android/pixel10-api37/no_image.png`](android/pixel10-api37/no_image.png)
- Status: human-approved Android reference (November 7, 2026, after image/context review); promoted byte for byte and verified in EXEC-030
- Source: ignored EXEC-029 review packet, `no_image.candidate.png` (two byte-identical native captures)
- Launch contract: explicit `qa_scenario=no_image` cold launch; exact scenario identity, effective light theme, text-layout readiness `qa-article-no-image-ready`, zero `ImageView`s in the card
- Image: PNG, 1028 x 711 pixels, RGBA; complete outer-card bounds `[26,837][1054,1548]`
- SHA-256: `AC5BD84B93778F4773B3A38ABD391A89483295446A2E096DD59E21CA288B3012`

Same synthetic article text as `long_headline` with genuinely absent featured media. This
is a development-only, challenge-scoped QA variation of the real `ArticlePost`; it does
not claim production-wide optional-media support. The reference is an outer-card element
screenshot; feed margins appear only in the uncompared context image. Thresholds remain
channel delta >12 and maximum changed-pixel ratio 0.002.

EXEC-030: two independent `no_image` comparisons passed with zero changed pixels
(byte-identical actuals), and the three existing references passed unchanged. All four
approved references are distinct scenario files.

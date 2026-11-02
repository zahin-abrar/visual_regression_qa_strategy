# Approved visual baselines

Baselines are reviewed reference images stored by platform and rendering profile. Keep device-specific references separate; do not reuse an Android image as an iOS or different-device baseline.

## Android: Pixel_10 / API 37

- Scenario: `long_headline`
- Reference: [`android/pixel10-api37/long_headline.png`](android/pixel10-api37/long_headline.png)
- Status: human-reviewed and approved
- Image: PNG, 1028 × 1237 pixels, RGBA
- SHA-256: `E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629`

Replacing a baseline requires explicit human review of the newly captured native element screenshot and comparison evidence. Never update a reference automatically to make a test pass. See the [runner README](../README.md#review-and-manually-promote-a-replacement) for the documented capture and promotion procedure.

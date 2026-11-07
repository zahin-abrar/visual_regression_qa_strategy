# Demonstration assets (not approved goldens)

Files here are **not** baselines and are never used by the normal visual tests.

| File | Size | SHA-256 |
|---|---|---|
| `intentional_mismatch_breaking_news.png` | 1028 × 493, RGBA | `A8BBE42E3932FEA83B1FC905814310022CF75D8617FC0F019528B18E905EB3CA` |

`intentional_mismatch_breaking_news.png` is a deliberately incorrect reference for
`tests/test_intentional_visual_failure.py`. It was derived deterministically from the
approved `baselines/android/pixel10-api37/breaking_news.png` (SHA-256 `E552AD4D…438BE7F`)
by swapping the red and blue channels: the red banner becomes blue, while the white text,
alpha and dimensions are unchanged. Regenerate it from `qa_visual/` with
`.\.venv\Scripts\python.exe demo_assets\generate_intentional_mismatch.py`; the script
verifies the golden's hash and never writes to `baselines/`.

See the [runner guide](../README.md#intentional-visual-failure-demonstration).

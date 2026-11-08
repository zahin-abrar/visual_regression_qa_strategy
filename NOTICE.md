# Notice: provenance, licenses and brand assets

## Provenance

The application in `app/` is adapted from [Volksverpetzer/vvp_app](https://github.com/Volksverpetzer/vvp_app) (upstream `prerelease` commit `8b421753a17a18cd648447319adcca61a288f97f`). This repository adds a development-only QA fixture provider and QA scenarios to the app, plus the Python/Appium visual-regression runner in `qa_visual/`. The synthetic fixture image `app/assets/images/qa/fixture-cover.png` and the strategy document in `deliverables/` were added by this project.

## Software license

The upstream software is licensed under the MIT License, copyright (c) 2026 Volksverpetzer VVP gUG. The notice is retained unchanged in [`app/LICENSE.md`](app/LICENSE.md) and applies to the upstream source code as stated there. Third-party dependencies keep their own licenses (see `app/package.json` and the in-app license list, `app/src/screens/Settings/components/licenses/data.tsx`).

## Brand assets and trademarks (limitation)

The MIT license covers the software. **This repository does not claim, and MIT does not necessarily grant, any right to use names, logos, trademarks, mascot artwork or animations** belonging to Volksverpetzer, Mimikama or others. Neither the license file nor the README in this snapshot states a separate permission for such assets, and none has been obtained for this project.

The following brand-related assets are part of the upstream app snapshot and are unchanged here:

- Volksverpetzer: app icons, splash and notification images, shop/donation button images, `einhorn.webp`, `logo_pike.webp`, `logo_animated.gif`, `welcome.webp`, `404.webp`, `success.png`, and the FaktenBot Rive animations (`app/assets/rive/`).
- Mimikama (alternative app variant, selected with `APP=mimikama`; the visual tests use the default `volksverpetzer` variant): `app/assets/images/mimikama/` and `app/config/mimikama.config.ts`.

The approved reference screenshots in `qa_visual/baselines/` contain only synthetic fixture content (a QA fixture image, QA text, a generic globe icon); they do not intentionally depict these logos or mascots.

Status: asset permissions are **unresolved**. Until they are confirmed with the rights holders, or the assets are removed or replaced, treat this repository as unsuitable for public distribution or for any use that implies endorsement by Volksverpetzer or Mimikama.

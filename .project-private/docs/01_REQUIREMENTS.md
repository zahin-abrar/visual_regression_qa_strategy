# Requirements and acceptance contract

**Authority:** Axel Springer Tech *QA Manager Take-Home Challenge*, four-page PDF. This is an interpretation; the original PDF overrides it.

## Employer's explicit requirements

| ID | Requirement | Minimum evidence | Source |
|---|---|---|---|
| R01 | Strategy, about 1–3 pages, covering **iOS and Android** | `deliverables/strategy.md`/PDF | PDF pp.2–3 |
| R02 | Tool choice and trade-offs; native, cross-platform or hybrid allowed | Explained recommendation | pp.2–3 |
| R03 | Real UI from sample/adapted production-style code, with **mocked deterministic data** | Source + data injection seam + test proof | pp.2–4 |
| R04 | Golden/reference images, storage, review, approval | Versioned PNGs + documented approval flow | pp.2–3 |
| R05 | Automated PR CI/CD and Scrum integration | Strategy + workflow/config if feasible | p.2, pp.3–4 |
| R06 | Flakiness management and scalability across apps/team | Environment pinning, isolation, suite tiering, rollout | pp.2–3 |
| R07 | **Working demo on at least one native mobile platform** | Reproducible test run on Android or iOS | pp.2–4 |
| R08 | Few representative screenshots with fixed fixtures (breaking banner, teaser, paywalled item examples) | Source fixtures + screenshot assertions | pp.2–3 |
| R09 | Reference images included/committed | Golden PNG files | pp.2–3 |
| R10 | README: how to run, regenerate golden images | Tested commands | p.3 |
| R11 | Disclose prompts used | `deliverables/ai_prompts_used.md` | p.3 |
| R12 | Explain integration into a large existing codebase, including fixture location, network seam, incremental adoption | Strategy production integration/rollout | p.4 |

### Strong extras

- **E01:** Deliberate UI regression, failing screenshot diff, review workflow (explicitly a *big plus*, not mandatory).
- **E02:** Representative variants: long German headlines, image/no-image, dark mode, font size, error/offline, premium badge. Aim for a *few*, not a full matrix.
- **E03:** Optional 3–5-minute demo walkthrough/notes.

### Explicitly permitted alternatives (PDF p.3)

- **Off-device component snapshots:** e.g. iOS swift-snapshot-testing, Android Paparazzi/Roborazzi.
- **Running app/device screenshots:** e.g. Appium, Maestro, XCUITest/Espresso; execute on **local emulator/simulator or device cloud**. Cloud is **not required**.
- Visual diff via local tooling or third-party service such as Applitools/Emerge; paid service is **not required**.
- For running app mocks: **local stub/mock server** or **launch argument/build flavor swapping to fixed fixtures**. The PDF explicitly asks why this is fast and stable.
- No need to run code on both platforms: **one working demo + convincing written second-platform strategy** suffices.

## Separate user objectives from employer requirements

These are **candidate strategy preferences / interview insights**, not additional mandates stated by the PDF:

| ID | User objective | How to evaluate honestly |
|---|---|---|
| U01 | Reduce QA bottleneck as AI-assisted builds become more frequent (reported from first interview) | Fast per-PR feedback, reduced repetitive manual verification; no invented quantified savings |
| U02 | Share as much test code as is economical across Android/iOS | Shared scenarios, test data contracts, assertions, reporting and CI templates; thin adapters where useful |
| U03 | Make CI/CD-first rather than attach CI afterward | Reproducible headless tests, stable images, fail artifacts, clear baseline approval |
| U04 | Use risk-based test selection at scale | Fast PR smoke/component checks and broader nightly/release suites; avoid all-device/full-matrix PR gates |
| U05 | Consider Appium + Python/pytest as primary candidate | Evaluate against actual SUT/mock feasibility and runtime cost; not yet approved |

## Proof chain

`real rendered UI → fixed fixture (not live content) → pinned device/environment → screenshot capture → platform-specific approved golden → automated comparison → pass/fail and diff → human-reviewed baseline update`

For Appium, explicitly show **how** fixtures reach the running app. Driving the UI and taking pictures does **not** by itself satisfy R03. Production API changes must not change screenshot-test data. Also control images, time, locale, animation, asynchronous settling, font scale and theme.

## Guardrails

Do not claim native iOS verification on Windows; no claim that Axel Springer uses React Native, Jetpack Compose, or any particular app architecture; no production company code provided. Do not treat static images or a browser screenshot as equivalent to a rendered native-app component. Do not claim CI is running before a successful pipeline run. Do not include private challenge PDF in public Git even though present inside the private starter ZIP.

## Definition of done

Account for R01–R12 with actual evidence or explicit disclosed limitations. Prefer a narrowly verified vertical slice over a larger unproven implementation; do not silently upgrade optional E01 to mandatory.

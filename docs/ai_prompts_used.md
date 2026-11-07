# Sanitized AI prompt log

- **2026-11-02 — EXEC-010:** User requested a review and documentation update for the implemented Android screenshot demo, including setup, test execution, artifact interpretation, human-controlled golden review/promotion, verification limits and an execution record. No application, runner, baseline or environment changes were authorized.

- **2026-11-02 — EXEC-012:** User requested a concise Android/iOS screenshot-testing strategy grounded in the verified Android prototype. The prompt required tooling trade-offs, deterministic fixture injection, golden approval, proposed CI/Scrum integration, stability, ownership and incremental rollout, with implemented evidence distinguished from proposals. The assistant inspected the implementation and prior records, checked official tool documentation, drafted the strategy and checked its length, links and evidence claims. The source brief's 1–3 page guidance resolved malformed page/word ranges in the request; no runtime implementation or execution was authorized. This entry is a sanitized summary, not a transcript of private source material.

- **2026-11-02 - EXEC-013:** User requested narrowly scoped corrections to the existing Android/iOS screenshot strategy, a professional A4 PDF, rendered-page inspection and evidence logging. The request contained conflicting pagination wording (“13 pages” versus 1-3 pages); the source employer brief and detailed instructions support a concise 1-3 page document, so the strategy was rendered as two pages. No implementation changes were authorized.

- **2026-11-02 - EXEC-014:** User requested correction of PDF-local Markdown link rendering, reconciliation of root README strategy links, and final PDF verification. The original brief and repository requirement specify 1-3 pages; the existing approved document is two pages. A corrected two-page candidate was generated and inspected, but the official PDF was held open by another process and Windows denied safe replacement. No process was terminated.

- **2026-11-02 - EXEC-014 completion:** After the user released the PDF lock, the corrected two-page candidate was promoted to `deliverables/strategy.pdf`. All pages were rendered and inspected; local README links, seven sections, Android evidence and clean PDF reference labels were verified. The original brief specifies 1-3 pages, so the approved two-page strategy was retained.

- **2026-11-06:** User requested an explanation of the profile variable in the long-headline test and its architecture. Inspected the test, driver, page/component objects and comparator; explained directory selection versus device configuration. No implementation changes or test execution.


### EXEC-025: Breaking-news candidate preparation
Human directed a minimal development-only, nonanimated breaking-news banner in the real app feed, deterministic fixture selection, separate Appium Component Object/test, two independent native captures and preservation of the approved article baseline. Implemented the QA sample extension (not an upstream production feature); prepared a review-only candidate. Native repeatability was verified; banner baseline approval remains a human decision. No new baseline was automatically approved, and no CI or iOS execution is claimed.


### EXEC-026: Approved breaking-news golden promotion
Human explicitly approved the exact reviewed breaking-news candidate and requested byte-for-byte promotion, two independent native comparisons, the existing article regression and unit/type checks. Both banner comparisons and the article regression passed with unchanged thresholds. No fixture, UI or runner changes, CI work, iOS execution, commit or publication occurred.


### EXEC-027 - Dark article candidate (2026-11-07)
Requested a development-only nonpersistent override through the real application theme,
with cold-launch isolation, exact scenario/effective-theme assertions, two native card
captures and existing two-scenario regression checks. Both approved goldens and
comparison thresholds were preserved. Two dark captures matched exactly; candidate
awaits explicit human approval. No new golden, CI/iOS execution or commit was created.


### EXEC-028 - Dark article baseline approval and verification (2026-11-07)
The human approved only the exact reviewed dark PNG. Requested byte-for-byte
promotion after source/hash/session checks, independent dark regressions, light
scenario regressions and a subsequent dark launch, unchanged thresholds and
fixtures, plus type/unit checks and documentation. No new scenario, automatic
baseline regeneration, CI/iOS implementation, commit or publication was authorized.

Verified result: all five authorized native runs passed with zero changed pixels;
dark captures were byte-identical. All three approved hashes remained correct.
TypeScript, focused/broad Jest and Python units/collection passed. The existing
FIXTUR spelling-only combined-check failure remains. No implementation changes.


### EXEC-029 - No-image article candidate (2026-11-07)
Requested a development-only `no_image` scenario using the real article teaser with
genuinely absent featured media (not a broken URL), text-layout readiness independent of
image loading, no general production optional-media change, Appium image-absence checks,
two native captures, the three existing regressions and a human review packet, without
promoting a golden or committing.

Verified result: two independent cold-launch captures were byte-identical; candidate
awaits explicit human approval. The three existing references passed with zero changed
pixels. TypeScript, focused/broad Jest and Python units/collection passed; the existing
FIXTUR spelling-only combined-check failure remains.

### EXEC-030 - No-image baseline approval and verification (2026-11-07)
The human approved only the exact reviewed `no_image` PNG/hash after checking the image
and its full-screen context (the element screenshot intentionally excludes feed margins).
Requested byte-for-byte promotion after provenance checks, two independent `no_image`
regressions, the three existing regressions, unchanged thresholds/fixtures/rendering,
type/unit checks and documentation. No `empty_feed`, CI/iOS work, commit or publication.

Verified result: all five native runs passed with zero changed pixels; the two `no_image`
actuals were byte-identical. All four approved hashes were correct. TypeScript,
focused/broad Jest and Python units/collection passed; the existing FIXTUR
spelling-only combined-check failure remains.

### EXEC-031 - Successful empty-feed candidate (2026-11-07)
Requested a development-only `empty_feed` scenario where one configured synthetic feed
source resolves successfully with zero articles (explicitly not offline, error, loading or
zero-configured-feeds coverage). The request also asked for a minimal signal that tells a
successful empty response apart from fetch errors that the existing utilities convert to
an empty list, rendering through the real feed empty state, scenario-specific readiness,
populated/empty/populated cold-launch isolation checks, two native captures, the four
existing regressions and a human review packet, without promoting a golden or committing.

Verified result: both empty-feed captures were byte-identical. Populated runs before and
after them passed, and no stale content appeared in the empty runs. The candidate awaits
explicit human approval. All four approved references passed unchanged. TypeScript,
focused and full Jest, and Python units and collection passed. The existing FIXTUR
spelling-only failure in the combined check remains.

### EXEC-032 - Empty-feed baseline approval and five-scenario verification (2026-11-07)
The human approved only the exact reviewed `empty_feed` PNG and hash, together with its
message-only capture boundary, after reviewing the image and its full-screen context.
Requested:
- byte-for-byte promotion after provenance checks
- two independent `empty_feed` regressions
- the four existing regressions in one cold-launch sequence
- unchanged thresholds, fixtures and rendering
- type and unit checks
- documentation, including a fix for stale commit-status wording
No commit, CI or iOS work.

Verified result: all six native runs passed with zero changed pixels, and the two
`empty_feed` actuals were byte-identical. All five approved hashes were correct.
TypeScript, focused and full Jest, and Python units and collection passed. The existing
FIXTUR spelling-only failure in the combined check remains.

### EXEC-033 - Marker-controlled intentional visual failure demonstration (2026-11-07)
Requested a permanent, explicitly selected pytest demonstration that genuinely fails
because a real `breaking_news` capture differs from a deliberately incorrect reference.
Requirements:
- a dedicated `intentional_failure` marker, excluded by default
- no `xfail`, `skip` or inverted assertion
- a deterministic channel-swapped reference outside `baselines/`
- reuse of the existing launcher, page object, capture and comparator
No app, golden, threshold, CI or iOS changes, and no commit.

Verified result: collection by default, `-m visual` and `-m unit` excluded the
demonstration, and `-m intentional_failure` selected exactly one test. `breaking_news`
PASS (0 changed pixels), then the demonstration FAILED at the comparison assertion (exit 1,
468,349 of 506,804 pixels changed, 92.41%) with actual, diff and JSON artifacts, then
`breaking_news` PASS. All five normal scenarios then passed with zero changed pixels, and
all approved hashes were unchanged. This is a reference-mismatch demonstration, not an
application regression.

### EXEC-034 - Final strategy documentation reconciliation (2026-11-07)
Requested: update the Android/iOS strategy Markdown and PDF so they describe the
five-scenario Android demonstration and the intentional mismatch demonstration
accurately, keep the 1-3 page scope and cross-platform recommendations, state
limitations honestly, and correct only essential README contradictions. Documentation
only; no app, test, fixture, threshold, golden, CI or iOS changes; no commit.

Verified result: `deliverables/strategy.md` was restructured into nine concise sections
(recommendation, demonstrated Android architecture with a five-scenario table, verified
local evidence, reuse boundaries, production data seams, golden governance, proposed
CI/Scrum, flakiness and rollout, limitations). A link to an ignored execution record
was removed. The PDF was regenerated from the Markdown with the previously used
ReportLab approach: 2 A4 pages, both rendered and visually inspected, with no clipping
or private content. The READMEs now state that Git-ignored run artifacts are absent
from a fresh clone.

### EXEC-035 - Self-contained pytest scenario launching (2026-11-07)
Requested: make the normal Android visual tests runnable directly, including from
PyCharm's normal pytest Run action, without an externally set per-scenario
`VVP_QA_LAUNCH_URL`. Each test declares its scenario. A conflicting override must fail
clearly. The intentional-failure demonstration keeps its own marker. No app, fixture,
golden, threshold, CI or iOS changes; no commit.

Implemented: a registered `qa_scenario(id)` marker, a `qa_scenario` fixture in a root
`conftest.py`, and `build_launch_url`/`resolve_launch_url` in the existing launcher.
`make_driver(scenario)` uses these to cold-launch the declared scenario through the
existing development-client deep link. Optional `VVP_METRO_HOST`/`VVP_METRO_PORT`
overrides are supported, and a mismatching `VVP_QA_LAUNCH_URL` is rejected.

Verified result, with `VVP_QA_LAUNCH_URL` unset:
- Each of the five visual files passed individually with 0 changed pixels.
- `-m visual`: 5 passed.
- The default run: 46 passed, with the demonstration deselected.
- `-m intentional_failure`: failed as designed (exit 1, 468,349 / 506,804).
- A stale override failed immediately.
- Unit tests: 41 passed.
- Golden and demo hashes are unchanged.
- One strategy sentence was updated and the 2-page PDF regenerated and inspected.

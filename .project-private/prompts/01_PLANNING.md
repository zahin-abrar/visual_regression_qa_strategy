# Phase 1 — PLANNING: SUT and mocking first

Read the employer PDF and project source-of-truth docs. **Our first planning decision is SUT FINALIZATION AND MOCK-DATA STRATEGY**; do not open with generic tooling brainstorming. No framework is approved yet.

## Step 1: Narrow SUT feasibility

Compare only **JetNews** and **Volksverpetzer `vvp_app`** as main candidates, with tiny owned news sample as fallback; study **Now in Android** only as architecture reference. Review their actual repositories/README/license as needed. Locate concrete feed/article component, its data source, setup/runtime needs, and stable selectors. Identify unverified assumptions and what can be checked in a short (<60–90-minute) feasibility spike on the available machine. Reject candidates if running UI, mocking or licensing cannot be made credible quickly. Use `docs/05_SUT_SELECTION.md`.

## Step 2: Decide data-injection seam together with SUT

For each viable SUT, evaluate **test-only fixture repository/build mode** versus **local mocked API**; proxy interception only if unavoidable. Show exact application boundary where fixed headlines, timestamps, images, premium flag, and error state would enter *real UI*; explain scenario-selection/reset and how to prevent live content leakage. Appium can't mock by itself. Use `docs/06_MOCKING_STRATEGY.md`.

## Step 3: Select minimum runner and scale path

Only after mock feasibility, compare **Appium + Python/pytest + platform-specific drivers/baselines** against **native component snapshots**; explain trade-offs and likely production hybrid. Propose pinned Android environment, real goldens/diff, PR CI workflow, artifacts and separate written iOS path. CI scalability must prioritize fast feedback and avoid a full device matrix per PR. Use `docs/07_ARCHITECTURE_CI.md`.

## Decision / exit output

Give a compact table with up to three realistic choices, recommend SUT+mock+runner and fallback, call out high-risk prerequisites, and define **one end-to-end fixture→real UI→PNG→golden→diff** acceptance slice. Ask for explicit human approval **once** before implementing; record approved ADRs in `docs/02_DECISIONS.md` and update `docs/03_HANDOFF.md`. Log substantial AI prompts. No implementation unless a bounded feasibility experiment is explicitly authorized; don't burn deadline in planning theater.

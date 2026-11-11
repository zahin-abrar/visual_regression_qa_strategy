# Phase 2 — EXECUTION (only after planning approval)

Read the original PDF, approved ADRs, handoff and SUT/mocking strategy. Implement **one narrow native mobile vertical slice** in the approved SUT: deterministic scenario selection → actual UI rendering → screenshot PNG → committed platform-specific golden → automated comparison. Use Appium+pytest only if it was approved; a native snapshot route is equally valid. Validate local run, fixture-to-view evidence and golden diff; add an intentionally failing visual regression if feasible.

Build with CI in mind: test-only mock data (no live news dependency), pinned OS/emulator, fixed assets/fonts/time, stable UI-ready checks, explicit diff reports and human baseline approval. Implement a CI job if feasible, but distinguish actual passing runs from proposed workflow configuration. iOS strategy must be concrete even if iOS tests aren't run. The production architecture may include hybrid component snapshots + Appium, but do **not** build unapproved scope.

Write the 1–3-page strategy, runnable README, baseline update instructions and prompts-used record. Record commands, successes, failures and evidence paths; update handoff after each work unit. Use short Tier A approval only for a material pivot. Move to EVALUATION only when evidenced or when human accepts explicitly documented limitations.

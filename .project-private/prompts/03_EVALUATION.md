# Phase 3 — EVALUATION: interviewer's strict evidence audit

Read employer PDF, approved decisions, handoff, actual source, fixtures, goldens, CI and run logs. Judge the submission as an Axel Springer Senior QA Manager interviewer:

1. Does a fixed fixture **really replace live data inside the real UI**? Can an evaluator reproduce it, repeat the screenshot and inspect a real comparison/diff?
2. Does the strategy cover Android and iOS honestly, platform-specific differences included? No claims of unrun iOS coverage.
3. Are goldens source-controlled, baseline updates reviewed, failure artifacts usable, and CI assertions truthful? Check actual green CI runs instead of treating YAML as proof.
4. Does the proposed design improve QA feedback time under frequent AI-assisted builds **without excessive per-PR device cost or flaky full-matrix tests**? Is shared vs platform-specific code pragmatic?
5. Does hand-in include 1–3-page strategy, demo, README commands, golden images, prompts-used log and optional regression/diff?

Report P0/P1/P2 findings with brief fix cost/interview impact. Fix blocking issues first; disclose others. Reproduce from clean instructions where feasible. Rehearse a clear 3–5-minute narrative: QA bottleneck → tool/mocking tradeoffs → running fixture/diff → scaled CI rollout. Update handoff, evidence links and final package inventory.

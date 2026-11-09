# AI assistance disclosure (material prompts)

**Status: DRAFT prepared from the project's own prompt log for the author's review.** The author must verify it against all AI conversations and complete or correct it before submission. It is a summary, not verbatim transcripts, and it contains no private brief, employer material or secrets.

## Tools

- **ChatGPT** (conversation label recorded as GPT-6 where noted): planning, option comparison, architecture and strategy drafting, interpretation of results.
- **Claude Code** (Anthropic; model labels varied across sessions and are not all recorded): implementation, local verification, CI authoring and troubleshooting, documentation, executed against the repository under the author's direction.

All AI-produced code and text was reviewed by the author. Golden images were captured from a real emulator and approved by a human; no AI tool approved or regenerated a reference. Claims in the README and strategy are limited to what was actually executed.

## Material prompts by phase

| Phase | Representative request (paraphrased) | Output used | Human check |
| --- | --- | --- | --- |
| Planning | Appraise open-source apps as a screenshot-testing system under test; compare candidates (JetNews, Volksverpetzer and others). | Shortlist and feasibility-first evaluation. | Licence and build feasibility checked by running the chosen app. |
| Planning | Clarify what "mocked data" means and whether source access is needed. | Real UI with fixed fixtures; fixtures at an app-level seam, not a mocked server. | Compared with the challenge text. |
| Planning | Assess an Appium/Python approach for shared Android/iOS tests and CI scalability. | Shared scenarios with thin platform adapters; Appium treated as driver, not mock engine. | Design only until executed. |
| Planning | Check the challenge's local-emulator versus cloud wording. | Local emulator accepted; cloud optional. | Re-read the original brief. |
| Execution | Build a bounded fixture-provider spike in the adapted app (synthetic article, image, text). | Development-only fixture seam feeding the real feed UI. | Rendered on a real emulator; code reviewed. |
| Execution | Select scenarios at launch (deep link `qa_scenario`), verify an identity marker. | Cold-launch scenario selection and marker check. | Repeated launches. |
| Execution | Implement capture, Pillow comparison, diff artifacts, page objects and unit tests. | `qa_visual/` runner and 100+ unit tests. | Tests run locally; thresholds unchanged. |
| Execution | Add four further scenarios (`breaking_news`, `dark_article`, `no_image`, `empty_feed`) and golden promotion steps. | Scenario fixtures and tests; goldens promoted byte for byte after human approval. | Human review of each candidate image. |
| Execution | Add an intentional visual mismatch demonstration. | Marker-controlled failing test with actual/diff/JSON output. | Confirmed genuine assertion failure. |
| Execution | Add Allure reporting and failure-evidence retention. | Allure results/report, attachments. | Generated and inspected locally. |
| CI | Create GitHub Actions: debug-APK build workflow; separate manual visual workflow that reuses an APK with provenance checks. | Two `workflow_dispatch` workflows and helper scripts. | Run on GitHub; each failure was analysed from logs. |
| CI troubleshooting | Diagnose runner disk, KVM, AVD creation/path, ADB authentication and emulator stability. | Series of small script fixes and a post-boot health gate. | Verified from hosted-run logs. |
| Debugging | Add launch-failure diagnostics, dismiss the Expo developer-menu overlay, add single-scenario scope. | Diagnostics, overlay handler, `visual_scope` input. | Real emulator reproduction of the overlay; GitHub runs inspected. |
| Evaluation | Audit deliverables against the challenge, update strategy/README to the verified evidence, draft interview notes. | Final documentation. | Author review. |

## Notes

- A native `SIGSEGV` in the `no_image` scenario on the hosted emulator was investigated with AI assistance for diagnosis only; its cause remains unresolved and is disclosed in the README and strategy.
- The author is responsible for the final submission and should add any prompts from conversations not captured here.

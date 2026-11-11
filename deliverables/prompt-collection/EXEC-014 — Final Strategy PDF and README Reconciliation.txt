# EXEC-014 — Final Strategy PDF and README Reconciliation

**Project:** `D:\Projects\visual_regression_qa_strategy`  
**Previous task:** EXEC-013 — PASS, with one PDF formatting issue identified during human review.

## Objective

Resolve two final documentation inconsistencies without changing the approved strategy or working demo.

## Required changes

1. **Fix links in the strategy PDF.**
   - The final section currently renders Markdown link syntax literally, for example `[runner guide](../qa_visual/README.md)`.
   - Replace these with clean reference labels or properly rendered hyperlinks.
   - Do not leave raw Markdown link syntax visible in the PDF.
   - Preserve the technical content and seven-section organization.

2. **Update the root README.**
   - Replace the statement that the cross-platform strategy is pending.
   - Add a working relative link to `deliverables/strategy.pdf`.
   - Optionally link the editable `deliverables/strategy.md`.
   - Leave the rest of the README unchanged unless correcting an obvious broken link or working-directory assumption.

3. **Regenerate and verify the PDF.**
   - Keep the PDF at `deliverables/strategy.pdf`.
   - Confirm it remains 1–3 A4 pages.
   - Render and inspect every page for readability, clipping, overflow and link formatting.
   - Confirm all seven strategy sections and verified Android metrics remain present.
   - Ensure the revised PDF and Markdown source remain consistent.

## Boundaries

- No changes to app source, automation, fixtures, goldens, comparator or thresholds.
- No emulator/Appium operations.
- No CI implementation.
- No Git initialization or publication.
- No new strategy sections or significant content changes.
- No additional document-generation tool installation unless genuinely necessary.

## Recordkeeping

Append EXEC-014 to `docs/AGENT_TASK_HISTORY.md` with changed files, PDF page count, verification steps and outcomes. Update the local handoff if appropriate.

## Completion report

Return:

1. PASS / FAIL / BLOCKED.
2. Files changed.
3. PDF page count.
4. Link-formatting verification.
5. Root README link verification.
6. Remaining submission blockers.

**Stop after EXEC-014. Do not proceed to Git packaging without authorization.**
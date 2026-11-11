# AI assistance and prompt register

Employer PDF p.3 requires **which prompts were used**. Log substantive requests as development happens, include tool/model labels where known, and export a cleaned `deliverables/ai_prompts_used.md` for submission. Include project instructions/agent prompts used. Do not invent unavailable exact prompts, tool outputs or testing evidence. Omit private/unrelated application details.

## AI-000 — Initial project scaffold

- **Date:** 2026-11-01; **Phase:** PLANNING; **Tool/model:** ChatGPT (model label verify in chat UI as needed).
- **Prompt:** Earlier project-setup request asking for Planning/Execution/Evaluation phases, human-reviewed options and trade-offs, and lightweight spec-driven agent handoffs (full verbatim text was not reproduced in this file; consult original chat if needed for exact disclosure).
- **Output:** Initial scaffold docs, phase prompts, consolidated project context and ZIP.
- **Human check:** User identified and found project instructions; architecture decisions remained open.

## AI-001 — Evaluate an open-source SUT

- **Date:** 2026-11-01; **Phase:** PLANNING; **Tool:** ChatGPT.
- **User prompt (verbatim):** "Before moving to new project I'd like to know about your appraisal of this project for the screenshot testing SUT: [https://github.com/Volksverpetzer](https://github.com/Volksverpetzer)"
- **Follow-up prompt (verbatim):** "what would you recommend to look into for candidate SUTs?"
- **Output used in planning:** Candidate shortlists (JetNews, Volksverpetzer, Now in Android reference, KMP sample), feasibility-first evaluation.
- **Human/technical verification:** No local SUT run or licensing review yet.

## AI-002 — Clarify mocking and codebase access

- **Date:** 2026-11-01; **Phase:** PLANNING; **Tool:** ChatGPT.
- **User prompt (verbatim):** "i am not sure about the mocking aspect. Does the task expect me to update the news app content with a mock data rather than what the app shows from its server?"
- **Follow-up prompt (verbatim):** "So we need the access to the codebase of whatever sut we decide to use?"
- **Output used:** Real UI plus fixed fixtures, source access helpful but black-box possible; no need to modify real news server.
- **Verification:** Compared with employer PDF p.3 mock examples and p.4 sample-app permission.

## AI-003 — Appium cross-platform architecture

- **Date:** 2026-11-01; **Phase:** PLANNING; **Tool:** ChatGPT.
- **User prompt (verbatim):** "I was thinking of using a framework like appium and use that to drive the app and take screenshots to make overall testing code ios or android platform independent"
- **Follow-up prompt (verbatim):** "In that approach, how do we inject mock data to sut? From the assignment doc, mock injection seemed a big part"
- **Output used:** Shared Appium/pytest scenarios, thin native drivers, platform-specific baselines, injection via fixture repository or mock API; never treat Appium as a mock engine.
- **Verification:** Design only, no Appium run.

## AI-004 — CI/CD scalability and interviewer-reported delivery problem

- **Date:** 2026-11-01; **Phase:** PLANNING; **Tool:** ChatGPT.
- **User prompt (verbatim):** "Would this approach ne ci cs friendly and scalable? Those are also requirements for the challenge"
- **Next user prompt (verbatim):** "From my first interview, i remember the interviewers said that they are facing a problem where builds are coming way faster because of ai assisted development approaches but qa is not that benifitted (because at the end of the day tester needs to test the application) and qa team is under pressure to veryfy these frequent builds. So my goal is to make as many ci cd friendly, scalable platform independent codebase so that test team has less selarate code bases to maintain. This would help the team save time. But it should not be too difficult to make it completely platform independent. We can evaluate the ios/android specific code where it's efficient (for example, may be the mocking part)"
- **Output used:** Shared-core/platform-adapter design, risk-based PR vs nightly suites, hybrid option, explicit CI metrics and limitations.
- **Verification:** The interview statement is **user-reported**, not sourced from the PDF; no measured efficiency savings exist.

## AI-005 — Verify PDF's local/cloud alternative

- **Date:** 2026-11-01; **Phase:** PLANNING; **Tool:** ChatGPT.
- **User prompt (verbatim):** "The source pdf says something about cloud or local screenshot (most likely in the second last page). Could you please check and confirm if their expectation matches the approach we are leaning towards?"
- **Output used:** Verified PDF p.3 explicitly accepts Appium/Maestro driving emulators/simulators or device cloud; mock server or test-only fixture swapping; choice must be fast and stable. Cloud not obligatory.
- **Verification:** Re-read original supplied PDF; not a claim that any cloud service has been tested.

## AI-006 — Refresh project starter after discussion

- **Date:** 2026-11-01; **Phase:** PLANNING; **Tool:** ChatGPT (GPT-6).
- **User prompt (verbatim):** "since we have discussed about some useful aspects after the project files were created, please go through our latest conversation after the project file generation and modify/add necessary files for the project. For the planning phase, I'd like to start with SUT finalization and mocking strategy as part of planning phase."
- **Output:** Revised requirements, decisions, handoff, first/project/phase prompts; new SUT, mock, CI architecture planning documents; updated consolidated context and ZIP.
- **Human validation:** User review pending; no SUT, Appium, or CI execution yet.

## Future entry template

```text
### AI-NNN — [short purpose]
- Date/time, phase, model/tool:
- Exact user prompt or stable versioned prompt file:
- Output and changed files:
- Human review/verification and commands:
- Caveats or corrections:
```


---

## AI-007 — Reassess JetNews vs vvp_app and first SUT/mock gate

- **Date:** 2026-11-01; **Phase:** PLANNING; **Tool/model:** ChatGPT (GPT-6), public GitHub/Android/Appium documentation via web lookup.
- **Current user prompt (verbatim):**

> We are continuing the Axel Springer Tech Senior QA Manager take-home challenge; the live interview/demo is **Tuesday 3 November 2026 at 14:00 CET**.
> 
> Read the original four-page employer PDF (QA_Manager_Challenge_Screenshot_Testing.pdf) and the updated project context and source-of-truth documents uploaded to this ChatGPT Project:
> 
> 01_REQUIREMENTS.md
> 
> 02_DECISIONS.md
> 
> 03_HANDOFF.md
> 
> 05_SUT_SELECTION.md
> 
> 06_MOCKING_STRATEGY.md
> 
> 07_ARCHITECTURE_CI.md
> 
> Use 01_PLANNING.md as the phase-specific guidance.
> 
> All documents are uploaded directly to the ChatGPT Project's Sources section without directory structures. Identify files by filename, ignoring any docs/ or prompts/ prefixes in older references.
> 
> We are currently in the PLANNING phase. Begin with SUT evaluation and finalization, followed by deterministic mock-data injection strategy. Evaluate the feasibility of these choices before finalizing the automation framework.
> 
> Our architectural objective is to reduce QA verification bottlenecks caused by increasingly frequent AI-assisted builds through CI/CD-friendly, scalable, maintainable automation. Prioritize shared cross-platform test logic while allowing lightweight Android/iOS-specific implementations where they are more practical.
> 
> Do not prematurely commit to Appium, a particular SUT, or a mocking mechanism. Present meaningful alternatives, trade-offs, recommendations, and decisions requiring human approval. Do not begin implementation until the major planning decisions are approved.
> 
> **We are in PLANNING, and our first work is SUT finalization together with mock-data injection.** The shortlist is **JetNews versus Volksverpetzer `vvp_app`**, with an owned sample news app as fallback; Now in Android is a reference. Appium + Python/pytest is my leading cross-platform automation idea, **not yet locked**.
> 
> Important context from my first interview: AI-assisted development increases build frequency and pressures QA to verify more builds. My objective is fast, CI/CD-friendly visual regression feedback and one practical shared test codebase for Android/iOS, while allowing efficient platform-specific adapters (especially data injection, drivers and golden images). Avoid pursuing 100% platform independence at the expense of reliability.
> 
> Please begin by comparing the SUT candidates specifically for **source/build feasibility, deterministic fixture injection into real UI, stable screens/selectors, reuse rights, and time to first screenshot**. Propose a short feasibility spike and an explicit **SUT + mocking** decision; then assess the screenshot runner and CI path in that light. Highlight unknown environment prerequisites rather than assuming anything already runs. Use 2–3 options maximum per major decision. Do **not** start implementation or silently approve Appium. Keep the docs and AI prompt log updated, and distinguish what is verified from what is proposed.

- **Output:** Online read-only comparison of JetNews and Volksverpetzer `vvp_app`; confirmed JetNews existing `PostsRepository` / `FakePostsRepository` and real `HomeScreens.kt` card consumers. Found 800 ms artificial delay, every-fifth-request failure; `vvp_app` build instructions/source existence but unresolved article API seam. Proposed coupled JetNews + test-only fixture repository, conditional Appium runner or native snapshot fallback, ~90-minute feasibility gate, CI risk controls.
- **Documents prepared (complete revised copies):** `02_DECISIONS.md`, `03_HANDOFF.md`, `04_AI_PROMPT_LOG.md`, `05_SUT_SELECTION.md`, `06_MOCKING_STRATEGY.md`, `07_ARCHITECTURE_CI.md`. The user must replace corresponding existing Project Sources; files generated here do not automatically overwrite uploaded Project Sources.
- **Independent verification:** Public source pages and official docs inspected, no candidate's Windows host/build/emulator or fixture-to-UI test. Attempted GitHub `git ls-remote` in assistant sandbox failed DNS resolution; this says nothing about user's machine. No implementation, test passes, golden images, or CI evidence.
- **Human status:** Bounded feasibility spike approval requested; SUT/mock/runner decision and implementation authorization PENDING.
- **Disclose caveat:** Any researched source paths and versions are branch-relative and must be pinned/verified on local checkout; `vvp_app` asset rights and article API injection not proven.

---

## AI-008 — Authorize `vvp_app`-first feasibility spike

- **Date:** 2026-11-01; **Phase:** PLANNING; **Tool/model:** ChatGPT (GPT-6).
- **User prompt (verbatim):** "Prioritize vvp_app in the bounded SUT/mock feasibility spike. Keep implementation and runner decisions open."
- **Task:** Change candidate inspection order to Volksverpetzer first; inspect public build/data seam evidence; keep architecture open; update decisions, handoff and prompt log without implementation.
- **Research performed:** Public Volksverpetzer GitHub README and root; public F-Droid app listing; official Maestro React Native `testID`, screenshot and assertion docs. Attempted to access GitHub source tree/files but web cache misses; attempted assistant-sandbox `git ls-remote` and saw DNS failure. No claim of local Windows verification.
- **Output:** Complete revised `02_DECISIONS.md`, `03_HANDOFF.md`, `04_AI_PROMPT_LOG.md`, `05_SUT_SELECTION.md`, `06_MOCKING_STRATEGY.md` and `07_ARCHITECTURE_CI.md`; a bounded host-side source/build diagnostic checklist. JetNews-first previous recommendation explicitly superseded by human inspection priority.
- **Verification:** No checkout, app build, mock, screenshot, golden, regression diff, CI, native iOS test or Appium/Maestro run. Material next step requires actual `vvp_app` files/build result from the candidate's Windows machine.

**Delivery note:** Include the substantive planning prompts in the cleaned employer-facing prompts record, omitting unrelated personal/project context. AI assistance outputs remain subject to human validation.


---

## AI-009 — Interpret actual `vvp_app` Windows feasibility output

- **Date:** 2026-11-01; **Phase:** PLANNING; **Tool/model:** ChatGPT (GPT-6).
- **User input:** PowerShell command/output transcript of `git clone --branch prerelease --single-branch https://github.com/Volksverpetzer/vvp_app.git`, `git rev-parse HEAD`, `node --version`, `pnpm --version` (initially missing), `npm install -g pnpm`, `pnpm --version`, `adb devices -l` and `emulator.exe -list-avds`. The full verbatim transcript is in the originating chat; this entry summarizes the lengthy console output rather than claiming a verbatim prompt.
- **Observed host results:** source cloned, HEAD `8b421753a17a18cd648447319adcca61a288f97f`, Node `v22.12.0`, pnpm `12.11.2` after npm global install, empty ADB device list, configured `Pixel_10` AVD.
- **Assistant output:** distinguished checkout/AVD existence from a successful build; identified Node below repo README 24+ minimum; proposed read-only source trace and project metadata inspection before package installation or framework selection; prepared revised decision/handoff/SUT/AI log files.
- **Verification limits:** User supplied actual command outputs. AI did not execute the commands on user's PC. No traced source files from checkout, app build, fixture injection, Android UI render, screenshot, visual golden/diff, runner, CI or iOS testing verified. No architecture decision or implementation approval inferred.


---

## AI-010 — Inspect exact `vvp_app` archive and host build prerequisites

- **Date:** 2026-11-01; **Phase:** PLANNING; **Tool/model:** ChatGPT GPT-6; Python/container for private read-only archive inspection; official React Native and Expo web docs for JDK/local build compatibility.
- **User input:** User provided a verbatim PowerShell transcript confirming clean checkout, `.nvmrc=24`, `packageManager=pnpm@12.11.2`, Node engine `24.x`, pnpm lockfile pin, `.env.sample` present, `JAVA_HOME` JDK11, `ANDROID_HOME` path, and `git archive ... HEAD`; uploaded `vvp_app_prerelease_8b42175_source.zip`. Original complete transcript and archive are in this project conversation, not recopied into this record.
- **Task/request inferred from current project workflow:** Continue authorized read-only `vvp_app` feasibility, identify actual native screen/data seam, assess fixture-provider vs mock HTTP, keep Appium/Maestro and implementation unapproved; update source-of-truth/handoff.
- **AI analysis / output:** Inspected archive; traced `HomeScreen → FeedFetcher → WordPressFetcher → WordPressAPI → Feed → GenericPost → ArticlePost`; identified custom WordPress feed client separate from FOSS-only app-server URL override; discovered additional media metadata request, dynamic engagement/announcements and existing non-unique `article-progress-bar` testID. Confirmed root MIT license and code version pins. Recommended a debug-only fixture fetcher conditioned on successful Android build; runner undecided.
- **Human/technical verification:** PowerShell outputs supplied by human; archived source inspected directly by AI. **No build, native UI, fixture injection, screenshot golden, diff, CI, or iOS verified.** AI did not execute commands on human's Windows machine. New proposed injection/fixture logic is not implemented or approved.
- **Document delivery:** Complete revised `02_DECISIONS.md`, `03_HANDOFF.md`, `04_AI_PROMPT_LOG.md`, `05_SUT_SELECTION.md`, `06_MOCKING_STRATEGY.md`, `07_ARCHITECTURE_CI.md` generated as replacements, subject to manual Project Sources update.

---

## AI-011 — Prepare bounded `vvp_app` home-feed synthetic fixture patch

- **Date:** 2026-11-01; **Phase:** PLANNING feasibility experiment; **Tool/model:** ChatGPT GPT-6 + local container Python/Node/Git for source transformation and static checks.
- **User approval (verbatim):** "I have reviewed the approach. We can proceed." This directly followed a recommendation to test a development-only injected article fixture with unrelated social feeds disabled. No SUT/runner/CI final architecture authorization inferred.
- **Additional user evidence:** actual native Volksverpetzer home/article feed visible on Pixel_10; Metro startup successful; `/proxy/instaFeed?account=pruefpunkt` returned HTTP 502 and displayed an app-level debug toast; cold boot resolved Android Package Manager responsiveness.
- **AI task:** Create the smallest **explicitly opted-in** synthetic one-article home-feed fixture passing through the actual WordPress article mapper, real Feed/GenericPost/ArticlePost components; bundle a static original image; suppress unrelated social feed fetchers, announcement/permission/changelog, view counter and progress in the test scenario; do not choose Appium/Maestro yet.
- **Output:** `vvp_qa_fixture.patch` (binary Git patch); original static PNG; exact Windows apply/run/rollback README; updated decision, handoff and mock docs. Runtime scenario: `__DEV__ && EXPO_PUBLIC_QA_SCENARIO === 'long_headline'`. Synthetic long headline/author/date, deterministic media and `testID` markers. Existing normal feed path remains in source.
- **Independent verification:** unpacked pinned archived source SHA `8b421753a17a18cd648447319adcca61a288f97f`; patch applied cleanly with `git apply --check` and `git apply` against a fresh copy; generated PNG hash matched; edited/new TS/TSX files passed TypeScript syntax/transpilation using locally installed `typescript` API. **Not tested:** app-specific dependency-linked TypeScript check, Windows Metro bundling, fixture card on Android/iOS, external-network exclusion across entire app, test runner, screenshot/golden/diff or CI.
- **Critical limitation:** Changes were prepared in the assistant sandbox, not automatically installed into the user's Windows clone. Their on-device verification is necessary before claiming mocking feasibility or approving the final architecture.


## EXEC-020 - 2026-11-07T12:45:56+01:00 - Runtime selection foundation
Human authorized Option B: development-only immutable cold-launch selection for a typed five-ID registry, only long_headline supported; preserve fallback, real fixture pipeline, golden, production safety, and unrelated work. Requested selection-before-feed, exact nonvisual identity, validation/isolation tests, candidate Windows launch lifecycle and honest native evidence.
Agent inspected current root/Router/native/dev-client/driver paths, implemented the bounded gate/registry/opt-in launch helper and tests, documented the unverified wrapper procedure, and updated private decisions/handoff. No private brief content copied into tracked files. Broad app tests passed before final route adjustment; final targeted 36 tests, TypeScript and 12 Python unit tests passed. Existing cspell FIXTUR issue remains. Runtime BLOCKED: no ADB device; Metro/Appium unavailable. No screenshot, native regression, release build, CI, install, commit or push claimed. Approved golden unchanged. Await runtime verification authorization; no new scenario UI implemented.


## EXEC-021 - 2026-11-07T13:18:45+01:00 - Native runtime verification
Human authorized preserving restored IPv4 Metro while verifying cold runtime selection, two original visual executions, negative launches and bounded startup/identity remediation. No scenario UI, fixture/golden/threshold change or publication authorized.
Agent independently verified IPv4 status/project manifest, online API37 Pixel_10, existing reverse and installed app; started Appium3.3.0/UiAutomator2 7.1.2 without changing Metro. Fixed only the QA marker's inaccessible top-edge placement (top64dp,zIndex1). Exact identity/readiness and unknown/unsupported/none/fallback native launches verified. Temporary probe ID lookup corrected, with original failure evidence preserved. Two native screenshots are byte-identical to each other but each FAIL approved golden by11640pixels/0.915356%, localized to synthetic image; no repair or new baseline attempted. Broad app1438passed3skipped, focused36passed, Python12passed, collection13, TypeScript exit0; known FIXTUR cspell failure persists. Private handoff contains commands/artifacts/limitations. EXEC-021 FAIL; EXEC-020 acceptance open. Recommend bounded image-region baseline-compatibility investigation before expansion. No employer/private brief copied into public files; no commits/pushes.


## EXEC-022 - 2026-11-07T13:32:33+01:00 - Image mismatch investigation
Human authorized direct artifact/pipeline/environment analysis, runtime-vs-fallback native captures, bounded verified corrections and two post-correction visual runs, with unchanged golden/content/thresholds and stop if unresolved. Agent measured edge-localized526-vs527 image geometry, verified source+Metro asset SHA and unchanged APK/display; runtime path failed while one fallback exactly matched golden. Investigated only QA native-intent route handling. Root redirect candidate failed; wrapper-preserving candidate passed once then failed with1238px card height on independent launch. Tentative sole-route-root-cause hypothesis was rejected; BOTH source/test files restored to pre-task contents. No accepted fix or obsolete-golden claim. Artifacts and full attempted-result record preserved in ignored directories. Final TypeScript and36focused Jest tests pass; baseline unchanged; services preserved. EXEC-022 BLOCKED pending controlled layout telemetry; no new scenario, baseline, dependency, commit or push.


## EXEC-023 - 2026-11-07T13:45:23.810737+01:00
Material prompt: authorized development-only layout/event telemetry, alternating runtime/fallback independent captures, bounded evidence-driven correction only; preserve golden/content/thresholds and remove probes afterward. No new scenarios/CI/commits.
Outcome: BLOCKED runtime visual acceptance. Three fallback captures byte-identical approved golden; three runtime captures byte-identical to each other but11640changed(0.915356%). Image onLayout527vs526px BEFORE load/readiness; fallback container1238->1237px during navigation, runtime1237 stable. Same desired image size/source/window/insets; exact native rounding/initialization cause unresolved. No speculative correction. All11 instrumented source files byte-restored/helper removed. Final original pytest runtimeFAIL(exit1),fallbackPASS(exit0); tsc0,Jest36passed,Python12passed. Golden unchanged. Retained ignored evidence/debug-logs and private handoff only; same Gitstatus/HEAD,no remote/push. Recommend fallback demonstration path/runtimeexperimental, await review before further work. Detailed commands/timelines/limitations in private handoff and ignored exec023 evidence. No proprietary brief copied.


## EXEC-024 Checkpoint 1 - 2026-11-07T14:00:59.387110+01:00
Material prompt: prepare exact verified runtime native capture as ignored baseline candidate,reviewpacket/provenance/metrics/quality assessment; current golden unchanged until separate humanreview and exact candidateapproval. No native runs or migration authorized in this invocation.
Outcome: packet debug-logs/exec024/review/,candidate1028x1237RGBA SHA256 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC,identical three independentEXEC023 runtimecaptures. Difference11640pixels/0.915356% vs currentgolden; image526vs527px; visual agentreview found no obvious substantive defects. Onepixel/channel1 uninstrumentedvariation disclosed. Proposed launchcontractmigration only; native roundingunresolved; baselineapproval/Checkpoint2 pending. Existinggoldenhashunchanged,Gitstatusunchanged,no source/UI/threshold/commit/push/servicechanges.


## EXEC-024 Checkpoint2 - 2026-11-07T14:25:05.223669+01:00
Materialprompt: human explicitly approves ONLY candidateSHA 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC; verifyoriginal/candidate/history,copyexactbytes,runoriginalruntimevisualtesttwice unchangedthresholds,checkrepeatability/unit/type,documentintentionalmigration andprivateapprovalrecords. Preserveexistingwork; no newscenario/commit/push.
OutcomePASS: targetgolden old E8D573E650E291D8FFDFD69DB9DD764ABB40C08B6FDA0F273E74365B1F6BF629 ->approved 6A9E18DAF9769686A9ADF4A3D7C85E9A09ED429FA17EDFB4ABE5880682C878CC; oldblobverifiedrecoverable atHEAD. Two independent coldlaunch pytest runs1passed/exit0 each,1028x1237,0changed; actualsbyteanddecodedidentical/candidateequal. Identity/readiness/title/outerbounds proven inAppiumlogs. tscPASS,Jest36PASS,Python12PASS; combinedcheckFAIL onlyexistingFIXTUR spelling. Root/runner/baselineREADMEs reconcileexplicitlaunch,newreferencecontract,humanreview,oldhistory,uncommittedstatus,fallbackwarning andunresolvednative rounding. No app/fixture/runner/comparatorlogicchanges; no thresholds/newgoldens/CI/iOS. Awaitreview beforebreaking_news.


## EXEC-025 - 2026-11-07T14:39:07.101213+01:00
Materialprompt: approvedbounded breaking_news QA-only realbanner/fixture/POM/test,2nativecoldcaptures/repeatability,candidatepacket,unchangedlonggoldenregression; noautogoldenapproval/newscenario/CI/commit.
Outcome: implementedmeasured-layoutstaticEILMELDUNG banneras sample-appchallengeextension,notauthenticupstreamfeature; existingimmutableselectorandarticlefixturepipeline retained. Nativebanner2captures1028x493,bounds26,720..1054,1213,byte-identicalSHA E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F,raw/policy0difference. Bothpytestexit1onlymissingbaseline. Candidateignoredreviewpath,pendinghumanreview. LongregressionPASSexit0,0changed,approvedSHAunchanged. FinaltscPASS,broadJest181suites1442passed3skipped,Python14unitPASS/16collected;combinedcspellonlyexistingFIXTURfailure. Initialtest-harnessfailurescorrectedandrecorded. No goldensource/comparator/productionlayout/CI/iOS/commit/push;privatehandoffhascommandsandlimits.


## EXEC-026 - 2026-11-07T14:56:26.851036+01:00
Material prompt: explicit human approval for exact breaking-news candidate E552AD4D89CC3684062E803B49550DFCDB868AEA0575BF890DA85D958438BE7F; verify identities/native provenance, promote exact bytes, run2coldbreaking comparisons and existinglong regression, type/unit checks and documentation; preserve source/layout/thresholds and all unrelated work, no commit/push.
Verified outcome PASS: breaking runs19.79s/15.92s,exit0each,1028x493,0changed; actuals/candidate byteidentical,raw/policy0difference. Long16.54s,exit0,1028x1237,0changed,approvedhashunchanged. tscPASS,Jest40PASS,Python14PASS; knownFIXTURcombinedcheckFAILonly. Baseline inventory/root/runner/prompt records updated with2approvedAndroidscenarios,humancontrolledreplacement,challenge-specificbanner andnoCI/iOSclaims. No application/runner changes; localgoldenaddition uncommitted. Full evidence in ignoredexec026artifacts and privatehandoff. Stop for review before nextscenario.


## EXEC-027 - 2026-11-07T15:14:23.006686+01:00
Material prompt: implement real dark_article through nonpersistent development-only theme override before article mount; preserve both exact approved references, use same synthetic article/assets and runtime coldlaunch; verify exact scenario/effective-theme/title/image/stablebounds, dark-light-dark isolation,2nativecaptures,existing2regressions,unit/type checks,ignoredreviewpacket; no golden promotion/CI/iOS/commit.
Verified: candidateSHA6FD667E87476F941F7CB7A8152F60FFB8C51A3FD4217A7E993300AB32EB62A96,1028x1237,raw/policy0difference,byteidentical;2pytestexit1onlymissinggolden. Long/breakingexit0,0changed,bothgoldenhashesunchanged. Persistedtheme system unchanged,hooktestscoveropposingpreferences/releasegate. tscPASS,Jest181suites1443PASS3skip,Python19PASS22collected; knownFIXTURcombinedcheckexit1. Wrong-cwd initialPythoncheck failedimports then corrected documented cwd. Fullnativeevidence/review in ignoredexec027paths. No fixture/layout/image/threshold changes. Humanreviewpending,stop.


## EXEC-028 - 2026-11-07T15:37:11.045622+01:00
Materialprompt: humanapprovedonlyexactdarkcandidatehash; verifynativeprovenance/existinggoldens,bytecopypromote,2independentdarkregressions,lightlong/breakingthemeisolation,optionalfinaldark,unit/typechecks,docs/privateapprovalrecords; preservefixtures/layout/thresholds/workingtree,noCI/iOS/newscenario/commit.
OutcomePASS: dark20.52s/17.21s,exit0,0changed;long18.37s/breaking18.47s,exit0,0changed;finaldark17.14s,exit0,0changed. Darkactualsbyteidentical;raw/policy0difference;all3hashescorrect. Actualthememarkersdark/light/light/dark;storedsystemunchanged. tscPASS,focused52PASS,broad181suites1443PASS3skip,Python19PASS22collected. KnownFIXTURcombinedcheckexit1separatelyrecorded. Noapplication/runner/thresholdchanges;newgoldenanddocumentationonly,HEADunchanged,nocommit/push. Fullcommands/evidenceprivatehandoff/ignoredexec028artifacts. Stopforreviewbeforeanother scenario.

## EXEC-029 - no_image (Claude Code, 2026-11-07)
Human prompt: implement approved QA-only no_image scenario with genuinely absent media, text-layout readiness, Appium image-absence checks, two native captures, three regressions, review packet; no golden promotion/commit. Outcome: implemented; stable candidate AC5BD84B...3012 pending approval; regressions PASS.

## EXEC-030 - no_image promotion (Claude Code, 2026-11-07)
Human prompt: approved exact no_image candidate AC5BD84B...3012; promote byte-for-byte, two no_image + three existing regressions, checks, docs; no empty_feed/commit. Outcome: PASS, all five runs 0 changed, four hashes correct.

## PRE-EXEC-031 - Four-scenario checkpoint (Claude Code, 2026-11-07)
Human prompt: approved exact 18-file inventory plus baseline README status-line fix; selective staging, one local commit without trailer, no push/empty_feed. Outcome: commit 8c54f0f, 18 files, four golden hashes verified in HEAD.

## EXEC-031 - Successful Empty Feed Visual Scenario - 2026-11-07
Prompt: implement empty_feed as a successful zero-article fetch (not offline/error/loading/zero-feeds). Requirements:
- minimal dev-only success-vs-error signal
- real EmptyComponent with a stable boundary that excludes dynamic content
- qa-empty-feed-ready readiness
- registry and allowlist updates
- POM plus test_empty_feed.py; app and Python tests
- populated/empty/populated/empty cold-launch isolation and two native captures
- review packet in debug-logs/exec031/review
- four regressions, checks, docs
No promotion, commit, stage or push.
Outcome: PASS checkpoint. Candidate 903B9710...A795 is pending approval (see 03_HANDOFF).

## EXEC-032 - Empty Feed Golden Promotion and Five-Scenario Verification - 2026-11-07
Prompt: the human approved the exact empty_feed SHA 903B9710...A795 and the message-only boundary. Requested:
- provenance checks and byte-for-byte promotion
- two empty_feed regressions plus the four existing ones
- a five-scenario sequence
- checks and docs, including a fix for stale commit wording
- private records
No stage, commit or push.
Outcome: PASS. All six runs had 0 changed pixels (see 03_HANDOFF).

## PRE-EXEC-033 - Five-scenario checkpoint preparation and finalization - 2026-11-07
Preparation prompt (read-only): reconcile the 14 M / 6 A / 10 scaffolding entries, verify five hashes, scan for privacy and doc consistency, and propose staging commands and a message.
Finalization prompt: apply the approved doc-only corrections (empty_feed commit status, stale f0b38e9 references, five-scenario demonstrated list, POM description), stage exactly 20 files, make ONE commit with no trailer, verify, update private records.
Outcome: commit bcc56b2. No new EXEC started.

## EXEC-033 - Marker-controlled intentional visual failure demonstration - 2026-11-07
Prompt: implement an intentional_failure-marked pytest that genuinely fails comparing the real breaking_news capture against a deterministic incorrect reference in demo_assets/; exclude by default; verify collection; run PASS -> FAIL -> PASS and the five-scenario suite; document PyCharm/PowerShell; no app/golden/threshold changes; no commit.
Outcome: as specified; FAIL exit 1 at comparison (92.41% changed); all other runs 0 changed (see 03_HANDOFF).

## EXEC-034 - Final strategy documentation reconciliation - 2026-11-07
Prompt: reconcile strategy.md/pdf with the five-scenario suite and EXEC-033 mismatch demo; preserve cross-platform strategy as proposals; concise limitations; regenerate and visually inspect PDF; essential README fixes only; no commit; final agent task.
Outcome: PASS; 2-page PDF (see 03_HANDOFF).

## EXEC-035 - 2026-11-07
Prompt: make normal visual pytest tests self-launching for PyCharm without per-scenario VVP_QA_LAUNCH_URL; investigate lifecycle, minimal change, verify individually/suite/default/intentional, document, no commit. Outcome: implemented marker+fixture+launcher URL builder; all verifications passed as recorded in 03_HANDOFF.

## CHECKPOINT-001 - 2026-11-07
Prompt: commit verified EXEC-033/034/035 work as one auditable checkpoint with explicit paths, `*.pdf binary` if needed, hash/test verification, lightweight tag visual-qa-baseline-exec035, no push. Outcome: commit 2bc313e, tag on same commit; details in 03_HANDOFF.


## EXEC-036 - 2026-11-08T00:48:03.068685+01:00
Material request: audit golden regeneration and environment configuration against checkpoint2bc313e; capture fresh real UI candidates, rehearse safe promotion in temporary files, verify suite and hashes, improve only necessary docs, preserve ten scaffolding entries; no reference changes, no commit or CI. Outcome PASS: README capture/review/promotion and config inventory clarified; all five captures0changed, default46passed1deselected; unit41passed; rehearsal safety cases pass; six hashes unchanged. No dotenv/helper justified. Full commands/results and limitations in handoff and ignored debug-logs/exec036.


## EXEC-037 - 2026-11-08T01:20:10+01:00
Material request: separate units/Appium tests, inspect style and PyCharm duplication, extract only meaningful shared infrastructure while preserving scenario launch/assertions/artifacts/cleanup, run requested unit/visual/default/individual/intentional commands, preserve six reference hashes and ten app scaffolding entries; no commit. Outcome PASS: five unit files moved, root pytest.ini, small VisualArtifacts/android_session helpers, nine focused unit cases, README updates; all normal comparisons0pixels and intentional exit1 at comparator assertion. Exact commands/results/limitations in handoff and debug-logs/exec037.


## EXEC-037 bounded exception remediation - 2026-11-08T01:47:41+01:00
Request: preserve original body/launch exceptions and traceback in android_session/make_driver, attempt diagnostics/terminate/quit, expose secondary failures through notes, report successful-body cleanup failures; mocks plus native regression, no unrelated work or commit. Outcome PASS:22focused/68totalunits,73normaltestscollected1demoexcluded,5visualPASS0pixels,intentionalFAILexit1atcomparison; six reference hashes unchanged. Misleading earlier diagnostics test corrected. Exact commands and limitations in handoff; existing working tree preserved.


## EXEC-037 final commit - 2026-11-08T01:55:18+01:00
Request: commit only the human-approved EXEC-037 refactor/remediation, verify staged privacy/scope and parent/status, preserve ten scaffolding entries and references, no trailer/amend/tag/push. Outcome: local main 5a0f2f0026763b437118759b70c64e708e3d3901, parent 09fc21a9bede9cfa1df76d58d17e0802b7466c67;19changes including6renames;staged audit clean,tracked tree clean,tenappentries untouched. Private records only updated after commit.


## EXEC-038
Prompt: integrate optional Allure reporting (evidence per visual test, separate intentional-failure report, local commands, JUnit XML, docs) without changing comparison/goldens/thresholds/SUT; no stage/commit. Outcome: see 03_HANDOFF.md EXEC-038; public summary in docs/ai_prompts_used.md.


## EXEC-039
Prompt: investigate intermittent ~1px image-shift mismatches (dark_article 11147, long_headline 11640) with controlled reproduction, no fixes. Outcome: see 03_HANDOFF.md EXEC-039; evidence in debug-logs/exec039/.

## EXEC-039 cold-boot probe
Prompt: one genuine emulator cold boot, run dark_article/long_headline at ready, 5-10, 20 min after boot, preserve evidence, classify boot-state hypothesis, no fixes. Outcome: no mismatch reproduced; see 03_HANDOFF.md.

## EXEC-040
Prompt: remove discontinued history/prompt docs and update agent instructions, verify four pytest command shapes plus six-test Allure, audit tracked files and history for publication, no history rewrite/commit. Outcome: see 03_HANDOFF.md EXEC-040.

## EXEC-040B
Prompt: implement automatic failure-evidence retention with unit tests, verify intentional failure package, fresh-clone docs audit, classify ten untracked app files, license/brand review, gitleaks scan, history/publication risk review; no commit. Outcome: see 03_HANDOFF.md EXEC-040B.

## EXEC-040C
Prompt: finalize publication readiness (fresh-clone docs with verified/unverified labels, license/brand notice, Algolia key assessment, repo content checks, verification, commit boundaries) without committing. Outcome: see 03_HANDOFF.md EXEC-040C.

## EXEC-040D
Prompt: create two approved local commits (evidence retention; docs/housekeeping) by explicit path, verify, no push. Outcome: see 03_HANDOFF.md EXEC-040D.

## EXEC-040E
Prompt: harden pytest default discovery (exclude artifacts), diagnose cache warning, verify collect/unit/visual from qa_visual/, commit config+doc only. Outcome: see 03_HANDOFF.md EXEC-040E.

## EXEC-041
Prompt: assess whether excluding the ten untracked upstream app/ entries breaks build/runtime/CI; validate Android build from a tracked-only checkout; per-entry recommendations. Outcome: see 03_HANDOFF.md EXEC-041.

## EXEC-042A - 2026-11-08
Prompt: create minimal workflow_dispatch GitHub Actions workflow building the Android debug APK on Ubuntu from committed files (no EAS/secrets/emulator/Appium/unit tests/goldens), document it in README, verify locally, one commit, update private records, stop before 042B.

## EXEC-042A-R1 - 2026-11-08
Prompt: remediate disk exhaustion in first GitHub Android build: add disk diagnostics at checkpoints, conservative measured cleanup of unrelated toolchains, keep build unchanged, no caching, one commit, update private records, stop.

## EXEC-042B - 2026-11-08
Prompt: add dependent advisory emulator job running the five normal Appium visual tests from the built APK, with Allure/evidence artifacts, advisory failure handling, README, one commit, private records, stop; do not claim a GitHub visual run.

## EXEC-042B-R1 - 2026-11-08
Prompt: split the two-job workflow into build-only and manually triggered visual-only workflows reusing an APK from a prior run (source_run_id) with source/compatibility validation, keep emulator/Appium/reporting, update README, one new commit, private records, stop.

## EXEC-042C - 2026-11-08
Prompt: fix visual workflow emulator provisioning (libpulse0, AVD device profile) and make final log collection bounded; no APK/visual changes; validate locally with mocks; one commit; records; stop.

## EXEC-042D - 2026-11-08
Prompt: remove the false-positive bare-ldd QEMU preflight failure, keep real startup failure detection, validate, commit, update records, stop.

## EXEC-042E - 2026-11-08
Prompt: make KVM preflight reliable: udev settle, separate diagnostics, functional open+ioctl check with distinct failure classes, mock validation, one commit, records, stop.

## EXEC-042F - 2026-11-08
Prompt: fix noninteractive AVD creation (explicit "no" via printf pipe, pipefail-safe status, verify config.ini and avdmanager list), mock validation, one commit, records, stop.

## EXEC-042G - 2026-11-08
Prompt: pin ANDROID_AVD_HOME so avdmanager and emulator share one AVD dir; verify registration and emulator -list-avds before launch; mock validation; one commit; records; stop.

## EXEC-042H - 2026-11-08
Prompt: initialize runner-local ADB key pair before emulator boot (adb keygen), restart adb once, state-aware bounded boot diagnostics, mock validation, one commit, records, stop. (One tool call was interrupted by the user; work resumed on instruction.)

## EXEC-042I - 2026-11-08
Prompt: validate API 37 AVD target metadata (conditional Command-line Tools 22.0), add bounded post-boot health gate and install diagnostics from real GitHub surfaceflinger crash evidence; mock validation; one commit; records; stop.

## EXEC-042J - 2026-11-09
Prompt: review GitHub visual failure evidence (.local-evidence, never committed), add bounded scenario-launch failure diagnostics with Allure attachments and classification, QA-only scenario logging, trace deep-link/fixture path, triage native SIGSEGV separately, add visual_scope=breaking_news workflow input, verify (mocks + local emulator), one commit incl. user-edited .gitignore, stop.

## EXEC-042K - Expo developer-menu dismissal and first CI golden comparison
Prompt: dismiss the Expo onboarding overlay (hierarchy-based recognition, one safe click, bounded, strict marker kept, diagnostics + classification expo-dev-menu-overlay), 20 required mock tests, real emulator check, APK compatibility assessment, one local commit, no push. Outcome: implemented incl. a second dev-menu-panel stage discovered on the real emulator; commit test(visual): dismiss Expo onboarding before scenario checks.

## EXEC-042L - isolated no_image crash reproduction
Prompt: add no_image to visual_scope allowlist, keep default all, bounded crash-buffer log collection, verify APK compatibility rule, one local commit, no push. Outcome: commit ci(visual): enable isolated no-image crash reproduction.

## EVAL-001 - final deliverable audit and closure
Prompt: freeze development, audit R01-R12, update strategy and README to verified evidence, draft clean AI disclosure, evidence index, walkthrough and Q&A, one docs commit, no push. Outcome: commit docs: finalize strategy, README and AI disclosure draft.

## README-003 - Final demo guide consolidation
Prompt: consolidate both README guides into one concise root guide with nine specified sections, implemented helper commands and explicit mocked-versus-native verification disclosure; reconcile framework contracts, delete only the nested runner README, fix tracked Markdown references, preserve frozen application/test/CI/goldens and ten untracked app entries; bounded checks only, update private handoff, no commit or push.
Outcome: 204-line root README; nested guide deleted; four cross-references fixed in three retained guides. Link/anchor, five node mappings, script/golden hash checks passed; existing offline helper safety suite rerun with 50 passing cases. No native services/tests/builds/CI or publication. This private entry is not a complete employer-facing AI disclosure.

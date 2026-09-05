---
name: usability-testing
description: Plans usability test sessions, analyses usability test results, and conducts simulated usability walkthroughs for web and mobile applications. Generates goal-oriented task scenarios, participant warm-up prompts, an affinity-diagram analysis structure, and a prioritised findings report. Use when the user asks to "conduct a usability test", "plan a usability study", "analyse usability results", "create test tasks", "write a test script", "build test scenarios", "evaluate my app with users", "run a simulated usability test", "test this app for me", or wants structured usability feedback on screens, flows, or prototypes.
license: Proprietary
metadata:
  version: "1.5.6"
  tags:
    - usability-testing
    - ux
    - research
    - task-scenarios
    - affinity-diagram
    - analysis
    - report
  authors:
    - Heinrich Mostert <heinrich.mostert@bmwithub.co.za>
---

# usability-testing

## Goal

Plan and/or analyse usability tests for a product, delivering task scenarios, participant prompts, and a multi-artifact deliverables pack aligned to the generated PDF outputs.

## Inputs

### Output opening behavior (mandatory)

After generating usability-testing outputs, automatically open the primary artifact for the user.

- Default behavior: open in the VS Code browser tab using `open_browser_page`.
- If the user explicitly asks for the system default browser, open via terminal command `open <url-or-file>`.
- DOCX outputs should be opened with the system default app using `open <docx-file>` (not in browser tab).
- For local HTML files, use absolute `file://` URLs when opening in the browser tab.
- If multiple companion HTML files are generated, auto-open the main report file and list clickable paths for the rest unless the user explicitly asks to open all of them.

### Output format rule (mandatory)

Collect and apply an `output_format` preference before generation.

- Ask `output_format` during Step 0 using `vscode_askQuestions`.
- Allowed values:
  - `Auto (recommended)`
  - `DOCX (editable)`
  - `HTML (report)`
  - `DOCX + HTML`
- Mode-based default when user selects `Auto (recommended)`:
  - `Plan a new usability test` (Mode A): `DOCX + HTML`
  - `Analyse results from a completed test` (Mode B): `DOCX + HTML`
  - `Conduct a simulated usability test` (Mode C): `HTML (report)`

Rationale:

- Human-led planning/analysis outputs are typically iterated and edited by teams, so DOCX should be available.
- Simulated walkthrough outputs are primarily reporting artifacts, so HTML is the default.

### Question delivery rule (mandatory)

Every user prompt in this skill must be asked using the chat questions UI via the `vscode_askQuestions` tool.

- Do not ask required input questions as plain assistant text.
- Do not place questions in freeform narrative paragraphs.
- Ask one field per `vscode_askQuestions` call unless the flow explicitly requires a fixed-option confirmation.
- Follow-up clarifications for missing/invalid input must also use `vscode_askQuestions`.

This applies to Step 0 (including `output_format`), focus-option selection, final scope confirmation, and Mode B findings collection prompts.

### Question counter rule (mandatory)

Show a visible question counter in every `vscode_askQuestions` prompt.

- Use a core linear counter for scope collection: `Q1` to `Q10`.
- Prefix each core question header with `[Qx/10]` (example: `[Q3/10] Mode`).
- Treat Step 0a final scope confirmation as `Q10`.
- For clarifications and iterative focus entry questions, keep the current core counter position and label extra prompts as `[B1]`, `[B2]`, and so on.

Every question prompt must also include a countdown line in the message body:

- Core questions: `Core questions left: N` where `N = 10 - current_core_question_number`.
- Branch questions: `Core questions left: N (branch question)` where `N` is based on the current core position.
- At final scope confirmation (`[Q10/10]`), this must read: `Core questions left: 0`.

At `Q1`, include this expectation line in the question message:

> "You will get 10 core questions. Additional branch questions appear only when needed."

At `Q2` through `Q10`, keep showing only the countdown line (do not repeat the expectation line unless the user asks).

### Step 0 — Collect scope

Before starting, collect scope inputs **one question at a time**.

Do not dump all questions in one prompt. Ask exactly one question, wait for the answer, then ask the next.
Keep the same field headers below and store answers as you go.
Each question must be emitted via `vscode_askQuestions`.

Recommended sequence:

1. `mode`
2. `product`
3. `users`
4. `focus`
5. `roles`
6. `target_groups`
7. `recruitment_plan` (skip for Mode C)
8. `test_type`
9. `output_format`
10. `scope_confirm`

If an answer is missing, ambiguous, or invalid, ask a targeted follow-up for that same field before moving on.
Use `vscode_askQuestions` for these follow-ups.
Mark these as branch prompts (`[B#]`) while keeping the current core question number unchanged.

Mode-based branching at `Q5`:

- If mode (Q1) is `Conduct a simulated usability test` (Mode C), do not ask who will facilitate/support the test.
- For Mode C, use `Q5` to capture which user role(s) the simulated test is catered to.
- For all other modes (A or B), use `Q5` to capture facilitator/support staffing.

Mode-based branching at `Q4` (focus phrasing):

- For Modes A and C: ask "What key user goals or task areas should the test focus on?" (future-planning intent).
- For Mode B: ask "What did the test focus on?" (past-tense; the test has already run).

Mode-based branching at `Q7` (recruitment_plan):

- Skip `Q7` entirely for Mode C. A simulated test has no real participants to recruit. Advance directly from Q6 to Q8.

Because mode is collected first at Q1, all downstream branching rules (Q4, Q5, Q7) are known before those questions are reached.

Mode-based branching at `Q1` for Mode B (findings input method):

- Immediately after the user selects `Analyse results from a completed test`, ask a branch question `[B1]` (scoped to Q1): **How would you like to provide your findings?**
  - `Paste directly in chat` — proceed through all remaining Step 0 questions normally.
  - `Upload a file` (Word `.docx`, Excel `.xlsx`, or `.csv`) — ask for the file path as `[B2]` (scoped to Q1). Mark Q3 (`users`), Q5 (`roles`), Q6 (`target_groups`), and Q7 (`recruitment_plan`) as **deferred**: present them as optional with a note "This will be extracted from your file — confirm or override below." Pre-fill them from the file content at Step 1 and allow the user to correct at Q10.
- For paste input, all Step 0 questions remain required as normal.

Use this format for each step:

- Ask the question for a single field.
- Confirm what you captured in one short line (e.g., "Captured `users`: Backend developers with intermediate experience.").
- Move to the next field.

| #   | Header             | Question                                                                                                                                          | Type                                                                                                                                                                                              |
| --- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | `mode`             | What would you like to do?                                                                                                                        | Single-select: `Plan a new usability test` · `Analyse results from a completed test` · `Conduct a simulated usability test`                                                                       |
| 2   | `product`          | What product or feature are you testing? (URL, description, or file path)                                                                         | Free text, required                                                                                                                                                                               |
| 3   | `users`            | Who are the target users? (role, experience level, or personas)                                                                                   | Free text, required                                                                                                                                                                               |
| 4   | `focus`            | Modes A/C: What key user goals or task areas should the test focus on? Mode B: What did the test focus on?                                        | See focus input rules below                                                                                                                                                                       |
| 5   | `roles`            | Conditional by mode: Mode C — Which user role(s) is this usability test catered to? Modes A/B — Who will facilitate and support the test session? | Free text, required. Mode C: must list intended user roles/personas. Modes A/B: must include a named facilitator (UX expert or team member), project team observers/note-takers, and participants |
| 6   | `target_groups`    | Which sub-target groups/personas are in scope?                                                                                                    | Free text, required                                                                                                                                                                               |
| 7   | `recruitment_plan` | What recruitment plan and participant counts per subgroup are planned?                                                                            | Free text, required for Modes A/B; skip for Mode C                                                                                                                                                |
| 8   | `test_type`        | What are you validating?                                                                                                                          | Single-select: `Concept/prototype` · `Existing application` · `Existing app as basis for new development`                                                                                         |
| 9   | `output_format`    | Which output format do you want?                                                                                                                  | Single-select: `Auto (recommended)` · `DOCX (editable)` · `HTML (report)` · `DOCX + HTML`                                                                                                         |
| 10  | `scope_confirm`    | Please confirm this scope. Should I proceed, or would you like to edit any field?                                                                 | Single-select: `Proceed` · `Edit scope`                                                                                                                                                           |

Do not proceed until all required inputs are answered.

### Mandatory method-quality checks

Before proceeding to any mode, validate the following:

- For Modes A/B: the `roles` input clearly identifies a named facilitator (UX expert or team member), project team observers/note-takers, and participants.
- For Mode C: intended user roles/personas are clearly identified (this can be captured in `users`, `roles`, and/or `target_groups`).
- For Modes A/B only: the recruitment plan includes all listed sub-target groups/personas, and each subgroup has at least 4 participants so recurring usability patterns can be distinguished from one-off behavior and feedback is directionally reliable at subgroup level.
- The participant-count check does **not** apply to Mode C — there are no real participants in a simulated test.

If any subgroup (Modes A/B) is below 4 participants:

- Flag this as a methodological risk.
- Continue only with explicit user confirmation.
- Mark outputs as directional and add a warning in the final report method section, noting reduced confidence due to limited subgroup sample size.

#### Focus input rules

When you reach the `focus` field, present the `focus` question with three options and allow the user to choose one:

| Option | Label                               | Behaviour                                                                                                                                                                                                                                                                                                                                       |
| ------ | ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A      | **Let the skill decide**            | Skip further focus input. After receiving `product` (Q2) and `users` (Q3), analyse the product (via URL inspection, file read, or provided description) and autonomously identify the 3–5 most critical user goals to test. State the inferred focus areas clearly before proceeding so the user can confirm or correct them.                   |
| B      | **Enter focus areas now** (default) | Accept a single free-text response. The user may list one or more task areas in a comma-separated list or as separate lines (e.g. "API key management, project onboarding, search"). Parse each comma-separated or line-separated item as a distinct focus area.                                                                                |
| C      | **Add focus areas one by one**      | After the user selects this option, prompt for focus areas iteratively — one per `vscode_askQuestions` call — until the user selects `Done — finish collecting`. Each prompt must offer a free-text entry field plus a `Done — finish collecting` option. Confirm each entry before asking for the next. Collect all entries before proceeding. |

For Option C iterative prompts, use branch labels (`[B#]`) and keep the core focus step as `[Q4/10]` until focus is confirmed. Start the branch counter at `[B1]` for the first iterative entry. Reset the branch counter independently for each scope question — branch labels do not carry across questions.

Regardless of which option is used, end this step with a confirmation list of the resolved focus areas, e.g.:

> **Focus areas confirmed:**
>
> 1. API key management
> 2. Project onboarding
> 3. Search discoverability
>
> Shall I proceed, or would you like to adjust these?

Do not proceed to Mode A or B until the focus areas are confirmed.

### Step 0a — Final scope confirmation checkpoint

After all Step 0 fields are captured, present a compact summary of all collected inputs and ask:

> "Please confirm this scope. Should I proceed, or would you like to edit any field?"

Ask this confirmation with `vscode_askQuestions` using fixed options such as `Proceed` and `Edit scope`.
This confirmation must be labeled `[Q10/10]`.

If the user selects `Edit scope`:

1. Ask a follow-up question (label: `[B1]` scoped to Q10): "Which field would you like to change?" and list all collected fields as options.
2. Re-ask only that specific field question using the same format as the original question (including the original `[Qx/10]` counter label).
3. After the updated answer is captured, return to `[Q10/10]` and repeat the scope summary and confirmation.

## Only proceed after user confirms with `Proceed`.

## Mode A — Plan a Usability Test

### Step 1 — Define task scenarios

Generate 3–5 realistic, goal-oriented task scenarios following the guidelines in [`references/task-design.md`](references/task-design.md).

For each task produce:

- **Goal** — what the participant should achieve (user-centric, not UI-centric)
- **Scenario prompt** — neutral, realistic language with no UI hints or correct-answer cues
- **Success criteria** — observable outcome that marks task completion

### Step 1b — Align and prioritise use cases with the team

After generating candidate use cases in Step 1, output a **non-blocking priority list** in chat showing:

1. All candidate use cases ranked by estimated user impact.
2. Brief rationale for why each selected use case matters.

Proceed immediately to Step 2 using the top-ranked use cases. Do **not** pause for team confirmation here — this avoids an unnecessary blocking round-trip. The user can adjust task order at the Q11 scope confirmation or by editing the generated artifacts. Note in the output: _"Review and adjust task order in the generated documents before your test session."_

### Step 2 — Create participant prompts

Produce a short warm-up script:

1. **Welcome & consent** — session purpose, recording notice, think-aloud instruction
2. **Background questions** (3 max) — role, familiarity with similar tools, relevant experience
3. **Think-aloud reminder** to include verbatim before each task

Use this mandatory verbatim reminder before the first task and as needed during tasks:

> We are testing the product, not you. There are no right or wrong answers.
> Please think out loud during the task:
>
> - What are you trying to do now?
> - What do you want to do next?
> - What feels good or bad, and why?
> - What did you expect to happen differently?
> - What is unclear?

### Step 2a — Run test-start operational checklist

Before Task 1 starts, complete and log this checklist:

- Camera and audio position verified
- Prototype/app and version confirmed
- Recording started (if applicable)
- Consent confirmed
- Note-taker assigned from project team

Follow `references/moderator-protocol.md` for the exact checklist format.

### Step 2b — Prepare moderator protocol per task

For each task, prepare a moderator protocol sheet including:

- Task complete definition
- Desired/expected path (moderator reference)
- Observed path during execution
- Help type coding:
  - No help
  - Indirect help
  - Negative help
  - Direct clue
- Free observations/comments

Use `references/moderator-protocol.md` to standardise coding.

### Step 2c — Contextual interview module (optional)

When the study goal requires deeper behavioural context, run a contextual interview before tasks.

Use `references/interview-bank.md` for prompts on:

- Recent real-world behaviour
- Triggers and decision criteria
- Information collection and comparison behaviour
- Prior pain points and positive experiences

### Step 2d — Closing interview module (mandatory)

After tasks, run a short closing interview using `references/interview-bank.md`:

- Perceived task difficulty (rating + rationale)
- Expectation mismatch checks
- Most liked / least liked aspects
- Final open feedback

### Step 3 — Summarise the test plan

Produce a concise inline test plan summary in chat (Markdown preview) covering:

- Product & scope
- Target users
- Target subgroups/personas and planned sample per subgroup
- Task list with success criteria
- Recommended session length (typically 45–60 min for 3–5 tasks)
- Participant recommendation: at least 4 participants per subgroup (typically 4–8 depending on heterogeneity) to improve signal stability and reduce outlier bias
- Method quality checklist status (roles, recruitment rule, think-aloud, note-taking, consent/recording)

### Step 3b — Generate Session Deliverables Pack (mandatory)

After the inline Markdown summary from Step 3 is shown, generate the full planning artifacts as files:

1. **UX Designer Test Plan Handout**
2. **Facilitator-only Guide**
3. **Live Session Worksheet**
4. **Affinity Mapping Template**

Save them to `reports/usability-testing/` using these file names, based on `output_format`:

- DOCX variants:
  - `<product-name>-ux-designer-test-plan.docx`
  - `<product-name>-facilitator-only-guide.docx`
  - `<product-name>-live-session-worksheet.docx`
  - `<product-name>-affinity-mapping-template.docx`
- HTML variants:
  - `<product-name>-ux-designer-test-plan.html`
  - `<product-name>-facilitator-only-guide.html`
  - `<product-name>-live-session-worksheet.html`
  - `<product-name>-affinity-mapping-template.html`

When `output_format` is `DOCX (editable)`, generate only DOCX variants for these artifacts.
When `output_format` is `HTML (report)`, generate only HTML variants for these artifacts.
When `output_format` is `DOCX + HTML` or `Auto (recommended)` with Mode A/B, generate both variants.

The structure and section depth should be close to the existing PDF-style outputs in `reports/usability-testing/` (not just a short flow summary).

### Step 4 — Generate User Journey Maps

**Scope guardrail:** Generate journey maps for a maximum of **3 task scenarios** (the highest-priority ones from Step 1b). If more than 3 tasks were defined, note which tasks were deferred and offer to generate them on request.

For each task scenario, produce a user journey map following [`references/journey-mapping.md`](references/journey-mapping.md).

For each task deliver:

- **Primary (happy) path** — the most direct route from task start to completion
- **1–2 alternative paths** — legitimate variations that still lead to success (e.g., search vs. navigation, keyboard shortcut vs. button)
- **Failure / recovery path** — a realistic obstacle and recovery route grounded in known pain points or heuristic predictions
- **Mermaid `flowchart LR`** showing all paths, decision points, and edge labels
- **Predicted emotion scores (text list)** — a concise step-by-step list of scores (−2 to +2) with one-line rationale per step, based on UX heuristics. Label all scores as `Predicted`. Annotate any friction point (score ≤ −1) with the driving heuristic.

> **SVG emotion curve:** Only render the full inline SVG emotion curve (per [`references/journey-mapping.md`](references/journey-mapping.md)) when the user explicitly requests it, or when `output_format` is `HTML (report)` or `DOCX + HTML`. For `DOCX (editable)`, the text-list format above is sufficient and keeps generation fast.

---

## Mode B — Analyse Usability Test Results

### Step 1 — Collect findings input

The input method was already collected in Step 0 as a branch after Q1. Proceed based on the user's selection:

**Option A — Paste in chat:**
Tell the user: "Please paste your session notes or transcripts directly in the chat." Accept freeform text (session notes, transcript excerpts, observer notes, post-session survey data, screen recording descriptions).

**Option B — File upload (`.docx`, `.xlsx`, `.csv`):**
Read the file provided using file tools and extract session observations:

- **Word (`.docx`)** — extract all text. Parse tables row-by-row as individual observations.
- **Excel (`.xlsx`) or CSV** — read as structured data. Recognise columns such as `Participant`, `Task`, `Observation`, `Severity`, `Help Type`; adapt if column names differ. Use quantitative data (SEQ scores, completion rates) in the severity assessment.

**After reading file content (Option B):**

- Show a brief extraction summary: participant count, observation count, tasks identified, and any deferred Step 0 fields now resolved (users, roles, target groups, recruitment plan).
- Ask the user to confirm or correct the extracted values before proceeding to Step 2.
- If any deferred field could not be resolved from the file, ask for it now via `vscode_askQuestions`.

**Structured metadata — collect via `vscode_askQuestions` (one field at a time, for all options, only if not already present in the source):**

- Subgroup/persona membership per participant
- Moderator help-type logs (no help / indirect help / negative help / direct clue)
- Any closing interview ratings and rationales

Do not proceed to Step 2 until at least some session observations have been provided. If none are provided, ask the user to supply them and do not fabricate findings.

### Step 2 — Build affinity diagram structure

Group raw observations into themes following the framework in [`references/analysis-framework.md`](references/analysis-framework.md).

For each theme:

- Label the theme clearly
- List supporting observations (direct quotes or paraphrased notes)
- Note the number of participants affected

Additionally, for each major theme:

- Report subgroup distribution (which subgroup was affected)
- Add a brief root-cause statement explaining why the issue occurred

### Step 2b — Map Observed Journeys and Emotional States

Using the session notes provided, produce an observed journey map for each task following [`references/journey-mapping.md`](references/journey-mapping.md):

- **Observed paths** — document the actual routes taken by participants (happy path, detours, failures); note how many participants took each path
- **Failure points** — identify where participants got stuck, made errors, or abandoned the task
- **Observed emotional journey curve** — plot emotion scores (−2 to +2) at each step derived from:
  - Think-aloud quotes (explicit emotional statements take priority)
  - Behavioural indicators from observer notes (hesitation, repeated attempts, refreshing, asking for help)
  - Post-task SEQ scores if provided
  - Where multiple participants hit the same step, use the median score
- **Mermaid `flowchart LR`** updated with observed path frequencies (e.g., `"Happy path (4/6)"`)
- Label all emotion scores as **Observed** and cite the data source (quote, observer note, or SEQ)
- If a planned journey map was produced in Mode A, note any deviations between the predicted and observed paths

### Step 3 — Rate and prioritise issues

Rate each issue using the severity scale in [`references/analysis-framework.md`](references/analysis-framework.md):

| Severity | Criteria                                                         |
| -------- | ---------------------------------------------------------------- |
| Critical | Blocks task completion for most participants                     |
| High     | Causes significant struggle or abandonment for some participants |
| Medium   | Causes confusion or delay but task is completed                  |
| Low      | Minor friction, cosmetic, or edge-case issue                     |

Add two mandatory evidence indicators per issue:

- **Subgroup spread** — which target groups were affected
- **Moderator intervention signal** — whether and how often help was needed

### Step 4 — Generate findings report

Load and follow the <skill>ux-report-generation</skill> skill to produce a Density-styled report (HTML and/or DOCX based on `output_format`).

**Report sections:**

1. Executive summary (product, scope, participant count, top 3 findings)
2. Affinity diagram / theme groups
3. Per-task journey maps — Mermaid flowchart (observed paths with frequencies) and inline SVG emotional journey curve (Observed scores with data sources)
4. Prioritised issue list with severity ratings
5. Actionable recommendations
6. Method quality appendix (roles, subgroup counts with min-4 rationale check, think-aloud usage, note-taker coverage, consent/recording status)

Save the report using `output_format` rules:

- HTML report: `reports/usability-testing/<product-name>-usability-report.html`
- DOCX report: `reports/usability-testing/<product-name>-usability-report.docx`

When `output_format` is `DOCX + HTML` or `Auto (recommended)` with Mode B, generate both report variants.
When `output_format` is `DOCX (editable)`, generate DOCX report plus DOCX companion artifacts.
When `output_format` is `HTML (report)`, generate HTML report plus HTML companion artifacts.

After saving, automatically open this report using the output opening behavior above.

When Mode B is selected, also generate companion artifacts in `reports/usability-testing/` to keep output aligned with the full deliverables pack:

- `<product-name>-ux-designer-test-plan.<ext>`
- `<product-name>-facilitator-only-guide.<ext>`
- `<product-name>-live-session-worksheet.<ext>`
- `<product-name>-affinity-mapping-template.<ext>`

Where `<ext>` is `docx`, `html`, or both, based on `output_format` and mode defaults.

If Mode A was not run in this session (standalone Mode B):

- Generate these artifacts as **post-hoc templates** populated from the collected scope (product, users, focus, roles, recruitment plan).
- Add a note at the top of each artifact: "Retroactively generated from session scope — not prepared before the study."
- Do not fabricate planning decisions (e.g., task sequences) that were not captured in the scope inputs.

Do not auto-open all companion artifacts by default. Open the primary report automatically and provide paths for the companion files unless the user asks to open all.

---

## Mode C — Conduct a Simulated Usability Test

The skill autonomously walks through the product as a simulated user, executes the planned task scenarios, and produces a findings report — without requiring real participants. This is useful for quick heuristic-informed feedback before recruiting users, or when access to participants is limited.

### Step 1 — Plan (reuse Mode A)

Execute Mode A Steps 1–4 to produce task scenarios, a test plan summary, and predicted journey maps. These become the test script for the simulated walkthrough.

The following Mode A sub-steps are **skipped** for Mode C because they assume real participants or a product team:

- **Step 1b** (team alignment checkpoint) — no product team is present
- **Step 2a** (test-start operational checklist) — no camera, recording, or consent workflow applies
- **Step 2c** (contextual interview module) — no real participants to interview
- **Step 2d** (closing interview module) — no real participants to interview

Execute Steps 1, 2 (warm-up script only, for reference), 2b (moderator protocol per task, for reference), 3, 3b, and 4.

### Step 2 — Conduct the simulated walkthrough

For each task scenario:

1. **Open the product** — if a URL was provided, use browser tools to load the page and take a snapshot. If a file path or description was provided, read the relevant source files or use the description as context.
2. **Attempt the task** — navigate the product step by step following the task scenario. At each step:
   - Capture a snapshot or screenshot of the current state
   - Record what is visible, what actions are available, and what a first-time user would likely try
   - Note any friction: unclear labels, missing affordances, unexpected states, jargon, accessibility gaps
3. **Document the path taken** — record the actual sequence of steps (happy path, detours, dead ends)
4. **Assign emotion scores** — use the heuristic-based scoring from [`references/journey-mapping.md`](references/journey-mapping.md), informed by what was actually observed in the product. Label scores as **Simulated** (not Predicted or Observed)
5. **Note task outcome** — completed successfully, completed with difficulty, or blocked

### Step 3 — Build findings

Using the walkthrough observations:

- Group issues into themes following [`references/analysis-framework.md`](references/analysis-framework.md)
- Rate each issue using the severity scale (Critical / High / Medium / Low)
- Produce observed journey maps with the actual paths taken and simulated emotion scores
- Compare against the predicted journey maps from Step 1 and note deviations

### Step 4 — Generate findings report

Load and follow the <skill>ux-report-generation</skill> skill to produce a Density-styled report (HTML and/or DOCX based on `output_format`).

#### Simulated Walkthrough Disclaimer (mandatory)

Every Mode C report **must** include a prominent disclaimer banner immediately after the Scope & Assumptions section. Use the `[DISCLAIMER_BANNER]` block defined in the `ux-report-generation` report shell. The disclaimer text is:

> _"These findings are based on an automated heuristic walkthrough, not observed user behaviour. Validate critical findings with real users before making high-investment design changes."_

Do not omit, rephrase, or bury this disclaimer inside other sections.

**Report sections:**

1. Executive summary (product, scope, method: simulated walkthrough, top 3 findings)
2. Scope & Assumptions (product, users, focus areas, test type, and any assumptions made during the simulation)
3. Simulated walkthrough disclaimer banner (see above — must appear here, immediately after Scope & Assumptions)
4. Per-task walkthrough results — screenshots, path taken, simulated emotion curve, issues found
5. Affinity diagram / theme groups
6. Prioritised issue list with severity ratings
7. Predicted vs. simulated journey comparison (if Mode A planning step was executed first)
8. Actionable recommendations

Save the report to `reports/usability-testing/<product-name>-simulated-usability-report.html`.

For Mode C, default to HTML when `output_format` is `Auto (recommended)`. If the user explicitly selected `DOCX (editable)` or `DOCX + HTML`, also generate `<product-name>-simulated-usability-report.docx`. The primary artifact opened automatically is always the HTML report when one is generated.

After saving, automatically open this report using the output opening behavior above.

Treat this report as the **Simulated Walkthrough** artifact in the deliverables pack.

---

## References

- **Task design guidelines**: [`references/task-design.md`](references/task-design.md) — read when writing or evaluating task scenarios
- **Analysis framework**: [`references/analysis-framework.md`](references/analysis-framework.md) — read when categorising findings and rating severity
- **Moderator protocol**: `references/moderator-protocol.md` — read when creating test-start checklists, help coding, and task protocol sheets
- **Interview bank**: `references/interview-bank.md` — read when preparing intro, contextual, task follow-up, and closing interview prompts

---
name: synthetic-user-simulation
description: Simulates a persona-based cognitive walkthrough of a workflow, page, or task. Use when teams want fast user-perspective feedback without recruiting real participants — ideal for short sprint cycles. Accepts proto-persona or research-backed persona data and produces step-by-step simulated reactions, friction/delight annotations, and prioritised recommendations. Triggers include "synthetic user simulation", "simulate a user", "persona walkthrough", "test as user", "synthetic user feedback", "walk through as persona", "test this flow as [persona name]", or when a team wants quick persona-based feedback before a usability study.
license: Proprietary
metadata:
  version: "1.1.1"
  tags:
    - persona
    - synthetic-user-simulation
    - cognitive-walkthrough
    - ux
    - feedback
    - sprint
    - usability
    - simulation
  authors:
    - Heinrich Mostert <heinrich.mostert@bmwithub.co.za>
---

# synthetic-user-simulation

## Goal

Simulate a target persona walking through a product workflow or page, producing realistic user-perspective feedback — friction points, confusion, satisfaction, and task-completion likelihood — without requiring real participants.

## Inputs

### Step 0 — Collect scope

Ask the user these questions in a single message:

| #   | Header          | Question                                                                                    | Type                                                                                                                       |
| --- | --------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 1   | `persona`       | How would you like to provide the persona?                                                  | Single-select: `Enter persona details now` · `Use a proto-persona template` · `Load from file`                             |
| 2   | `persona_count` | Are you testing with a single persona or multiple?                                          | Single-select: `Single persona` · `Multiple personas (comparison matrix)`                                                  |
| 3   | `target`        | What should the persona interact with? (URL, workflow description, Figma URL, or file path) | Free text, required                                                                                                        |
| 4   | `tasks`         | What tasks should the persona attempt? (Leave blank for autonomous task identification)     | Free text, optional                                                                                                        |
| 5   | `depth`         | How detailed should the walkthrough be?                                                     | Single-select: `Quick scan` (high-level reactions) · `Standard` (step-by-step) · `Deep dive` (think-aloud style narration) |
| 6   | `output_format` | How would you like to receive the report?                                                   | Single-select: `Markdown (in chat)` · `HTML report` · `Both`                                                               |

Collect all inputs using `vscode_askQuestions` with the appropriate single-select options shown above. Do not proceed until `persona` and `target` are provided.

---

### Step 1 — Establish the persona

Based on the user's selection in Step 0:

#### Option A: Enter persona details now

Prompt the user for the following persona attributes. All fields are optional except **name** and **goal**:

| Attribute                | Description                         | Example                                                          |
| ------------------------ | ----------------------------------- | ---------------------------------------------------------------- |
| **Name**                 | Persona identifier                  | "Maria, Fleet Manager"                                           |
| **Role / Job**           | Professional context                | "Operations manager at logistics company"                        |
| **Goal**                 | Primary goal when using the product | "Quickly assign vehicles to drivers"                             |
| **Tech literacy**        | Low / Medium / High                 | "Medium — uses Excel daily, unfamiliar with developer tools"     |
| **Domain expertise**     | Familiarity with the product domain | "Expert in fleet operations, novice with digital portals"        |
| **Pain points**          | Known frustrations or constraints   | "Time-pressured, interrupted frequently, poor wifi in warehouse" |
| **Accessibility needs**  | Any relevant needs                  | "Uses screen magnification at 150%"                              |
| **Context of use**       | Where/when/how they use the product | "On tablet in warehouse during morning shift"                    |
| **Motivations**          | What drives them                    | "Reduce admin time, avoid errors that delay drivers"             |
| **Frustration triggers** | What makes them abandon a task      | "Unclear jargon, too many steps, slow loading"                   |

#### Option B: Use a proto-persona template

Provide the template from [`references/persona-template.md`](references/persona-template.md) and ask the user to fill in the blanks or confirm defaults.

#### Option C: Load from file

Read the specified file and extract persona data. Confirm the parsed persona with the user before proceeding.

#### Multi-persona intake and confirmation rules

If `persona_count` is `Multiple personas (comparison matrix)`, collect and confirm personas as follows:

1. Collect 2-5 personas using one of these formats:

- Repeated persona cards (one block per persona)
- A Markdown table (one row per persona)
- A structured file (JSON, YAML, or Markdown) with one persona object per entry

2. Require each persona to include at least **name** and **goal**. If either is missing, ask follow-up questions before continuing.
3. Assign a stable persona label for reporting (for example: Persona A, Persona B) while preserving the original names.
4. Show a **Persona Summary Card** for each persona in a single consolidated section.
5. Ask for explicit approval before walkthrough execution using this gate question: "Do these personas look right, and shall I proceed with the walkthrough for all of them?"
6. If the user edits any persona after review, re-display only the changed persona card and request confirmation again.

---

After establishing the persona, display a **Persona Summary Card** as a Markdown table:

| Field                    | Value                              |
| ------------------------ | ---------------------------------- |
| **Persona**              | Maria, Fleet Manager               |
| **Tech literacy**        | Medium                             |
| **Goal**                 | Quickly assign vehicles to drivers |
| **Context**              | Tablet, warehouse, morning shift   |
| **Frustration triggers** | Jargon, many steps                 |
| **Accessibility needs**  | Screen magnification at 150%       |

Ask: "Does this persona look right? Shall I proceed with the walkthrough?"

---

### Step 1.5 — Inspect the interface

Before executing the walkthrough, proactively attempt to load and observe the target:

1. If a URL was provided, open it using `open_browser_page` and take a screenshot with `screenshot_page`.
2. Record what is **directly observable** (navigation structure, key UI elements, page title, visible content sections).
3. Note what **cannot be inspected** (e.g. content behind authentication, pages not yet loaded). Mark every finding that relies on these unobserved areas as an **⚠️ Assumption**.
4. If the target is a workflow description or file path (not a URL), proceed with the information provided and flag all interface details as assumptions.

> **If the page is behind SSO or authentication:** document the login screen itself as a valid finding (e.g. missing pre-login branding, no anonymous preview), and flag all post-login findings as assumptions based on available knowledge.

---

## Walkthrough Execution

### Step 2 — Identify tasks

If the user provided tasks in Step 0, use those. Otherwise, analyse the target (URL, description, or file) and identify 3–5 realistic tasks the persona would attempt, based on their stated goal and context.

Present tasks for confirmation:

> **Tasks for Maria:**
>
> 1. Find and assign an available vehicle to a new driver
> 2. Check the status of today's assignments
> 3. Export a report of the week's fleet usage

### Step 3 — Execute the walkthrough

For each task, simulate the persona's experience step-by-step. Adopt the persona's perspective — their vocabulary, patience level, mental model, and constraints.

For each step produce:

| Field           | Description                                                                       |
| --------------- | --------------------------------------------------------------------------------- |
| **Action**      | What the persona attempts to do                                                   |
| **Expectation** | What the persona expects to happen (based on their mental model)                  |
| **Actual**      | What actually happens in the interface (based on inspection)                      |
| **Reaction**    | Persona's emotional/cognitive response                                            |
| **Friction**    | Any mismatch, confusion, or frustration (severity: Low / Medium / High / Blocker) |
| **Delight**     | Anything that exceeds expectations or feels easy                                  |

#### Depth levels

- **Quick scan**: 1–2 sentences per task summarising overall experience. No step-by-step.
- **Standard**: 3–6 steps per task with the fields above.
- **Deep dive**: Full think-aloud narration in the persona's voice, including internal monologue, hesitations, and emotional shifts. 8–12 steps per task.

#### Accessibility evaluation

If the persona has **accessibility needs** defined (e.g. screen magnification, screen reader, motor impairment, cognitive load sensitivity), evaluate each step against those constraints:

- **Screen magnification**: Are touch/click targets large enough? Does zooming break the layout?
- **Screen reader**: Are interactive elements labelled? Is the reading order logical?
- **Motor impairments / keyboard-only**: Is every action reachable without a mouse? Are focus indicators visible?
- **Cognitive load**: Is the language plain? Are there too many choices or steps?

Annotate affected steps with the accessibility constraint as the friction source (e.g. `Friction: Target too small for magnified view — Severity: High`).

### Step 4 — Produce the feedback report

#### Mandatory disclaimer placement

Include this exact disclaimer text in every report output:

> This is a simulated walkthrough based on persona data. Validate critical findings with real users.

Placement rules:

- For `Markdown (in chat)`, place the disclaimer immediately after the report title and before the Summary section.
- For `HTML report` and `Both`, include the disclaimer banner immediately after Scope & Assumptions (as required by the report contract's Section 2a).

#### Summary section

| Metric                     | Value                                  |
| -------------------------- | -------------------------------------- |
| **Tasks attempted**        | N                                      |
| **Tasks likely completed** | N / N                                  |
| **Overall satisfaction**   | 😊 Positive / 😐 Neutral / 😞 Negative |
| **Top friction points**    | Ranked list                            |
| **Top delight moments**    | Ranked list                            |

**Task completion criteria:**

- **Completed** — No Blocker-severity friction; any friction is Medium or Low.
- **Likely completed** — High-severity friction is present but a workaround exists and the persona could reasonably find it.
- **Not completed** — At least one Blocker-severity friction; the persona cannot proceed without external help.

#### Findings table

| #   | Task | Step | Friction | Severity | Recommendation |
| --- | ---- | ---- | -------- | -------- | -------------- |
| 1   | ...  | ...  | ...      | High     | ...            |

Severity scale:

- **Blocker** — Persona cannot complete the task
- **High** — Persona completes with significant difficulty or frustration
- **Medium** — Noticeable friction but task is completable
- **Low** — Minor annoyance, persona barely notices

#### Persona quote highlights

Include 3–5 simulated quotes "in voice" of the persona to make findings relatable:

> "I clicked 'Fleet Overview' expecting to see my drivers, but this is just a map. Where are my people?" — Maria

### Step 5 — Recommendations

Provide prioritised recommendations:

1. **Quick wins** — Low effort, high impact fixes
2. **Should fix** — Medium effort, clearly reduces friction
3. **Consider** — Nice-to-have improvements
4. **Investigate** — Needs real user validation

---

## Multi-Persona Mode

If the user provides multiple personas, run the walkthrough for each and produce a **comparison matrix**:

| Friction point              | Maria (Fleet Mgr) | Tomás (New Driver) | Overlap |
| --------------------------- | ----------------- | ------------------ | ------- |
| Unclear jargon on dashboard | High              | Blocker            | Yes     |
| No mobile-optimised view    | Medium            | High               | Yes     |
| Export buried in settings   | High              | —                  | No      |

Highlight universal issues (affect all personas) vs persona-specific issues.

---

## Report Output

When `output_format` is `HTML report` or `Both`, load <skill>ux-report-generation</skill> and follow its full workflow:

- Report folder: `reports/synthetic-user-simulation/`
- File name: `<app-name>-synthetic-user-simulation-report.html`
- The report contract's **Section 2a: Automated / Simulated Evaluation Disclaimer** applies — include the disclaimer banner immediately after the Scope & Assumptions section.
- Populate the Findings section with the walkthrough findings table and persona quote highlights as the primary content.
- If `persona_count` is `Multiple personas`, include the comparison matrix as an additional section before Recommendations.

When `output_format` is `Markdown (in chat)`, deliver the full report inline in the chat using the structure defined in Steps 4 and 5 above.

---

## Constraints

- **Never claim to replace real user testing.** Always include a disclaimer: "This is a simulated walkthrough based on persona data. Validate critical findings with real users."
- **Stay in character.** When narrating, maintain the persona's vocabulary and mental model consistently.
- **Do not fabricate interface details.** If you cannot inspect the target, state assumptions clearly and flag them.
- **Bias awareness.** Acknowledge that simulated feedback reflects the persona definition's quality — garbage in, garbage out.

---

## References

- [`references/persona-template.md`](references/persona-template.md) — Proto-persona template for quick input
- [`references/cognitive-walkthrough-method.md`](references/cognitive-walkthrough-method.md) — Background on the cognitive walkthrough methodology adapted for this skill

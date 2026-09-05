# Usability Test Analysis Framework

## Table of Contents

1. [Affinity Diagramming Process](#1-affinity-diagramming-process)
2. [Severity Rating Scale](#2-severity-rating-scale)
3. [Issue Categories](#3-issue-categories)
4. [Frequency & Impact Matrix](#4-frequency--impact-matrix)
5. [Common Usability Patterns to Watch For](#5-common-usability-patterns-to-watch-for)
6. [Subgroup and Intervention Reporting](#6-subgroup-and-intervention-reporting)

---

## 1. Affinity Diagramming Process

Use affinity diagramming to move from raw observations to structured themes.

### Step-by-step

1. **Capture raw observations** — one observation per note (direct quote or paraphrase). Include the participant ID and task number.
2. **Remove duplicates** — merge observations that describe the same issue from different participants.
3. **Group by similarity** — cluster notes that share a root cause or affected area (e.g., "Navigation confusion", "Form validation errors").
4. **Label each cluster** — write a concise, descriptive theme title that captures the shared problem.
5. **Count participants affected** — record how many unique participants contributed to each cluster.
6. **Sort clusters by frequency** — highest participant count first.

### Output format per theme

```text
## Theme: <Label>
Participants affected: X / N

Observations:
- [P1, Task 2] "I didn't know where to click — there are too many options."
- [P3, Task 2] Spent 2 min looking at the sidebar before finding the correct menu.
- [P5, Task 4] "Is this the same page I was just on?"

Subgroups impacted:
- Persona A: X participants
- Persona B: Y participants

Root cause hypothesis:
- Short explanation of why the issue occurred
```

---

## 2. Severity Rating Scale

Rate each distinct issue (not each observation) on this four-point scale:

| Severity | Label        | Criteria                                                                                                      |
| -------- | ------------ | ------------------------------------------------------------------------------------------------------------- |
| 4        | **Critical** | Blocks task completion for most participants. Requires immediate fix before launch.                           |
| 3        | **High**     | Causes significant struggle, repeated attempts, or abandonment for some participants. Fix in the next sprint. |
| 2        | **Medium**   | Causes confusion or delay but the participant eventually completes the task. Plan for a future iteration.     |
| 1        | **Low**      | Minor friction, cosmetic polish, or very infrequent edge-case issue. Backlog candidate.                       |

### Frequency modifier

Adjust severity upward by 1 if ≥ 60% of participants encountered the issue.

### Intervention modifier

Adjust severity upward by 1 when successful completion consistently required moderator support (indirect help, negative help, or direct clue).

---

## 3. Issue Categories

Tag each issue with one or more of these categories to support root-cause analysis and routing to the right team:

| Category                     | Description                                                                   |
| ---------------------------- | ----------------------------------------------------------------------------- |
| **Navigation**               | Users cannot find features, get lost, or use wrong paths                      |
| **Labelling**                | Labels, headings, or button text are unclear or misleading                    |
| **Feedback**                 | System does not confirm actions, show progress, or report errors clearly      |
| **Information architecture** | Content is grouped or ordered in a way that does not match user mental models |
| **Form / input**             | Input fields, validation, or error recovery are confusing or error-prone      |
| **Visual hierarchy**         | Important elements are not visually prominent; users miss key affordances     |
| **Performance perception**   | Users perceive the system as slow or unresponsive                             |
| **Terminology**              | Domain jargon or technical terms confuse non-expert users                     |
| **Missing feature**          | A capability users expected was absent                                        |

---

## 4. Frequency & Impact Matrix

Use this 2×2 to help prioritise recommendations:

```text
            Low Impact          High Impact
            ─────────────────────────────────
High        │  Monitor          │  Fix first  │
Frequency   │  (quick win?)     │  (Critical) │
            ├───────────────────┼─────────────┤
Low         │  Deprioritise     │  Investigate│
Frequency   │  (backlog)        │  (edge case)│
            ─────────────────────────────────
```

- **Fix first** (High frequency + High impact) → Critical / High severity
- **Quick win** (High frequency + Low impact) → Medium severity, often easy to fix
- **Investigate** (Low frequency + High impact) → May indicate a specific persona or edge-case problem worth deeper research
- **Deprioritise** (Low frequency + Low impact) → Backlog only

---

## 5. Common Usability Patterns to Watch For

These patterns frequently emerge in usability tests and map directly to Nielsen heuristics:

| Pattern                      | What to look for                                                                    | Heuristic                              |
| ---------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------- |
| **Lost navigation**          | Participants repeatedly use Back, refresh, or ask "where am I?"                     | H6 Recognition over recall             |
| **Error recovery confusion** | Participants cannot recover from an error without help                              | H9 Error recovery                      |
| **No feedback after action** | Participants repeat an action because they received no confirmation                 | H1 Visibility of system status         |
| **Terminology mismatch**     | Participants use different words than the UI uses for the same concept              | H2 Match between system and real world |
| **Accidental actions**       | Participants trigger destructive actions (delete, submit) without intending to      | H5 Error prevention                    |
| **Cognitive overload**       | Participants are unsure which of many options to choose                             | H8 Aesthetic and minimalist design     |
| **Missing affordances**      | Participants do not discover interactive elements (links that look like text, etc.) | H4 Consistency and standards           |
| **Mental model mismatch**    | Participants expect content to be organised differently from how it is              | H2 Match between system and real world |

---

## 6. Subgroup and Intervention Reporting

Use this section to strengthen findings from "what happened" to "who was affected and why".

### Required per issue

- **Subgroup spread** — specify which target groups were affected and at what rate.
- **Intervention profile** — count how often each help type occurred (No help, Indirect help, Negative help, Direct clue).
- **Why statement** — one concise root-cause explanation grounded in evidence.

### Suggested issue output format

```text
Issue: <short title>
Severity: <Critical|High|Medium|Low>
Participants affected: X / N
Subgroups affected: <list with counts>
Interventions observed: no help=X, indirect=X, negative=X, direct clue=X
Why this happened: <evidence-based root cause>
Recommendation: <action>
```

# Nielsen Heuristic Correlation Guide

## Table of Contents

1. [The 10 Nielsen Heuristics (Quick Reference)](#1-the-10-nielsen-heuristics-quick-reference)
2. [Category → Heuristic Mapping](#2-category--heuristic-mapping)
3. [Keyword Signal Table](#3-keyword-signal-table)
4. [Correlation with Existing Audit Report](#4-correlation-with-existing-audit-report)
5. [Confidence Levels](#5-confidence-levels)

---

## 1. The 10 Nielsen Heuristics (Quick Reference)

| #   | Name                                                    | Core Concern                                                    |
| --- | ------------------------------------------------------- | --------------------------------------------------------------- |
| H1  | Visibility of System Status                             | Does the UI always tell users what is happening?                |
| H2  | Match Between System and the Real World                 | Does the UI use language and concepts familiar to the user?     |
| H3  | User Control and Freedom                                | Can users undo, cancel, or escape easily?                       |
| H4  | Consistency and Standards                               | Do things work the same way across the product?                 |
| H5  | Error Prevention                                        | Does the UI prevent mistakes from happening in the first place? |
| H6  | Recognition Rather Than Recall                          | Can users see their options or must they remember?              |
| H7  | Flexibility and Efficiency of Use                       | Can experienced users shortcut common tasks?                    |
| H8  | Aesthetic and Minimalist Design                         | Is there unnecessary information or visual noise?               |
| H9  | Help Users Recognize, Diagnose, and Recover from Errors | Are error messages clear and actionable?                        |
| H10 | Help and Documentation                                  | Is guidance available when users need it?                       |

---

## 2. Category → Heuristic Mapping

Use the feedback category (from `feedback-analysis-framework.md`) to determine the **primary** and **secondary** heuristics most likely violated.

| Feedback Category                  | Primary Heuristic(s)                 | Secondary Heuristic(s)                        |
| ---------------------------------- | ------------------------------------ | --------------------------------------------- |
| Navigation & Wayfinding (`NAV`)    | H6 — Recognition over Recall         | H1 — Visibility of Status, H4 — Consistency   |
| Visual Design & Layout (`VIS`)     | H8 — Aesthetic and Minimalist Design | H4 — Consistency                              |
| Performance & Speed (`PERF`)       | H1 — Visibility of System Status     | H9 — Error Recovery (if no feedback on delay) |
| Content & Copy (`CON`)             | H2 — Match with Real World           | H4 — Consistency, H10 — Help                  |
| Forms & Input (`FORM`)             | H5 — Error Prevention                | H9 — Error Recovery, H3 — User Control        |
| Accessibility (`A11Y`)             | H4 — Consistency                     | H6 — Recognition over Recall                  |
| Notifications & Feedback (`NOTIF`) | H1 — Visibility of System Status     | H9 — Error Recovery                           |
| Onboarding & Help (`HELP`)         | H10 — Help and Documentation         | H6 — Recognition over Recall                  |
| Data & Tables (`DATA`)             | H6 — Recognition over Recall         | H7 — Flexibility and Efficiency               |
| Mobile & Responsive (`MOB`)        | H4 — Consistency                     | H7 — Flexibility, H8 — Minimalist Design      |
| Trust & Transparency (`TRUST`)     | H2 — Match with Real World           | H1 — Visibility of Status                     |
| Feature Request (`FEAT`)           | H7 — Flexibility and Efficiency      | —                                             |
| Positive Feedback (`POS`)          | —                                    | _(No heuristic violation; note as strength)_  |

---

## 3. Keyword Signal Table

Use these signals to refine heuristic assignment when category alone is ambiguous.

| Keyword / Phrase Signal                                           | Likely Heuristic      |
| ----------------------------------------------------------------- | --------------------- |
| "don't know what happened", "no feedback", "no confirmation"      | H1 — Visibility       |
| "confusing terminology", "technical jargon", "doesn't make sense" | H2 — Real World Match |
| "can't undo", "can't go back", "stuck", "no way out"              | H3 — User Control     |
| "different every time", "inconsistent", "changed without warning" | H4 — Consistency      |
| "accidentally deleted", "no warning", "easy to make mistakes"     | H5 — Error Prevention |
| "can't find", "hard to remember", "have to guess"                 | H6 — Recognition      |
| "takes too many clicks", "no shortcut", "repetitive"              | H7 — Efficiency       |
| "too much info", "cluttered", "overwhelming"                      | H8 — Minimalist       |
| "unhelpful error", "vague message", "don't know how to fix"       | H9 — Error Recovery   |
| "no help", "can't find instructions", "no documentation"          | H10 — Help            |

---

## 4. Correlation with Existing Audit Report

When a `ux-reviewer` report exists in the workspace, compare its findings against the user feedback analysis to surface correlations.

### Correlation Logic

1. **Direct match**: A feedback finding and an audit finding share the same heuristic AND the same UI area → **Strong Correlation** — user evidence validates the auditor's assessment.

2. **Heuristic overlap only**: Findings share the same heuristic but differ in UI area → **Partial Correlation** — heuristic is broadly problematic.

3. **Feedback only**: A feedback cluster identifies a problem not captured in the audit → **Gap in Audit** — flag as missed finding.

4. **Audit only**: An audit finding has no matching user feedback → **Unvalidated Finding** — lower confidence, may still be valid.

### Correlation Output Format

For each correlated pair, record:

```
{
  feedback_id: "F003",
  audit_finding_id: "A007" (or null if no match),
  correlation_type: "Strong | Partial | Gap in Audit | Unvalidated",
  shared_heuristic: "H6 — Recognition over Recall",
  notes: "Both identify navigation confusion on the Settings page."
}
```

### Consolidation Rule

If a feedback cluster and an audit finding are a **Strong Correlation**:

- Elevate the severity of the combined issue by 1 (capped at 4)
- Mark it as **"User-Validated"** in the priority matrix
- Include the combined evidence (audit observation + user quotes)

---

## 5. Confidence Levels

Assign a confidence level to each heuristic correlation:

| Confidence | Criteria                                                             |
| ---------- | -------------------------------------------------------------------- |
| **High**   | Keyword signals clearly match heuristic + audit finding confirms it  |
| **Medium** | Category mapping suggests heuristic, keyword signals partially match |
| **Low**    | Inferred from category alone; no direct keyword signals              |

Document `confidence` in every finding so readers can calibrate trust.

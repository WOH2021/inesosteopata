# Feedback Analysis Framework

## Table of Contents

1. [Supported Input Formats](#1-supported-input-formats)
2. [Feedback Categorization Taxonomy](#2-feedback-categorization-taxonomy)
3. [Sentiment Classification](#3-sentiment-classification)
4. [Priority Matrix Construction](#4-priority-matrix-construction)
5. [Consolidation Rules](#5-consolidation-rules)
6. [Output Data Model](#6-output-data-model)

---

## 1. Supported Input Formats

### Plain Text / Copy-Paste

Treat each paragraph or bullet as one feedback item. Strip headers and metadata before analysis.

```
"The search bar is hard to find on mobile."
"Loading times are too slow after login."
```

### CSV

Expected columns (flexible — use best-match detection if columns differ):

| Column (primary) | Aliases accepted                                        |
| ---------------- | ------------------------------------------------------- |
| `feedback`       | `comment`, `response`, `text`, `message`, `description` |
| `date`           | `timestamp`, `created_at`, `submitted`                  |
| `user_id`        | `user`, `respondent`, `customer_id`                     |
| `rating`         | `score`, `stars`, `satisfaction`                        |
| `category`       | `topic`, `tag`, `type`                                  |
| `source`         | `channel`, `platform`, `survey_name`                    |

If `rating` or `score` is present, normalise to 1–5 scale:

- 1–10 scale → divide by 2 and round
- 0–1 scale → multiply by 5 and round
- CSAT / NPS labels → map Detractor = 1, Passive = 3, Promoter = 5

### JSON

Accept both array-of-objects and `{ items: [...] }` wrapper patterns.

```json
[
  { "id": "f001", "text": "Navigation is confusing", "rating": 2 },
  { "id": "f002", "text": "Love the new dashboard layout", "rating": 5 }
]
```

---

## 2. Feedback Categorization Taxonomy

Map each feedback item to **one primary category** and up to **two secondary categories**.

| Category                 | ID      | Keywords / Signals                                            |
| ------------------------ | ------- | ------------------------------------------------------------- |
| Navigation & Wayfinding  | `NAV`   | lost, can't find, menu, back, breadcrumb, search, filter      |
| Visual Design & Layout   | `VIS`   | looks, ugly, cluttered, spacing, font, color, contrast, icon  |
| Performance & Speed      | `PERF`  | slow, loading, lag, freeze, timeout, crash, refresh           |
| Content & Copy           | `CON`   | wrong info, outdated, unclear, label, text, wording, missing  |
| Forms & Input            | `FORM`  | field, validation, error message, submit, required, dropdown  |
| Accessibility            | `A11Y`  | screen reader, keyboard, zoom, contrast, alt text, ARIA       |
| Notifications & Feedback | `NOTIF` | alert, confirmation, toast, error, success, warning           |
| Onboarding & Help        | `HELP`  | tutorial, tooltip, guide, documentation, confused, first time |
| Data & Tables            | `DATA`  | table, chart, graph, export, sort, filter, row                |
| Mobile & Responsive      | `MOB`   | mobile, phone, tablet, swipe, touch, portrait, landscape      |
| Trust & Transparency     | `TRUST` | unclear why, unexplained, data usage, privacy, confusing AI   |
| Feature Request          | `FEAT`  | would be nice, please add, wish there was, missing feature    |
| Positive Feedback        | `POS`   | great, love, easy, clear, intuitive, fast, helpful            |

---

## 3. Sentiment Classification

Assign each feedback item one of three sentiments:

| Sentiment | Label      | Examples                                               |
| --------- | ---------- | ------------------------------------------------------ |
| Negative  | `negative` | frustration, confusion, failure, complaint             |
| Neutral   | `neutral`  | factual observation, mild suggestion, no clear emotion |
| Positive  | `positive` | praise, satisfaction, delight                          |

When `rating` is available, use it as a ground-truth signal:

- 1–2 → `negative`
- 3 → `neutral`
- 4–5 → `positive`

Override with textual sentiment only if there is a clear contradiction (e.g., rating 4 but clearly negative language).

---

## 4. Priority Matrix Construction

Produce a **Frequency × Severity** priority matrix with four quadrants.

### Severity Scale (0–4, mirrors Nielsen severity)

| Score | Label    | Definition                                          |
| ----- | -------- | --------------------------------------------------- |
| 0     | None     | Positive feedback; no problem                       |
| 1     | Cosmetic | Minor annoyance; low impact on task completion      |
| 2     | Minor    | Noticeable friction; task completion still possible |
| 3     | Major    | Significant obstacle; partial task failure possible |
| 4     | Critical | Blocks task completion entirely; urgent fix needed  |

Derive severity from:

1. Explicit rating (if available) — map to severity scale above
2. Sentiment + strong negative keywords → elevate severity
3. Multi-mention across users → increase severity by 1

### Frequency Calculation

Count occurrences per unique issue cluster (merge near-duplicate items):

- **High**: mentioned by ≥10% of respondents or ≥5 unique users
- **Medium**: mentioned by 3–9% of respondents or 2–4 unique users
- **Low**: mentioned by 1–2% or 1 unique user

### Quadrant Assignment

|                    | Low Severity | High Severity        |
| ------------------ | ------------ | -------------------- |
| **High Frequency** | Monitor      | Critical — Fix First |
| **Low Frequency**  | Backlog      | Investigate          |

### Priority Score Formula

```
priority_score = (severity × 0.6) + (frequency_tier × 0.4)
```

Where `frequency_tier`: Low = 1, Medium = 2, High = 3.

Sort the final matrix descending by `priority_score`.

---

## 5. Consolidation Rules

Before building the matrix, cluster similar feedback items to avoid duplicate counting:

1. **Semantic similarity**: Items with the same root complaint but different wording should be merged.
2. **Category + sentiment**: Items in the same category with the same sentiment are candidates for merging.
3. **Threshold**: Merge items when they describe the same observable UI problem.
4. **Preserve evidence**: Keep 2–3 representative verbatim quotes per merged cluster.

---

## 6. Output Data Model

Each finding in the final analysis should contain:

```
{
  id: "F001",
  title: "Short descriptive title",
  category: "NAV",
  sentiment: "negative",
  severity: 3,
  frequency: "High",
  priority_score: 3.0,
  quadrant: "Critical — Fix First",
  evidence: ["Quote 1", "Quote 2"],
  recommendation: "Concrete, actionable change",
  effort: "Low | Medium | High",
  nielsen_heuristics: ["#6 Recognition over recall", "#1 Visibility of system status"]
}
```

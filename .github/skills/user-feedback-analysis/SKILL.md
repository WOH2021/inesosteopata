---
name: user-feedback-analysis
description: Analyses user feedback from applications to identify pain points and usability issues, consolidates findings into a prioritised matrix, visually verifies issues in the live application via browser, and correlates results with existing UX audit reports. Use when the user provides user feedback (CSV, plain text, or JSON), asks to analyse user research, wants to understand common pain points, needs a prioritised list of UX issues from real user data, wants issues verified against the live app by pasting a URL, or wants to cross-reference feedback with a ux-reviewer report.
license: Proprietary
metadata:
  authors:
    - Heinrich Mostert <heinrich.mostert@bmwithub.co.za>
  version: "0.4.0"
  tags:
    - user-feedback
    - ux
    - research
    - pain-points
    - priority-matrix
    - nielsen
    - usability
---

# User Feedback Analysis

## Goal

Transform raw user feedback into a structured, prioritised set of UX findings — with a Frequency × Severity priority matrix and optional correlation with an existing Nielsen heuristics audit — then generate a Density-styled HTML report.

## Inputs

| Input                         | Required | Notes                                                            |
| ----------------------------- | -------- | ---------------------------------------------------------------- |
| User feedback data            | Yes      | CSV, plain text, JSON, or copy-pasted survey responses           |
| App / product name            | Yes      | Used in report title and naming                                  |
| Application URL               | No       | If provided, enables live visual verification of reported issues |
| Existing Nielsen audit report | No       | If available, enables heuristic correlation                      |

## Outputs

- Structured findings with category, severity, frequency, and quadrant
- Priority matrix (Frequency × Severity, sorted by priority score)
- Visual verification status per finding with screenshots (when URL is provided)
- Heuristic correlation table (when Nielsen audit is provided)
- Density-styled HTML report saved to `reports/user-feedback-analysis/<app-name>-feedback-analysis-report.html`
- Screenshots saved to `reports/user-feedback-analysis/screenshots/`

## Workflow

### Step 0 — Gather inputs

Before starting any analysis, collect all required and optional inputs. If any required input is missing, ask for it explicitly before proceeding.

**Required — ask if not already provided:**

1. **App / product name**

   > "What is the name of the application or product this feedback is for?"

2. **User feedback data**
   > "Please paste or attach your user feedback. I accept plain text, CSV, or JSON. You can copy-paste directly from a survey tool, spreadsheet, or any other source."

**Optional — ask once required inputs are confirmed:**

3. **Existing Nielsen audit report** _(enables heuristic correlation)_

   > "Do you have an existing Nielsen heuristics audit report for this app? If so, please share it and I'll correlate the feedback with its findings."

4. **Application URL for live click-through** _(enables visual verification and correlation)_

   > "Would you like me to open your live application in a browser tab and click through to visually confirm the reported issues? If so, please paste the URL — SSO-protected apps are supported. I'll open it in VS Code's built-in browser and walk through the key areas reported by users."

   Accept any public or internal URL:

   - `https://myapp.example.com`
   - SSO-gated apps (e.g. `https://gaia.bmwgroup.net`) — the browser tab will open and you will be guided through the login flow
   - If the app requires BMW SSO or another identity provider, a login page will appear; follow the interactive login steps before verification begins

Only proceed to Step 1 once the app name and feedback data are both confirmed. Optional inputs can be collected in the same prompt or deferred if the user prefers to skip them.

---

### Step 1 — Ingest and parse feedback

Read the `references/feedback-analysis-framework.md` for format-specific parsing instructions.

- Accept CSV, plain text, or JSON
- Normalise ratings to a 1–5 scale if present
- Strip headers, metadata rows, and empty items
- Confirm the total number of feedback items found

### Step 2 — Categorise and classify

Using the taxonomy in `references/feedback-analysis-framework.md`, Section 2:

1. Assign each feedback item a **primary category** (e.g., `NAV`, `PERF`, `FORM`)
2. Classify **sentiment** (negative / neutral / positive)
3. Cluster near-duplicate items following the consolidation rules in Section 5

### Step 3 — Score severity and frequency

Using Section 3 and 4 of `references/feedback-analysis-framework.md`:

1. Assign a **severity score** (0–4) to each cluster
2. Calculate **frequency tier** (Low / Medium / High)
3. Compute `priority_score = (severity × 0.6) + (frequency_tier × 0.4)`
4. Assign each cluster to a **quadrant** (Critical / Investigate / Monitor / Backlog)

### Step 4 — Map to Nielsen heuristics

Read `references/nielsen-correlation.md` and:

1. Map each finding's category to the most likely heuristic(s) using Section 2 (category table) and Section 3 (keyword signals)
2. Assign a **confidence level** (High / Medium / Low) per finding

### Step 5 — Live click-through and visual verification (if URL provided)

Read `references/visual-verification.md` for the full navigation, SSO handling, and screenshot strategy.

1. **Open in VS Code browser tab** — use `run_vscode_command` with command `simpleBrowser.show` and the URL as the argument. The app will open as an interactive tab inside VS Code.
2. **Handle SSO / authentication** — before opening, inform the user:
   - _"I'm about to open the app in a VS Code browser tab. If a login page appears, please complete the SSO sign-in directly in that tab, then let me know when you're in so I can continue the click-through."_
   - Wait for user confirmation that they are authenticated before proceeding
   - If the app uses BMW SSO or a similar identity provider, do not store credentials in any output
3. **Click-through walkthrough** — once the app is accessible, systematically navigate the key areas reported by users:
   - Use `read_page` to understand the current page structure and available navigation elements
   - Use `click_element` and `navigate_page` to move through the app areas linked to each high-priority finding
   - Group findings by UI area to avoid unnecessary re-navigation (see `references/visual-verification.md`, Section 4)
4. **Capture and correlate** — for each finding with `severity >= 3` or in the Critical / Investigate quadrant:
   - Capture a screenshot with `screenshot_page` and save to `reports/user-feedback-analysis/screenshots/`
   - Assign a `visual_status`: `confirmed`, `not_reproduced`, `partial`, or `inconclusive`
   - Record what was clicked and what was observed to explain the correlation with user feedback
5. **Update findings** — update each finding's `confidence` and add `visual_notes` based on the click-through observations

### Step 6 — Correlate with existing Nielsen audit (if available)

If the user provides an existing `ux-reviewer` report:

1. Follow the correlation logic in `references/nielsen-correlation.md`, Section 4
2. Tag each finding as: Strong Correlation / Partial Correlation / Gap in Audit / Unvalidated
3. Elevate severity by 1 for **Strong Correlation** findings (cap at 4) and mark as **User-Validated**

### Step 7 — Generate the HTML report

Load the <skill>ux-report-generation</skill> skill and follow its specification. Map the analysis output to the required report sections:

| Report Section              | Content                                                                                                                                        |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Cover                       | App name, "User Feedback Analysis", date, reviewer, total feedback items                                                                       |
| Executive Summary           | Total items, clusters identified, critical issues count, top pain point, URL inspected (if applicable)                                         |
| Scorecard                   | Critical / Investigate / Monitor / Backlog finding counts                                                                                      |
| Risk Banner                 | Derived from highest-severity finding                                                                                                          |
| Findings                    | One card per cluster: category, severity, frequency, quadrant, evidence quotes, visual status badge + screenshot (if verified), recommendation |
| Visual Verification Summary | Table: Finding, Status (✅/❌/⚠️/❓), Screenshot thumbnail, Notes — only if URL was provided                                                   |
| Priority Remediation Matrix | All findings sorted by `priority_score` descending; columns: Issue, Category, Severity, Frequency, Visual Status, Effort, Action               |
| Methodology                 | Frequency × Severity matrix method, Density severity scale, Nielsen heuristic correlation, browser verification approach                       |

Save to: `reports/user-feedback-analysis/<app-name>-feedback-analysis-report.html`

## References

- `references/feedback-analysis-framework.md` — Input formats, categorisation taxonomy, priority matrix rules
- `references/nielsen-correlation.md` — Heuristic mapping, correlation logic with existing audit reports
- `references/visual-verification.md` — Browser navigation strategy, screenshot naming, verification outcomes, auth handling

# Evidence and Reporting Workflow

Use this reference for the full Playwright evidence capture process, output format, report generation rules, and PDF handoff.

## Playwright Evidence Collection Protocol

Activate this protocol in all audit modes whenever `Live URL / product access` is selected as evidence. Run it once before scoring begins and keep the captured evidence available throughout the audit.

### Step 1 — Collect the URL and confirm access

#### 1a — Ask for the product URL

Use a single `askQuestion` call:

| #   | Header        | Question                                          | Type                |
| --- | ------------- | ------------------------------------------------- | ------------------- |
| 1   | `product_url` | What is the URL of the product you want to audit? | Free text, required |

Do not open any browser until the URL is provided.

Once the URL is received, use `open_browser_page` to navigate to it.

#### 1b — Handle SSO or login screens

If the page redirects to a login or SSO screen, state:

> _"The product is behind authentication. Please enter your credentials and log in — I'll wait here until you confirm the home screen or landing page is fully loaded."_

Do not take any screenshots or proceed with any audit steps until the user explicitly confirms they are on the authenticated home screen or landing page.

#### 1c — Request consent to begin screen capture

Once the user confirms the landing page is loaded, use a single `askQuestion` call:

| #   | Header               | Question                                                                                                                                                        | Type                                                                                                  |
| --- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| 1   | `playwright_consent` | The product is ready. Playwright will now navigate multiple pages and send a test message to collect audit evidence via screen capture. Do you want to proceed? | Single-select: `Yes — start screen capture` · `No — I'll provide screenshots or descriptions instead` |

- If the user selects **Yes — start screen capture**: take a full-page screenshot and call `read_page` to capture the accessibility snapshot. This is the starting point for all evidence collection. Continue to Step 2.
- If the user selects **No — I'll provide screenshots or descriptions instead**: do not take any screenshots or navigate further. Ask the user to drop in screenshots or describe the product surfaces, then tag all evidence as `[Screenshot-N]` or `[Stated]` for the remainder of the audit.

### Step 2 — Capture the landing state before dismissing anything

- Screenshot any welcome modals, tours, or first-run banners before dismissing them. Record all text and UI elements as evidence for heuristics 1.2, 1.3, 1.4, and 6.1.
- Note all proactive disclaimers, capability statements, or data-use notices visible at this point.
- Then dismiss modals or tours to reach the main interface.

### Step 3 — Systematic section exploration

Navigate to each section below. For each: take a screenshot and call `read_page` to capture the accessibility snapshot. Navigate using the product's own navigation rather than guessed URLs.

| Section                            | What to look for                                                  | Heuristics              |
| ---------------------------------- | ----------------------------------------------------------------- | ----------------------- |
| Home / landing                     | Onboarding copy, capability overview, trust signals, disclaimers  | 1.2, 1.3, 1.4           |
| Chat / main AI interface           | Input affordances, placeholder text, disclaimers, model selector  | 1.1, 1.2, 1.4, 3.1, 4.3 |
| Settings panel                     | Temperature, model options, reasoning controls, advanced settings | 2.1, 4.1, 4.2           |
| Profile / account menu             | Language, feedback access, data deletion option, privacy controls | 2.2, 6.4                |
| Privacy / Imprint / data pages     | Data use statements, retention timeline, consent, deletion flow   | 5.1, 6.1, 6.4           |
| Feedback page                      | Feedback history, submission UI, closing loop messaging           | 2.2                     |
| App Store / feature discovery      | Progressive disclosure, categorisation, feature accessibility     | 4.2, 2.3                |
| Academy / Help                     | Training content, capability docs, prompting guides               | 1.4                     |
| Status / incident page (if linked) | System status, incident history, degraded mode notice             | 6.2, 3.1                |

### Step 4 — Send a test message and capture AI behaviour

In the main chat interface:

1. Type a capability-probing message such as _"What can you help me with? What are your limitations?"_ and submit it.
2. While the AI is generating, take a screenshot immediately to capture the loading state. Record whether a spinner, streaming indicator, progress label, or stop or cancel control is present.
3. After the response renders, hover over the AI response to reveal any hover-action controls such as thumbs up or down, regenerate, copy, or flag. Take a screenshot.
4. Read the full response text for evidence on reasoning transparency, claims, capability disclosure, system status, uncertainty handling, and tone consistency.

### Step 5 — Check security and privacy signals

- Confirm HTTPS from the browser address bar for heuristic 6.3 evidence.
- Look for padlock icons, encryption notices, or security trust indicators at file upload or sensitive data entry points.
- Check whether any sensitive actions trigger step-up authentication.
- Look for a privacy policy link, data use summary, or consent UI accessible within the product.

### Step 6 — Screenshot cap and begin scoring

Start the screenshot counter only once the user confirms the home screen or landing page is fully loaded. Screenshots taken during login or SSO screens do not count toward the cap. The hard cap is 18 screenshots from that point.

When the cap is reached:

- state: _"Screenshot cap of 18 reached — proceeding automatically to audit scoring."_
- note unvisited sections as `[Not visited — cap reached]`
- mark affected items as `[Stated]` or `N/A`
- begin scoring immediately without pausing

Evidence tagging rules:

- Tag all Playwright-captured evidence as `[URL]`.
- Do not re-navigate unless a specific heuristic requires an unvisited section.
- If Playwright cannot load a section because of auth, VPN, or internal-only access, note the reason and use `[Stated]` or `N/A` where necessary.

### Auth failure handling

If Playwright cannot access the product:

1. State clearly: _"Playwright cannot access [URL] — [reason]. Falling back to available evidence."_
2. If screenshots were provided, switch to `[Screenshot-N]` evidence mode.
3. If no screenshots exist, switch to `[Stated]` mode and continue from auditor descriptions.

## Output Format

### 1. Audit Summary

Product name, audit date, auditor, scope, and overall health with Red, Amber, and Green counts.

### 2. Master Scorecard

| ID  | Heuristic                   | ✅ Pass | ⚠️ Partial | ❌ Fail | N/A | Score % | Health |
| --- | --------------------------- | ------- | ---------- | ------- | --- | ------- | ------ |
| 1.1 | AI Reasoning Visible        |         |            |         |     |         |        |
| 1.2 | Personality vs Expectations |         |            |         |     |         |        |
| 1.3 | Appropriate Trust Levels    |         |            |         |     |         |        |
| 1.4 | Interaction Understanding   |         |            |         |     |         |        |
| 2.1 | Human Control               |         |            |         |     |         |        |
| 2.2 | Improvement from Input      |         |            |         |     |         |        |
| 2.3 | Diverse Input/Output        |         |            |         |     |         |        |
| 3.1 | Visible System Status       |         |            |         |     |         |        |
| 3.2 | Errors and Uncertainty      |         |            |         |     |         |        |
| 3.3 | Coherent AI Character       |         |            |         |     |         |        |
| 4.1 | Context Adaptation          |         |            |         |     |         |        |
| 4.2 | Progressive Disclosure      |         |            |         |     |         |        |
| 4.3 | Time and Attention          |         |            |         |     |         |        |
| 5.1 | Data Transparency           |         |            |         |     |         |        |
| 5.2 | Bias and Fairness           |         |            |         |     |         |        |
| 6.1 | Minimum Data Collection     |         |            |         |     |         |        |
| 6.2 | Incident Transparency       |         |            |         |     |         |        |
| 6.3 | Security and Protection     |         |            |         |     |         |        |
| 6.4 | Privacy Best Practices      |         |            |         |     |         |        |

### 3. Priority Matrix

Red heuristics first, then Amber. Per item: Finding, Risk, Owner, Effort, and Recommended action.

### 4. Quick Wins

Fail items with low effort should be scheduled immediately.

### 5. Roadmap Items

Fail or partial items with medium or high effort belong in roadmap planning.

### 6. Role-Specific Actions

- Business and Leadership: liability, regulatory exposure, trust risk
- Product Management: pre-launch gates and sprint priorities
- UX and Design: findings mapped to design system components
- Development: specific technical implementation tasks

## Audit Notes

- Score formula: `(Pass × 1 + Partial × 0.5) / (Total − N/A) × 100`
- Re-audit cadence: Red every sprint, Amber quarterly, full audit bi-annually or after a major model update
- Last framework review: 2026

## Report Generation

After the final Priority Matrix is written, generate the report automatically without waiting for the user to ask.

### Template

Use the template at `.github/skills/ux-report-generation/templates/ai-ux-audit-shell.html` as the structural blueprint. This template lives in the `ux-report-generation` skill and follows the contract (9 required sections in order) with ai-ux-audit-specific extensions appended after Confidence & Gaps.

Important template rules:

- the template uses the `ux-report-generation/templates/report-styles.css` Density tokens as the CSS base, with ai-ux-audit-specific styles appended
- produce a single self-contained HTML file with all CSS inlined
- load `.github/skills/ux-report-generation/SKILL.md` only for the `scripts/generate-pdf.mjs` PDF step

### Contract Compliance

The template follows the ux-report-generation section order:

1. Cover (dark banner with meta-grid)
2. Scope & Assumptions
3. Executive Summary
4. Scorecard (standard 4-box + extended health cards + group donuts + detailed table)
5. Risk Banner
6. Findings (tier-based priority cards)
7. Priority Remediation Matrix (table format)
8. Methodology
9. Confidence & Gaps

Extensions added after section 9:

- Quick Wins
- Roadmap Items
- Actions by Role

### Output Paths

Slugify the product name to lowercase hyphenated form.
Example: `GAIA Gen AI Chat` becomes `gaia-gen-ai-chat`

| Audit Mode              | HTML file name                     | PDF file name                     |
| ----------------------- | ---------------------------------- | --------------------------------- |
| Fresh full audit        | `<app-slug>-audit-report.html`     | `<app-slug>-audit-report.pdf`     |
| Re-audit Red & Amber    | `<app-slug>-reaudit-report.html`   | `<app-slug>-reaudit-report.pdf`   |
| Pre-launch module audit | `<app-slug>-prelaunch-report.html` | `<app-slug>-prelaunch-report.pdf` |

| Output        | Path                                               |
| ------------- | -------------------------------------------------- |
| Report folder | `reports/<app-slug>/`                              |
| Session log   | `reports/<app-slug>/audit-session.md`              |
| HTML report   | `reports/<app-slug>/<app-slug>-<mode>-report.html` |
| PDF report    | `reports/<app-slug>/<app-slug>-<mode>-report.pdf`  |
| Screenshots   | `reports/<app-slug>/screenshots/`                  |

### Filling the Template Placeholders

Replace every `[PLACEHOLDER]` in the template with collected audit data.

| Placeholder                                                             | Source                                              |
| ----------------------------------------------------------------------- | --------------------------------------------------- |
| `[APP_NAME]`                                                            | Product name from Step 1                            |
| `[AUDIT_DATE]`                                                          | Today's date in ISO format                          |
| `[REVIEWER]`                                                            | `GitHub Copilot` or auditor name                    |
| `[MODEL_TESTED]`                                                        | Model used e.g. `Claude Sonnet 4.6`                 |
| `[AUDIENCE]`                                                            | Audience from Step 1                                |
| `[SCOPE]`                                                               | Example: `Full · All 6 Groups · 19 Heuristics`      |
| `[EVIDENCE]`                                                            | Example: `Live URL · Playwright · 8 Screenshots`    |
| `[TOTAL_CHECKS]`                                                        | Total heuristics scored e.g. `19`                   |
| `[SCOPE_TEXT]`                                                          | What was evaluated and out of scope                 |
| `[ASSUMPTIONS_TEXT]`                                                    | Assumptions made during evaluation                  |
| `[EXECUTIVE_SUMMARY_TEXT]`                                              | 3–5 sentence overview                               |
| `[PASS_COUNT]` / `[PARTIAL_COUNT]` / `[FAIL_COUNT]` / `[UNKNOWN_COUNT]` | Standard scorecard counts                           |
| `[OVERALL_PCT]`                                                         | Average score across scored heuristics              |
| `[HEALTH_CLASS]`                                                        | `red`, `amber`, or `green`                          |
| `[HEALTH_LABEL]`                                                        | Example: `At Risk`, `Monitor`, or `Healthy`         |
| `[RED_COUNT]` / `[AMBER_COUNT]` / `[GREEN_COUNT]`                       | Health-band counts                                  |
| `[ALL_COUNT]`                                                           | Total heuristics scored                             |
| `[SC_RED_COUNT]` / `[SC_AMBER_COUNT]` / `[SC_GREEN_COUNT]`              | Scorecard filter counts                             |
| `[RISK_CLASS]`                                                          | `critical`, `high`, `medium`, or `low`              |
| `[RISK_ICON]`                                                           | Emoji: 🔴 🟠 🟡 🟢                                  |
| `[RISK_LABEL]`                                                          | `Critical`, `High`, `Medium`, or `Low`              |
| `[RISK_DESCRIPTION]`                                                    | One sentence overall risk description               |
| `[GROUP_CARDS]`                                                         | Group-card HTML (6 cards)                           |
| `[SCORECARD_ROWS]`                                                      | Scorecard row HTML (19 rows)                        |
| `[PRIORITY_TIERS]`                                                      | Tier blocks and finding card HTML                   |
| `[MATRIX_ROWS]`                                                         | Priority Remediation Matrix table rows              |
| `[FRAMEWORK_DESCRIPTION]`                                               | `AI UX Design Heuristics — 6 groups, 19 heuristics` |
| `[EVALUATION_APPROACH]`                                                 | How evaluation was conducted                        |
| `[CONFIDENCE_LEVEL]`                                                    | `High`, `Medium`, or `Low`                          |
| `[CONFIDENCE_NARRATIVE]`                                                | 1–2 sentences on evidence quality                   |
| `[GAPS_TEXT]`                                                           | What could not be assessed                          |
| `[WIN_ITEMS]`                                                           | Quick win list items                                |
| `[ROADMAP_ITEMS]`                                                       | Roadmap list items                                  |
| `[ROLE_CARDS]`                                                          | Role-card HTML                                      |

### Screenshots

Embed screenshots inside relevant finding cards using:

```html
<div class="finding-screenshot">
  <img
    src="screenshots/[F_SCREENSHOT]"
    alt="[F_SCREENSHOT_ALT]"
    loading="lazy"
  />
</div>
```

Place this block after `.f-chips` and before the closing finding card element. Only include it when a screenshot exists.

## Audit Complete

1. Ensure the output folder exists:

```bash
mkdir -p reports/<app-slug>/screenshots
```

2. Save the HTML report to `reports/<app-slug>/<app-slug>-<mode>-report.html` using the naming convention from the Output Paths table above (`audit` · `reaudit` · `prelaunch`).
3. Confirm the saved report path.
4. Ask once whether a PDF should be generated.
5. If yes, load `.github/skills/ux-report-generation/SKILL.md` and run only the PDF generation step.
6. If no, stop immediately.

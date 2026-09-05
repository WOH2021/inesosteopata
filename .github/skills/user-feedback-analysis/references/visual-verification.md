# Visual Verification via Browser

This reference guides the Playwright-based live verification step. It instructs Claude how to open the user's application in the browser, navigate to the relevant UI areas for each high-priority finding, capture screenshots as visual evidence, and update the confidence and verification status of each finding.

## Table of Contents

1. [When to Run Visual Verification](#1-when-to-run-visual-verification)
2. [Ask for the URL](#2-ask-for-the-url)
3. [Browser Navigation Strategy](#3-browser-navigation-strategy)
4. [Category → Navigation Hints](#4-category--navigation-hints)
5. [Verification Outcomes](#5-verification-outcomes)
6. [Screenshot Naming and Storage](#6-screenshot-naming-and-storage)
7. [Updating Findings After Verification](#7-updating-findings-after-verification)
8. [Handling Auth-Protected and SSO Apps](#8-handling-auth-protected-and-sso-apps)
9. [Click-Through Walkthrough Strategy](#9-click-through-walkthrough-strategy)

---

## 1. When to Run Visual Verification

Always offer visual verification after Step 4 (Nielsen heuristic mapping). Run it for:

- All findings with `severity >= 3` (Major or Critical)
- All findings in the **Critical — Fix First** or **Investigate** quadrant
- Any finding where the user specifically asks to verify it

Skip visual verification for:

- `POS` (positive feedback) findings — nothing to verify
- Findings with `severity <= 1` unless user requests it
- Feature requests (`FEAT`) — no existing UI to verify against

---

## 2. Ask for the URL

Step 0 of the skill gathers the URL. If it was not provided there, ask:

> "Would you like me to open your live application in a browser tab and click through to visually confirm the reported issues? If so, please paste the URL — SSO-protected apps (including BMW SSO) are supported."

If the user provides a URL, proceed with visual verification. If they skip or decline, mark all findings as `visual_status: "Not Verified"` and continue to report generation.

Accept:

- Public URLs: `https://myapp.example.com/dashboard`
- BMW internal / SSO-gated URLs: `https://gaia.bmwgroup.net`, `https://developer-home.bmwgroup.net`
- Paths that imply a starting page: `https://myapp.example.com` (start from home)

**SSO note:** If the URL redirects to an identity provider login page (e.g., BMW SSO, Azure AD, Okta), the browser tab will land on that login page first. Follow the instructions in Section 8 before beginning the click-through.

---

## 3. Browser Navigation Strategy

### Opening the app

Use `run_vscode_command` with command `simpleBrowser.show` and the URL as the argument. This opens the URL in an interactive VS Code browser tab that the user can see and navigate directly.

Before opening, inform the user:

> _"I'm about to open the app in a VS Code browser tab. If a login page appears, please complete the SSO sign-in directly in that tab, then let me know when you're in so I can continue."_

Wait for the user to confirm they are authenticated before proceeding. Then attempt `read_page` to understand the current page structure — note that `read_page`, `click_element`, and `screenshot_page` may not have access to the Simple Browser session. If any of these fail, ask the user to describe what they see or provide screenshots, and skip to Section 9 for the manual walkthrough strategy.

### Navigation approach (per finding)

For each finding being verified:

1. **Identify the target area** — use the finding's category and evidence keywords to determine which part of the UI to inspect (see Section 4)
2. **Navigate** — use `navigate_page` if the relevant content is on a different route, or `click_element` to reach it via in-page navigation
3. **Read the page** — use `read_page` to get the current DOM-level understanding
4. **Capture screenshot** — use `screenshot_page` to record visual evidence
5. **Assess** — determine the verification outcome (see Section 5)

### Efficient navigation

- Group findings by area of the app before navigating — verify all issues in the same section before moving on
- Use `screenshot_page` at the start of each section visit (one screenshot per distinct page/view)
- Do not reload the page unnecessarily between findings in the same view

---

## 4. Category → Navigation Hints

Use these hints to determine where in the app to look for each finding category.

| Category                           | Where to navigate                          | What to look for                                          |
| ---------------------------------- | ------------------------------------------ | --------------------------------------------------------- |
| Navigation & Wayfinding (`NAV`)    | Main menu, sidebars, breadcrumbs, search   | Missing nav elements, inconsistent menus, hidden search   |
| Visual Design & Layout (`VIS`)     | Any reported page                          | Cluttered UI, poor contrast, icon ambiguity               |
| Performance & Speed (`PERF`)       | Login flow, data-heavy pages               | Loading spinners, skeleton screens, perceived delay cues  |
| Content & Copy (`CON`)             | Page headings, labels, tooltips            | Jargon, vague labels, outdated copy                       |
| Forms & Input (`FORM`)             | Forms, modals, input fields                | Missing labels, unclear validation, placeholder-as-label  |
| Accessibility (`A11Y`)             | Any reported page                          | Missing focus indicators, no alt text, color-only signals |
| Notifications & Feedback (`NOTIF`) | After submit actions, error flows          | Confirm/success messages, error banners                   |
| Onboarding & Help (`HELP`)         | First-run screens, help menus              | Missing tooltips, no guidance, broken help links          |
| Data & Tables (`DATA`)             | Tables, dashboards, charts                 | Sort/filter controls, export buttons, column clarity      |
| Mobile & Responsive (`MOB`)        | Resize viewport or check responsive layout | Overlapping elements, tiny tap targets                    |
| Trust & Transparency (`TRUST`)     | AI features, data displays                 | Unexplained decisions, missing data sources               |

---

## 5. Verification Outcomes

After inspecting each finding, assign one of four statuses:

| Status            | Label            | Meaning                                                    |
| ----------------- | ---------------- | ---------------------------------------------------------- |
| ✅ Confirmed      | `confirmed`      | The issue is visually present in the live app              |
| ❌ Not Reproduced | `not_reproduced` | The issue could not be found in the current UI             |
| ⚠️ Partial        | `partial`        | The issue exists but only in specific states or contexts   |
| ❓ Inconclusive   | `inconclusive`   | Cannot determine without user credentials or specific data |

**Effect on severity:**

- `confirmed` → keep severity as-is; mark as **"Visually Confirmed"**
- `not_reproduced` → reduce confidence to **Low**; note "Not present in current UI"
- `partial` → keep severity; add note "Reproduced only in [specific context]"
- `inconclusive` → keep severity; add note "Auth/data required to fully verify"

---

## 6. Screenshot Naming and Storage

Save all screenshots to: `reports/user-feedback-analysis/screenshots/`

Naming convention:

```
<finding-id>-<category>-<short-description>.png
```

Examples:

- `F001-NAV-search-bar-missing.png`
- `F003-FORM-validation-error.png`
- `F005-PERF-no-loading-indicator.png`

In the HTML report, embed each screenshot inline using a `<figure>` with a caption describing what the screenshot illustrates.

---

## 7. Updating Findings After Verification

After visual verification, update each verified finding's data model with:

```
{
  visual_status: "confirmed | not_reproduced | partial | inconclusive",
  screenshot: "reports/user-feedback-analysis/screenshots/F001-NAV-search-bar-missing.png",
  visual_notes: "Search bar is hidden behind a collapsed hamburger menu on desktop — not visible by default."
}
```

Add a **Visual Verification Summary** section to the report between Findings and the Priority Remediation Matrix:

| Finding                          | Status          | Screenshot   | Notes                             |
| -------------------------------- | --------------- | ------------ | --------------------------------- |
| F001 — Search bar hard to find   | ✅ Confirmed    | [screenshot] | Hidden behind collapsed menu      |
| F003 — Form error messages vague | ✅ Confirmed    | [screenshot] | Only shows "Error" with no detail |
| F005 — No loading indicator      | ❓ Inconclusive | —            | Could not trigger loading state   |

---

## 8. Handling Auth-Protected and SSO Apps

Many internal BMW applications are protected by SSO (e.g., BMW Group Alpha SSO, Azure AD, Okta). The browser tab will open on the identity provider login page rather than the app itself.

### Detecting SSO

Before calling `run_vscode_command`, proactively inform the user:

> _"I'm about to open the app in a VS Code browser tab. If you see a login or SSO page, please complete the sign-in there and let me know when you're in."_

After opening, if the user reports a login page (or if `read_page` returns a URL containing `sso`, `login`, `auth`, `idp`, `XUI`, or `oauth2`), confirm that SSO is required and wait for the user to complete authentication in the VS Code tab.

### SSO login flow

1. Wait for the user to confirm they have completed login
2. After confirmation, call `read_page` again to verify the app has loaded (URL should no longer be the identity provider domain)
3. Take an initial `screenshot_page` of the authenticated landing page as orientation evidence
4. Proceed with the click-through walkthrough (Section 9)

### If credentials must be typed interactively

If the user explicitly provides credentials to type (e.g., a test account):

- Use `type_in_page` and `click_element` to complete the login form
- **Never store, log, or include credentials in any file or report output**
- Use them only for the active browser session

### If login cannot be completed

If authentication cannot be completed (no credentials provided, MFA required, access restrictions):

- Mark all findings inside protected pages as `visual_status: "inconclusive"`
- Add note: "Authentication required — SSO login could not be completed during this session"
- Still run verification on any publicly accessible areas of the app

---

## 9. Click-Through Walkthrough Strategy

Once the app is accessible (authenticated or public), perform a systematic click-through that maps directly to the reported findings rather than a generic tour.

### Preparation

Before navigating, compile a **verification route**: an ordered list of UI areas to visit, grouped by region to minimise back-and-forth navigation. Derive the route from the findings in the Critical and Investigate quadrants.

### Walkthrough sequence

1. **Orientation screenshot** — take a full-page screenshot of the landing/home state before clicking anything. Save as `F000-overview-home.png`.
2. **Navigate to each area in the route**:
   - Use `click_element` for in-page links, menu items, tabs, and CTAs
   - Use `navigate_page` for direct URL changes (e.g., specific route paths)
   - After each click, use `read_page` to confirm the navigation succeeded
3. **Attempt to reproduce the reported scenario**:
   - For search findings: type a search term and observe results (or lack thereof)
   - For navigation findings: right-click targets using `read_page` to inspect the element type (`<a>` vs `<div>`)
   - For performance findings: note any visible loading states, spinners, or blank content areas
   - For layout findings: take a screenshot at the reported viewport
4. **Capture evidence**: take a `screenshot_page` for each finding area and save with the naming convention in Section 6
5. **Record the correlation**: for each screenshot, note:
   - What user feedback it relates to (finding ID and quote)
   - What was clicked / navigated to
   - What the screenshot shows that confirms, partially confirms, or contradicts the reported issue

### Click-through documentation block

Add a **Click-Through Correlation Log** to the report's Visual Verification Summary section:

| Step | Area Visited       | Action Taken                        | Finding Correlated   | Outcome                            |
| ---- | ------------------ | ----------------------------------- | -------------------- | ---------------------------------- |
| 1    | Home / Landing     | Opened URL, observed landing state  | F005 — cluttered IA  | ✅ Confirmed                       |
| 2    | Search             | Typed keyword, clicked result       | F001 — search broken | ✅ Confirmed — click had no effect |
| 3    | Nav items          | Right-clicked nav item              | F004 — no new tab    | ✅ Confirmed — `<div>` not `<a>`   |
| 4    | Documentation page | Clicked doc link from search result | F002 — blank page    | ✅ Confirmed — blank white page    |

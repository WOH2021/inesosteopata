---
name: ux-reviewer
description: Conducts a UX heuristic audit using Nielsen's 10 usability heuristics and returns prioritized findings with severity, impact, and concrete recommendations. Use when the user asks for a UX review, usability audit, heuristic evaluation, or wants structured UX feedback on screens, flows, prototypes, or product experiences.
license: Proprietary
compatibility: Works with live URLs (browser tools), screenshots (visual analysis), and Figma links (Figma MCP); HTML/PDF report generation requires filesystem and Node.js access (ux-report-generation skill). A structured chat response is the fallback when those tools are unavailable.
metadata:
  authors:
    - "Adele Campbell <Adele.Campbell@bmwithub.co.za>"
    - "Heinrich Mostert <heinrich.mostert@bmwithub.co.za>"
  version: "1.5.1"
  tags:
    - ux
    - usability
    - heuristic-evaluation
    - nielsen
    - audit
    - visual-design
    - interaction-design
    - enforced-checks
---

# ux-reviewer

## Goal

Produce a structured Nielsen heuristic audit with evidence-based findings, severity ratings, and actionable recommendations.

## Inputs

### Step 0 — Ask the user how they want to provide their UI for audit

**MANDATORY: Before starting any audit, ask the user this question in chat:**

> **How would you like to provide the UI for the audit?**
>
> Please choose one of the following options:
>
> **1. URL** — Paste a live URL and I'll inspect it with browser tools (contrast, hover states, console errors, etc.)
>
> **2. Screenshots** — Share one or more screenshots directly in the chat and I'll evaluate them visually.
>
> **3. Figma file** — Paste a Figma link and I'll read the design using the Figma MCP.

Wait for the user's answer before proceeding. Then ask the follow-up:

- **If URL:** "Please paste the URL(s) you'd like me to audit."
- **If screenshots:** "Please share the screenshot(s) in the chat. Feel free to add any context about the screen or user flow."
- **If Figma:** "Please paste the Figma URL(s) in the format `https://www.figma.com/design/:fileKey/:fileName?node-id=1-2`. I'll use the Figma MCP to read the design."

---

### Input Method Workflows

#### Option A — URL

Use browser tools (open_browser_page, screenshot_page, read_page, run_playwright_code) to:

- Navigate to the URL.
- Capture screenshots for the report.
- Run accessibility checks (contrast, keyboard, ARIA, console errors).
- Execute mandatory checks from Steps 1–2 using live DevTools data.

#### Option B — Screenshots

Analyse the screenshots directly:

- Evaluate all 10 Nielsen heuristics visually.
- Flag any contrast, layout, hierarchy, or interaction issues observable from the images.
- Note that browser-based mandatory checks (console errors, hover states, tab order) **cannot be performed** on static images — explicitly state this in the Confidence and Gaps section.
- Lower confidence ratings for findings that require live interaction to confirm.

#### Option C — Figma File

Load the **`figma-design-to-code`** skill at `.github/skills/figma-design-to-code/SKILL.md` which defines how to work with the Figma MCP, then:

- Extract the `fileKey` and `nodeId` from the Figma URL.
- Call `mcp_figma-mcp_get_design_context` with the extracted `fileKey` and `nodeId` to retrieve design data, a screenshot, and component context.
- Call `mcp_figma-mcp_get_screenshot` for additional visual reference if needed.
- Evaluate design tokens, spacing, hierarchy, and component usage from the Figma data.
- Note that runtime checks (console errors, hover states, live tab order) **cannot be performed** on Figma designs — explicitly state this in the Confidence and Gaps section.
- Lower confidence ratings for findings that require a live implementation to confirm.

---

### Additional Context

Gather as many of these as available:

- Product context (user role, primary goals, domain constraints)
- Audit scope (screens, user journey, feature area)
- Platform and constraints (web/mobile, accessibility, legal, technical limits)
- Known issues or business priorities

If inputs are incomplete, state assumptions explicitly before evaluating.

## Outputs

Deliver a comprehensive audit report containing:

1. Scope and assumptions
2. Findings table (issue, heuristic, evidence, severity, recommendation) covering:
   - Nielsen heuristic violations
   - Visual design and layout issues
   - Interaction design problems
   - Design system compliance issues
   - Microcopy and labeling problems
   - Technical issues (errors, loading states)
3. Prioritized remediation plan (quick wins, medium effort, strategic work)
4. Issue coverage validation (confirm findings span multiple categories)
5. Optional score summary by heuristic with confidence notes

**Quality bar:** A thorough audit should identify 18-25 issues across diverse categories on complex pages (validated through testing). If you find fewer than 15 issues, systematically re-examine using the checklists in step 2.

**MANDATORY CHECKS:**

These checks are conditional on the input method. Skipping an applicable check makes the audit INCOMPLETE.

**URL audits (Option A) — all four checks are required:**

1. Hover state testing on at least 5 interactive elements
2. Full page scroll with sticky element observation
3. Console error check (before and after interactions)
4. Heading hierarchy with exact pixel sizes

**Screenshot audits (Option B) — browser-based checks are not applicable:**

1. Hover state testing — **not applicable** (static image); note in Confidence and Gaps
2. Full page scroll — evaluate visible layout only; note any clipping or scroll context assumptions
3. Console error check — **not applicable** (no live runtime); note in Confidence and Gaps
4. Heading hierarchy — infer visually from font size/weight; note pixel sizes cannot be confirmed

**Figma audits (Option C) — runtime checks are not applicable:**

1. Hover state testing — **not applicable** (design file); note in Confidence and Gaps
2. Full page scroll — evaluate frame layout only; note in Confidence and Gaps if scrolling behaviour cannot be assessed
3. Console error check — **not applicable** (no live runtime); note in Confidence and Gaps
4. Heading hierarchy — read from design tokens or computed values in Figma data; note any gaps

For Options B and C, all not-applicable checks **must be disclosed** in the Confidence and Gaps section of the report.

## Steps

> **Reminder:** Complete Step 0 (ask the user for input method) before executing any of the steps below.

### 1. Define Scope and Risk Context

- Confirm what is in scope and out of scope.
- Identify primary user tasks and failure costs.
- Mark any missing information that limits confidence.
- **Use browser dev tools:** Open element inspector, accessibility panel, and console to identify issues.

### 1.1 Use Browser Tools for Deep Analysis

> **Applies to: Option A (URL) only.** For screenshots or Figma input, skip the browser tool steps and document the limitation in the Confidence and Gaps section.

When conducting audits with browser access, leverage these tools:

> **Accessibility note:** Contrast ratios, ARIA, keyboard accessibility, and WCAG checks are handled by the **`designops-accessibility`** skill. Run it alongside this audit for a complete review.

**Element Inspector:**

- Measure spacing values (padding, margins) for consistency
  - Use ruler tool to verify alignment (vertical and horizontal)
  - Check for diagonal misalignments (elements shifting as you scroll)
- Check computed font sizes and line heights
  - Document any text under 14px (accessibility concern)
- Verify responsive breakpoints and layout behavior
- Inspect hover/focus state CSS separately

**Console:**

- Look for JavaScript errors that impact UX
- Check for failed API calls or resources
- Monitor performance warnings
- **Clear console, then interact:** Click, scroll, navigate - watch for new errors

**Network Tab:**

- Identify slow-loading resources affecting perceived performance
- Check for failed requests that may cause missing content
- Monitor for 404 errors or timeout issues

### 2. Evaluate Against All 10 Heuristics

Read `references/nielsen-heuristics-checklist.md` and assess each heuristic systematically.

**IMPORTANT:** Before evaluating heuristics, perform systematic analysis in these areas:

#### 2.1 Visual Design & Layout Analysis

- [ ] Check spacing consistency (padding, margins between sections)
  - Measure exact values with inspector: "Section A: 20px margin, Section B: 24px margin"
  - Document any variations over 4px as potential inconsistency
- [ ] Verify heading hierarchy (H1 → H2 → H3 logical progression)
  - Check computed font sizes don't break hierarchy
  - Flag if H2 appears smaller than H3
- [ ] Identify sizing inconsistencies (buttons, images, cards)
  - Measure heights/widths: "Button A: 40px, Button B: 32px"
  - Check image aspect ratios for consistency
- [ ] Look for visual weight balance and information density
- [ ] **Check alignment and grid consistency (REQUIRED):**
  - Execute this check: Measure left position of 3-5 elements that should align
  - Document measurements: "Element A: 40px left, Element B: 40px left, Element C: 45px left (5px misalignment)"
  - Flag if alignment varies by >5px without visual justification
  - Example issue: "Card titles left-aligned at x:40px but buttons below are centered at x:200px - diagonal misalignment"
- [ ] **Review Gestalt grouping principles (OBJECTIVE THRESHOLDS):**
  - **Proximity Rule:** Measure distance from button to its parent vs. distance to next section
    - Related elements should be <24px apart
    - Unrelated elements should be >32px apart
    - **Violation threshold:** If button is >30px from its content but <20px from unrelated content = FLAG
  - Document measurements: "CTA button 40px below parent card, but only 16px above next section (grouping violation)"
  - Example: "Profile button at y:450px, card ends at y:410px (40px gap), next section starts at y:466px (16px gap) - button appears grouped with wrong content"

> **Accessibility:** WCAG 2.1/2.2 checks (contrast, ARIA, keyboard, screen reader, alt text, focus indicators) are out of scope for this audit. Use the **`designops-accessibility`** skill at `.github/skills/designops-accessibility/SKILL.md` for a dedicated accessibility review.

#### 2.3 Interaction Design Inspection

- [ ] **Test hover states separately (MANDATORY - Test 5+ elements minimum):**
  - **REQUIREMENT:** Physically hover over at least 5 interactive elements (or ALL if fewer than 5)
  - For EACH element document: normal state → hover state change
  - Example: "Button normal: #037493 background, Hover: #025a73 (darker) - PASS: clearly visible"
  - Example violation: "Link normal: rgb(51,51,51), Hover: rgb(85,85,85) - FAIL: insufficient contrast change"
  - **Enforcement:** If you don't have documented hover states for 5+ elements, re-test
  - Check cursor changes to 'pointer' on hover
  - Verify hover doesn't hide critical information
- [ ] **Test focus states separately (MANDATORY - Tab through page):**
  - **REQUIREMENT:** Press Tab key at least **10 times** (MINIMUM) and document focus progression
  - Document first 10 focused elements: "Tab 1: Search input (blue outline 2px), Tab 2: Logo link (outline visible), etc."
  - Flag if ANY interactive element has no visible focus state
  - Ensure focus order is logical (follows visual layout)
  - **Enforcement:** If fewer than 10 Tab stops documented, audit is incomplete
- [ ] Verify clickability affordances (cursor changes, visual cues)
  - Check elements that look clickable are actually clickable
  - Check non-clickable elements don't suggest clickability
- [ ] **Test footer/bottom navigation (MANDATORY - Must scroll to bottom):**
  - **REQUIREMENT:** Scroll to bottom of page and document footer behavior
  - Check if footer is sticky: "Footer remains visible during scroll" or "Footer only appears at bottom"
  - Test: Scroll to middle of page, does footer stay visible? Document yes/no.
  - If sticky elements present, scroll entire page and flag any overlap/z-index issues
  - Verify bottom CTAs remain accessible and don't hide content
  - **Enforcement:** If you haven't scrolled to bottom and tested footer, you MUST do so
- [ ] **Carousel/slideshow testing (if present):**
  - Check for presence: Search for carousel, slider, slideshow in page
  - If found: Test prev/next controls with mouse and keyboard
  - Verify keyboard navigation (arrow keys work)
  - Check auto-play can be paused
  - Verify pagination shows current position
  - If NO carousel found, document: "No carousel/slideshow elements detected"
- [ ] **Manual interaction bug testing (MANDATORY - Active testing required):**
  - **REQUIREMENT 1: Full page scroll**
    - Scroll from top to bottom slowly
    - Document any: sticky element bugs, content jumping, layout shifts
    - Example: "At 50% scroll, sticky header overlaps content" or "No scroll bugs detected"
  - **REQUIREMENT 2: Interactive element testing**
    - Click at least 3 different interactive elements (buttons, links, menus)
    - Document behavior: "Clicked menu icon: menu opens cleanly" or "Clicked button: no response (bug)"
  - **REQUIREMENT 3: Console error check**
    - Open browser console BEFORE interactions
    - Interact with page (click, scroll)
    - Document any errors: "3 errors logged: 404 on /api/tools" or "No console errors"
  - **Enforcement:** If no interaction testing documented with specific results, audit is incomplete
- [ ] Check loading and transition states
- [ ] Test error states and empty states
- [ ] Verify interactive elements are clearly distinguishable from static content

#### 2.4 Design System Compliance (if applicable)

**If BMW Density or other design system is specified:**

- [ ] Verify component usage matches design system patterns
- [ ] Check button hierarchy (single primary CTA per page/section)
- [ ] Validate spacing tokens and design system values
- [ ] Confirm color usage matches brand guidelines
- [ ] Check typography scale compliance
- [ ] Verify design system component variants used correctly

#### 2.5 Microcopy & Labels

- [ ] Verify labels accurately describe destinations/actions (not "Nearest" when meaning "Upcoming")
- [ ] Check instructions are clear and unambiguous (not "Type '/'" when meaning "Press /")
- [ ] Confirm empty states provide helpful guidance
- [ ] Review error messages for specificity and recovery options

#### 2.6 Technical Issues

- [ ] **Check browser console for JavaScript errors (MANDATORY):**
  - **REQUIREMENT:** Document console state BEFORE and AFTER interactions
  - Process:
    1. Open browser DevTools → Console tab
    2. Clear console
    3. Note: "Console cleared, starting with 0 errors"
    4. Interact with page (scroll, click buttons, open menus)
    5. Document: "After interactions: 3 errors, 2 warnings" with examples
  - Example finding: "Console shows: GET /api/tools failed (404) - impacts resource loading"
  - **Enforcement:** If no console state documented, you MUST check it
- [ ] Verify API calls succeed (check Network tab)
  - Look for 404, 500, timeout errors
  - Document: "Network tab shows 2 failed requests: /api/tools (404)" or "All requests successful"
- [ ] Test loading states appear and complete correctly
- [ ] Look for infinite spinners or broken UI states
- [ ] **Document reproduction steps for any bugs found:**
  - MUST include step-by-step instructions:
    - "1. Scroll to 50% page"
    - "2. Click menu icon in top right"
    - "3. Menu appears but overlaps content (z-index bug)"
  - Include screenshot reference or specific element selector
  - If NO bugs found, state: "No reproducible bugs detected during testing"

For each issue found, capture:

- `heuristic`: Nielsen heuristic name
- `issue`: What is wrong from a UX perspective
- `evidence`: Screenshot clue, UI text, interaction behavior, or user-provided detail
- `page` (if auditing multiple pages): Page name or ID (e.g., "Dashboard", "Checkout - Step 2", "Settings Page")
- `impact`: Who is affected and how task success is harmed
- `severity`: Use 0-4 scale below
- `recommendation`: Concrete change that can be implemented
- `effort`: Low, medium, or high
- `confidence`: High, medium, or low (based on evidence quality)

### 2.7 MANDATORY CHECK VALIDATION (BLOCKING CHECKPOINT)

**🚨 CRITICAL: Before proceeding to Step 3, verify ALL mandatory checks are complete.** If any are missing, STOP and complete them now.

- [ ] Keyboard navigation tested for **at least 10 Tab stops** (logical order and visible focus states)
- [ ] Console error state documented **before and after** interactions
- [ ] Heading hierarchy documented with **exact pixel sizes** (H1 > H2 > H3 > body)
- [ ] Entire page scrolled with sticky element behavior documented

**If ANY box above is unchecked, DO NOT PROCEED to Step 3. Complete the missing check first.**

---

### 3. Apply Severity Ratings

Use this scale consistently:

- `0` No usability problem
- `1` Cosmetic issue
- `2` Minor usability problem
- `3` Major usability problem
- `4` Usability catastrophe (urgent)

Severity should reflect frequency, impact, and persistence.

### 4. Prioritize Fixes

Group recommended fixes into:

- `Quick wins`: high impact, low effort
- `Planned improvements`: medium effort or moderate impact
- `Strategic redesign`: high effort, systemic issues

### 4.1 Ensure Comprehensive Issue Coverage

Verify your findings include diverse issue types:

**Visual/Layout Issues:**

- Spacing inconsistencies
- Sizing problems (too large/small elements)
- Hierarchy violations
- Alignment issues

> **Accessibility Issues** (contrast, ARIA, keyboard, focus indicators, missing labels) are covered by the **`designops-accessibility`** skill — run it alongside this audit for full coverage.

**Interaction Issues:**

- Unclear affordances (what's clickable)
- Poor hover/focus states
- Confusing microcopy
- Misleading labels

**Technical Issues:**

- Failed API calls
- Performance problems
- Loading state gaps
- Browser compatibility

**Design System Violations:**

- Incorrect component usage
- Button hierarchy violations
- Spacing token misuse
- Brand guideline violations

If any category has zero findings, explicitly re-examine that area before finalizing the report.

### 5. Generate the Report

**When filesystem and Node.js tooling are available** (i.e. the agent can create files and run scripts), load the `ux-report-generation` skill and follow its full workflow to produce the HTML and PDF deliverables:

```
Load: .github/skills/ux-report-generation/SKILL.md
```

Then follow every step in that skill exactly:

1. Capture and save screenshots for key findings.
2. Write the self-contained HTML report to `reports/ux-buddy/<app-name>-ux-audit-report.html`.
3. Write and run `generate-pdf.mjs` to produce `reports/ux-buddy/<app-name>-ux-audit-report.pdf`.
4. Confirm outputs with full file paths.

**When filesystem or Node.js tooling is unavailable** (e.g. screenshot-only or Figma-only runtimes without file access), deliver the full audit as a structured chat response using the same required sections. Explicitly state at the top: `Note: HTML/PDF report generation is not available in this environment. Full findings are presented below.`

Prefer on-disk deliverables when possible; the chat fallback is acceptable only when file creation is not supported.

The report must contain the following sections (per the ux-report-generation contract):

- **Scope and Assumptions**
- **Key Findings table** with columns: ID, Page (if multi-page), Heuristic, Issue, Evidence, Severity (0–4), Recommendation, Effort, Confidence
- **Prioritized Plan** (Quick wins / Planned improvements / Strategic redesign)
- **Confidence and Gaps**

**Note:** When auditing a single page, the Page column can be omitted. When auditing multiple pages or flows, always include the Page column to clearly identify where each issue occurs.

## Guardrails

- Do not invent user research results or implementation details.
- If evidence is weak, lower confidence and request missing artifacts.
- Separate observed issues from assumptions.
- Keep recommendations specific and testable.
- **When auditing multiple pages:** Always include page identifiers in the findings table to make it clear where each issue occurs. Use descriptive page names (e.g., "Dashboard", "Dev Resources Listing", "Resource Detail Page") rather than just URLs.

## Example Trigger Prompts

- "Run a Nielsen heuristic audit for our checkout flow."
- "Review these app screens for usability problems using Nielsen heuristics."
- "Give me a prioritized UX audit report with severity ratings."
- "Here are some screenshots — can you audit these for usability issues?"
- "Here's a Figma link — please do a UX audit: https://www.figma.com/design/..."
- "Audit this live URL: https://example.com"

## References

- `references/nielsen-heuristics-checklist.md`: Heuristic definitions, probing questions, and common failure signals.
- **`.github/skills/designops-accessibility/SKILL.md`**: Dedicated accessibility skill for WCAG 2.1/2.2 checks — contrast ratios, ARIA, keyboard accessibility, screen reader testing. Run alongside this audit for a complete review.

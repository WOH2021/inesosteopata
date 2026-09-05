# BMW Digital Accessibility Guidelines

> **Source**: [BMW IT Guideline — Digital Accessibility](https://atc.bmwgroup.net/confluence/x/4Zcqp) > **Standard**: WCAG 2.2, conformance level **AA** (levels A + AA)
> **Self Service / Human Escalation**: [BMW Accessibility Self Service](https://atc.bmwgroup.net/confluence/x/fKgrXQE)

---

## BMW Context

The **European Accessibility Act (EAA)**, EU Directive 2019/882, requires BMW Group to meet accessibility standards. EAA laws came into force across the EU on **28 June 2025**. **High-risk AI systems under the European AI Act**, including instructions for use for high-risk AI systems, must also be barrier-free; the EU AI Act references EAA criteria and is expected to come into force on **2 August 2026**. A company-wide Workers Agreement (Gesamtbetriebs- und Inklusionsvereinbarung) adds an internal obligation for employee-facing tools.

BMW references **WCAG 2.2** via the chain: EAA → BFSG/BFGSV (Germany) → EN 301 549 → WCAG. WCAG 2.2 was published in 2024; in the course of 2026, WCAG 2.2 requirements become mandatory for EAA compliance.

**Required conformance level: AA** — all success criteria from levels A and AA must be met.

Two application types must be accessible:

- **End-customer-facing** — check EAA scope via the [Accessibility Self Service](https://atc.bmwgroup.net/confluence/x/fKgrXQE)
- **Internal employee applications** — always in scope

---

## Audit Severity Taxonomy

Every finding in an accessibility audit **must** use one of these three severity labels exactly as written. Do not invent alternatives ("Low", "Medium", "High", "Info", etc.).

| Label      | When to use                                                                             |
| ---------- | --------------------------------------------------------------------------------------- |
| `CRITICAL` | Confirmed WCAG A or AA violation — blocks conformance; must be fixed before release     |
| `WARNING`  | Likely violation or a pattern that commonly causes failures in context; should be fixed |
| `ADVISORY` | Best-practice gap with no confirmed criterion failure; fix if time allows               |

Always open the finding list with the highest-severity items first.

---

## Hands-On Checklist

A quick entry-point. Passing all 6 areas alone does not make an app fully accessible — refer to the full criteria below.

| #   | Area                        | Key Rules                                                                                                                                                           | WCAG Criteria                              |
| --- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
| 1   | **Content**                 | Plain language; unique/meaningful element descriptions (no "Click here")                                                                                            | 3.1 Readable, 1.3.3                        |
| 2   | **Headings & Structure**    | Logical heading hierarchy (`<h1>` describes page purpose, no skipped levels); use landmark elements                                                                 | 1.3.1, 2.4.6, 2.4.1                        |
| 3   | **Controls & Keyboard Nav** | Full keyboard operability; `href` on all links; `<button>` for buttons; visible focus style; logical tab order; "Skip to main content" link; screen-reader coverage | 1.3.1, 2.1.1, 2.4.7, 2.4.3, 2.4.1          |
| 4   | **Images & Media**          | Meaningful `alt` or `alt=""` for decorative; no text in images; no autoplay without pause controls                                                                  | 1.1.1, 1.4.5, 2.2.2                        |
| 5   | **Appearance**              | Color contrast ≥ 4.5:1 (text), ≥ 3:1 (large text/UI); consistent layout; works at 200% zoom, inverted colors, mobile                                                | 1.4.3, 1.4.11, 3.2.3, 3.2.4, 1.4.4, 1.4.10 |
| 6   | **Code**                    | Valid HTML (W3C); correct `lang` attributes                                                                                                                         | 1.3.1, 3.1.1, 3.1.2                        |

---

## WCAG 2.2 AA Criteria

### Principle 1 — Perceivable

#### 1.1 Text Alternatives

**1.1.1 Non-text Content** (A)
All non-text content has a text alternative. Use appropriate `alt` per type:

- Decorative: `alt=""` — screen readers skip it
- Functional (logo, icon button): describe the function, not appearance
- Informative: describe what is most relevant
- Complex (charts, graphs): short alt + full data as text

```html
<img src="chart.png" alt="Q1 revenue up 12% year-on-year" />
<img src="divider.png" alt="" />
<!-- decorative -->
```

**Tool**: Lighthouse `1.1`

---

#### 1.2 Time-Based Media

**1.2.1 Audio-only / Video-only — Prerecorded** (A)
Provide a transcript for audio-only. Provide transcript (preferred) or audio description for video-only.

**1.2.2 Captions — Prerecorded** (A)
Synchronized captions for all prerecorded audio content. Use an accessible media player (e.g. Able Player).

**1.2.3 Audio Description or Media Alternative — Prerecorded** (A)
Describe visual-only content via audio description or text alternative. Satisfying 1.2.5 also satisfies this.

**1.2.4 Captions — Live** (AA)
Real-time captions for live audio content.

**1.2.5 Audio Description — Prerecorded** (AA)
Audio description for all prerecorded video.

---

#### 1.3 Adaptable

**1.3.1 Info and Relationships** (A)
Use semantic HTML so assistive technology understands structure. Where tech cannot convey relationships programmatically, describe them in text (e.g. "All required fields are marked with \*").

```html
<!-- Prefer semantic elements -->
<nav>
  ,
  <main>
    ,
    <header>
      ,
      <footer>
        ,
        <article>
          ,
          <section>
            <table>
              with
              <th scope="col|row">
                <form>with <label for="..."></label></form>
              </th>
            </table>
          </section>
        </article>
      </footer>
    </header>
  </main>
</nav>
```

**1.3.2 Meaningful Sequence** (A)
Reading order in the DOM matches the visual reading order. Do not reorder content purely via CSS.

**1.3.3 Sensory Characteristics** (A)
Do not reference UI by appearance or position alone: "Click the red button on the right" → "Click **Save** to continue."

**1.3.4 Orientation** (AA)
Content works in both portrait and landscape unless a specific orientation is essential.

**1.3.5 Identify Input Purpose** (AA)
Use HTML `autocomplete` attributes on common fields:

```html
<input type="text" autocomplete="name" />
<input type="email" autocomplete="email" />
```

---

#### 1.4 Distinguishable

**1.4.1 Use of Color** (A)
Color must not be the sole means of conveying information. Use text + symbols as additional cues. Required form fields: use `*` not just red color.

**1.4.2 Audio Control** (A)
No audio auto-plays for more than 3 seconds without a pause/stop/volume mechanism.

**1.4.3 Contrast — Minimum** (AA)

- Normal text: ≥ **4.5:1** against background
- Large text (≥ 18.5px bold or ≥ 24px regular): ≥ **3:1**
- Decorative / disabled elements: exempt
  **Tools**: Color Contrast Analyser, Contrast Grid

**1.4.4 Resize Text** (AA)
Text must be resizable up to 200% without assistive technology — no loss of content or functionality.

**1.4.5 Images of Text** (AA)
Avoid images that contain text. Exception: logos and brand names.

**1.4.10 Reflow** (AA)
No horizontal scrolling at viewport width equivalent to 320 CSS px (test: zoom to 400% at 1280px wide). Ensure viewport meta tag:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
```

**1.4.11 Non-text Contrast** (AA)
UI components and their states (e.g. focus ring, checkbox border, input outline) must have ≥ **3:1** contrast against adjacent colors. Inactive/disabled components exempt.

**1.4.12 Text Spacing** (AA)
Content must not lose information when the user overrides spacing to:

- Line height: 1.5× font size
- Paragraph spacing: 2× font size
- Letter spacing: 0.12× font size
- Word spacing: 0.16× font size

**1.4.13 Content on Hover or Focus** (AA)
Tooltips and similar hover/focus-triggered content must be:

- **Dismissible** — closable without moving focus/pointer (e.g. Esc)
- **Hoverable** — pointer can move over the triggered content without it disappearing
- **Persistent** — stays visible until the trigger is removed

---

### Principle 2 — Operable

#### 2.1 Keyboard Accessible

**2.1.1 Keyboard** (A)
All functionality must be operable via keyboard alone. No mouse-only interactions.

**2.1.2 No Keyboard Trap** (A)
Users must always be able to tab out of interactive components (e.g. modals must have a close mechanism reachable by keyboard).

**2.1.4 Character Key Shortcuts** (A)
Single-character keyboard shortcuts must be remappable, disableable, or only active on focus. Prefer `Ctrl+Key` combinations.

---

#### 2.2 Enough Time

**2.2.1 Timing Adjustable** (A)
When a time limit exists, users must be able to turn it off, adjust it (≥ 10× default), or extend it (≥ 20 s warning, ≥ 10 extensions). Exception: >20 h limits, real-time events, essential limits.

**2.2.2 Pause, Stop, Hide** (A)
Moving/blinking/scrolling content that auto-starts, runs in parallel, and lasts >5 s must have pause/stop/hide controls. Same for auto-updating content.

---

#### 2.3 Seizures and Physical Reactions

**2.3.1 Three Flashes or Below Threshold** (A)
Content must flash no more than 3 times per second. If faster, the flashing area must be < 341×256 px at 1024×768 reference resolution.
Prefer `prefers-reduced-motion` media query to suppress animations:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation: none;
    transition: none;
  }
}
```

---

#### 2.4 Navigable

**2.4.1 Bypass Blocks** (A)
Provide a "Skip to main content" link as the first focusable element. Use ARIA landmarks:

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
<header>
  ,
  <nav>
    ,
    <main id="main-content">
      ,
      <aside>
        ,
        <footer></footer>
      </aside>
    </main>
  </nav>
</header>
```

**2.4.2 Page Titled** (A)
Descriptive `<title>` per page — describes topic/purpose, not just app name:

```html
<title>User Profile — BMW Fleet Manager</title>
```

**2.4.3 Focus Order** (A)
Tab order matches visual reading flow (left-to-right, top-to-bottom). Hidden elements do not receive focus. Prefer DOM order over positive `tabindex`. Use `tabindex="-1"` to exclude, `tabindex="0"` to include.

**2.4.4 Link Purpose (In Context)** (A)
Link text (or link + surrounding context) describes the destination. Avoid "Click here", "Read more".

**2.4.5 Multiple Ways** (AA)
At least 2 ways to reach the same content: search + navigation, breadcrumbs + sitemap, etc.

**2.4.6 Headings and Labels** (AA)
Headings and form labels describe topic/purpose clearly.

**2.4.7 Focus Visible** (AA)
Every focusable element must have a visible focus indicator. Focus ring must have ≥ 3:1 contrast against background and must not be obscured. Do not use `outline: none` without a custom replacement.

```css
/* Never do this without a replacement */
:focus {
  outline: none;
}

/* Do this instead */
:focus-visible {
  outline: 2px solid #005bd3;
  outline-offset: 2px;
}
```

**Tools**: Silktide, Accessibility Insights for Web (BMW blueprint available)

**2.4.11 Focus Not Obscured** (AA)
Ensure the keyboard focus indicator is not entirely hidden by other content, such as cookie banners, toolbars, menus, or sticky overlays.

---

#### 2.5 Input Modalities

**2.5.1 Pointer Gestures** (A)
Multi-finger gestures (pinch-to-zoom, swipe) must have single-pointer alternatives (e.g. +/− buttons).

**2.5.2 Pointer Cancellation** (A)
Avoid triggering actions on `mousedown`/`pointerdown`. Use `click` (up-event) so users can cancel by moving the pointer away.

**2.5.3 Label in Name** (A)
The accessible name of a control must contain the visible label text. Speech input users say the visible label to activate a control.

```html
<!-- Bad: visible label "Search" but aria-label is "Search the site" -->
<button aria-label="Search the site">Search</button>

<!-- Good: accessible name contains visible label -->
<button aria-label="Search products">Search</button>
```

**2.5.4 Motion Actuation** (A)
Device motion (shake, tilt) must not be the only way to trigger actions. Users must be able to disable motion-based controls.

**2.5.7 Dragging Movements** (AA)
Drag-and-drop interactions must provide an equivalent non-dragging alternative, such as clickable or tappable “Up” and “Down” controls.

**2.5.8 Target Size** (AA)
Interactive targets such as buttons must be at least 24×24 CSS pixels unless layout constraints or available alternatives justify a smaller size. A smaller icon inside a larger clickable area satisfies this criterion.

---

### Principle 3 — Understandable

#### 3.1 Readable

**Key writing rules**:

- Short sentences; one thought per sentence
- No subordinate clauses or convoluted structures
- Familiar words; avoid jargon and abbreviations (explain if necessary)
- Active voice
- Numbers as digits ("5" not "five")
- Supplement text with images or pictograms

**3.1.1 Language of Page** (A)

```html
<html lang="en"></html>
```

**3.1.2 Language of Parts** (AA)
Mark inline content in a different language:

```html
<span lang="de">Willkommen</span>
```

---

#### 3.2 Predictable

**3.2.1 On Focus** (A)
Receiving focus must not trigger a context change (e.g. submitting a form, navigating away).

**3.2.2 On Input** (A)
Changing a form field value must not automatically change context unless the user is warned in advance. Avoid auto-submit, auto-navigate on select change.

**3.2.3 Consistent Navigation** (AA)
Navigation blocks repeated across pages appear in the same relative order on each page.

**3.2.4 Consistent Identification** (AA)
Components with the same function are labelled consistently across pages. Do not alternate "Read more" and "View details" for the same action.

**3.2.6 Consistent Help** (A)
Help mechanisms such as chat support, contact details, or FAQ/self-help links must appear in a consistent position across pages.

---

#### 3.3 Input Assistance

**3.3.1 Error Identification** (A)
Identify the field in error and describe the problem in text:

```html
<p role="alert">
  Email address is required and must be in the format name@example.com
</p>
```

**3.3.2 Labels or Instructions** (A)
Provide labels and format hints for all inputs:

```html
<label for="dob">Date of birth (DD/MM/YYYY)</label>
<input id="dob" type="text" autocomplete="bday" />
```

**3.3.3 Error Suggestion** (AA)
If the error type is known, suggest the correction.

**3.3.4 Error Prevention — Legal, Financial, Data** (AA)
For submissions with legal or financial consequences: make them reversible, check inputs before submission, or provide a confirmation step before finalising.

**3.3.7 Redundant Entry** (A)
Do not ask users to re-enter information they have already provided unless it is necessary, such as when security measures are affected or previously entered information is no longer valid.

**3.3.8 Accessible Authentication** (AA)
Authentication must not require significant cognitive effort, such as solving difficult puzzles, complex CAPTCHAs, or memorizing numbers. Provide an authentication method that avoids cognitive function tests, or provide assistance such as copy-paste support, Face ID, object recognition, or recognition of personal content provided by the user.

---

### Principle 4 — Robust

#### 4.1 Compatible

**4.1.1 Parsing** (removed in WCAG 2.2)
This criterion is no longer needed because assistive technologies no longer parse HTML directly, so it has been removed from WCAG 2.2.

**4.1.2 Name, Role, Value** (A)
Custom components must expose correct name, role, state, and value to assistive technology. Native HTML elements satisfy this when used correctly. For custom components use ARIA:

```html
<div
  role="checkbox"
  aria-checked="true"
  tabindex="0"
  aria-label="Accept terms"
></div>
```

See [ARIA Authoring Practices Guide](https://www.w3.org/WAI/ARIA/apg/).

**4.1.3 Status Messages** (AA)
Status changes that appear without focus movement must be announced via ARIA live regions:

```html
<div role="status" aria-live="polite">Form submitted successfully.</div>
<div role="alert" aria-live="assertive">Error: session expired.</div>
```

---

## Recommended Tools

| Tool                                                                                  | Use                                                                |
| ------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| [Lighthouse](https://developer.chrome.com/docs/lighthouse)                            | Automated a11y scan in DevTools / CI                               |
| [Accessibility Insights for Web](https://accessibilityinsights.io/docs/web/overview/) | Guided manual audit (BMW blueprint available)                      |
| [Silktide Accessibility Checker](https://silktide.com/)                               | Chrome extension for in-browser scanning (BMW blueprint available) |
| [Color Contrast Analyser](https://www.tpgi.com/color-contrast-checker/)               | Eyedrop-based contrast checking                                    |
| [Contrast Grid](https://contrast-grid.eightshapes.com/)                               | Preview color palette contrast matrix                              |
| `@axe-core/playwright`                                                                | Automated a11y assertion in Playwright tests                       |
| NVDA (Windows)                                                                        | Native screen reader for manual testing                            |
| VoiceOver (macOS)                                                                     | Native screen reader for manual testing                            |
| [Stark (Figma)](https://www.getstark.co/)                                             | Contrast & accessibility for design                                |
| [HTML Validator](https://validator.w3.org/)                                           | W3C HTML conformance check                                         |

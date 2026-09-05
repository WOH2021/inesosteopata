---
name: accessibility-audit-wcag
description: "Load the BMW IT Guideline - Digital Accessibility WCAG 2.2 AA reference before performing any accessibility audit or review. Use this skill for any accessibility question or task involving Angular or React front-end code. Also use when the topic includes: accessibility, a11y, WCAG, aria, aria-label, aria-live, role attribute, screen reader, keyboard navigation, keyboard trap, tab order, focus management, focus visible, focus ring, skip link, color contrast, alt text, axe, axe-core, semantic HTML, landmark, reflow, captions, audio description, EAA, European Accessibility Act, BFSG, accessible form, error announcement, status message, prefers-reduced-motion, pointer gesture, disabled users, low vision, BMW accessibility audit, IT Guideline Digital Accessibility."
metadata:
  version: "0.9.0"
  tags:
    - accessibility
    - a11y
    - wcag
    - aria
    - angular
    - react
    - bmw
  authors:
    - Maria Haas <Maria.Haas@bmw.de>
---

This skill provides deployment-safe access to BMW accessibility reference documentation.
**Always load `./references/bmw-guidelines.md` before starting any audit** — it contains
the BMW-specific criteria, hands-on checklist, and recommended tooling that must inform
every finding. If `./references/bmw-guidelines.md` cannot be loaded, inform the developer
that the BMW reference document is unavailable and pause the audit until it is accessible.
Do not proceed with findings based solely on generic WCAG knowledge.

## Knowledge Index

| Topic                                                                              | Reference                                                                                                                  |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| BMW WCAG 2.2 AA requirements, full criteria, hands-on checklist, recommended tools | [./references/bmw-guidelines.md](./references/bmw-guidelines.md)                                                           |
| Official Link to the EU AI ACT                                                     | [https://ai-act-service-desk.ec.europa.eu/en/ai-act-explorer](https://ai-act-service-desk.ec.europa.eu/en/ai-act-explorer) |
| Official WCAG 2.2 Guidelines                                                       | [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/)                                           |

## Gotchas

- **BMW mandates WCAG 2.2 AA (levels A + AA)** — do not enforce AAA criteria unless the developer explicitly requests it. Applying AAA requirements creates incorrect findings and erodes trust in the audit.
- **EAA scope and legal interpretation must be escalated** — do not attempt to determine whether a product falls under the European Accessibility Act or BFSG. Direct the developer to the [BMW Accessibility Self Service](https://atc.bmwgroup.net/confluence/x/fKgrXQE).
- **Advisory only** — this agent reads and audits; it never edits files. Every finding is a recommendation; the developer decides priority and timing.

# UX Copy Review Report Template

Use this template when delivering a comprehensive UX copy review.

## 1. Executive Summary

Include:

- Feature or page reviewed and URL
- Review date and reviewer
- Overall compliance score
- Top critical findings
- Overall recommendation

## 2. Summary Metrics Dashboard

Include:

- Scores by category (for example Density compliance, UX writing quality, accessibility)
- Issue count by severity (Critical, High, Medium, Low)
- Issues by category (clarity, conciseness, tone, consistency, accessibility)

Example:

```markdown
Overall Scores:

- Density Compliance: 6.0/10
- UX Writing Quality: 7.0/10
- Accessibility: 6.5/10

Issues Found: 18 total

- Critical: 5
- High: 6
- Medium: 7
- Low: 0
```

## 3. What Is Working Well

Include 3 to 5 positive findings with short rationale.

## 4. Critical Issues

For each issue, provide:

- Current text
- Violated guideline
- Impact
- Recommended fix

Example:

```markdown
**Issue Title**

- Current: "Click here"
- Violation: Descriptive link text guideline
- Impact: Ambiguous action for screen reader users
- Fix: "Download report"
```

## 5. Detailed Findings by Section

Organize by sections (for example Navigation, Hero, Forms) or by copy type (Buttons, Errors, Empty States).

Each finding should include:

- Context
- Issue
- Fix
- Severity (Critical, High, Medium, Low)

## 6. Quick Wins

List high-impact, low-effort changes with estimated effort and expected impact.

## 7. Before and After Examples

Show side-by-side improvements and impact statement.

Example:

```markdown
Before (50 words): ...
After (20 words): ...
Impact: 60 percent shorter and easier to scan.
```

## 8. Prioritized Action Plan

Provide phased plan (for example This sprint, Next sprint, Ongoing) or priority levels (P0, P1, P2).

## 9. Compliance Checklist

Use a table with pass, partial, fail by guideline.

Example:

```markdown
| Guideline     | Status  | Notes                          |
| ------------- | ------- | ------------------------------ |
| Conciseness   | Partial | Copy too long in hero section  |
| Sentence case | Fail    | All caps heading in onboarding |
| Active voice  | Pass    | Most actions use direct verbs  |
```

## 10. Next Steps

Include:

- Immediate actions
- Owners or reviewers
- Re-audit timing
- Success criteria

## Severity Reference

- Critical (P0): Accessibility or core brand violations that block release
- High (P1): Significant UX impact and should be fixed before release
- Medium (P2): Important clarity improvements for near-term iteration
- Low (P3): Polish and consistency improvements

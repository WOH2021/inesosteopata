---
name: ux-writing
description: Write clear, concise, and helpful interface copy that guides users and reinforces the product voice. Use when writing UI text (buttons, labels, errors, success messages, tooltips, empty states, onboarding), improving existing copy, conducting content audits, or ensuring consistency with Density voice and tone guidelines. Also use for microcopy, form validation messages, calls-to-action, navigation labels, placeholder text, and inline help.
license: Proprietary
compatibility: Works with text-based interfaces, design files, and code components; no special tools required.
metadata:
  author:
    - Adele Campbell <Adele.Campbell@bmwithub.co.za>
  version: "1.0.0"
  tags:
    - ux-writing
    - microcopy
    - content-design
    - voice-and-tone
    - density
---

# ux-writing

## Goal

Produce clear, concise, and user-centered interface copy that aligns with Density voice and tone guidelines and follows UX writing best practices.

## Inputs

Gather as many of these as available:

- **Context**: Component type (button, error message, tooltip, empty state, etc.)
- **Artifacts**: Screenshots, Figma links, recordings, descriptions
- **User goal**: What the user is trying to accomplish
- **Tone**: Required tone (informative, encouraging, warning, error, success)
- **Constraints**: Character limits, localization needs, accessibility requirements
- **Brand guidelines**: Specific Density voice and tone requirements
- **Existing copy**: Text to review or improve

If inputs are incomplete, ask clarifying questions before generating copy.

## Outputs

Deliver interface copy that is:

1. **Clear**: Users understand immediately without confusion. Say exactly what you mean. No jargon, no ambiguity, no fluff.
2. **Concise**: No unnecessary words; respects user attention. Use the fewest words that convey the full meaning.
3. **Helpful**: Guides users toward successful completion
4. **Consistent**: Same terms for the same things everywhere. Matches Density voice and tone.
5. **Accessible**: Works for all users, including those using assistive technologies.
6. **Human**: Write like a helpful person, not a machine.

Include rationale explaining copy choices when requested.

## Steps

### 1. Understand Context and User Need

- Identify the interface element type and its purpose
- Clarify the user's goal at this moment in the journey
- Determine appropriate tone based on context (neutral, encouraging, warning, etc.)
- Note any technical constraints (character limits, platform, localization)

### 2. Review Density Voice and Tone Guidelines

Before writing, review the appropriate reference files to ensure alignment with BMW Density guidelines:

- `references/density-voice-and-tone.md` - Core voice, tone, characteristics, and perspective
- `references/density-numerics.md` - Date, time, number, phone, currency formatting
- `references/density-text.md` - Spelling, capitalization, punctuation, gendering
- `references/density-error-messages.md` - Error message principles
- `references/density-action-labels.md` - Standardized UI action labels
- `references/density-imprint.md` - Legal and contact information requirements

### 3. Apply UX Writing Best Practices

Consult `references/copy-patterns.md` for proven patterns for:

- Buttons and calls-to-action
- Error and validation messages
- Success and confirmation messages
- Empty states
- Tooltips and helper text
- Placeholders
- Navigation labels
- Onboarding and first-use experiences

### 4. Write User-Centered Copy

Follow these principles:

**Clarity over cleverness**

- Use simple, familiar words
- Avoid jargon unless it's industry-standard and users expect it
- Be specific rather than vague
- Front-load important information

**Brevity**

- Remove filler words ("please", "kindly", "simply")
- Use active voice
- One idea per sentence
- Cut redundant phrases

**Helpfulness**

- Tell users what happened and why
- Provide clear next steps
- Anticipate and address user concerns
- Never blame the user

**Consistency**

- Use the same term for the same concept throughout
- Match tone to context appropriately
- Follow established patterns users have learned

**Accessibility**

- Write descriptive link text (not "click here")
- Provide context in error messages
- Use sentence case for readability
- Ensure color is not the only way to convey information

### 5. Format and Present Options

When presenting copy options:

1. Provide 2-3 variations when appropriate
2. Label each option with context (character count, tone, use case)
3. Include a rationale for the recommended option
4. Note any accessibility or localization considerations

Example format:

```markdown
## Button Label

**Recommended:** "Save changes"

- Character count: 12
- Tone: Neutral, clear action
- Rationale: Specific action verb + what's being saved

**Alternative:** "Save"

- Character count: 4
- Tone: Minimal
- Rationale: Works when context is clear; use when space is critical

**Avoid:** "Submit"

- Rationale: Vague; doesn't specify what happens next
```

### 6. Review Against Checklist

Before finalizing, verify:

- [ ] Clear and immediately understandable
- [ ] Concise without sacrificing clarity
- [ ] Helpful and action-oriented
- [ ] Consistent with Density voice and tone
- [ ] Accessible to all users
- [ ] Respects character limits and constraints
- [ ] Appropriate tone for context
- [ ] No jargon or ambiguous terms
- [ ] Specific rather than vague
- [ ] Provides clear next steps when needed

### 7. Provide Localization Notes (if applicable)

When writing for international audiences, include:

- Terms that should not be translated
- Cultural considerations
- Character expansion estimates for other languages
- Idioms or expressions that don't translate well

## Common Copy Types

### Buttons and CTAs

- Use verb + noun format: "Create account", "Save changes", "Cancel order"
- Be specific about the action and outcome
- Keep under 25 characters when possible
- Match button prominence to action importance

### Error Messages

- State what went wrong clearly
- Explain why (if it helps the user)
- Provide a clear path to resolution
- Never blame the user
- Use a helpful, reassuring tone

Template: `[What happened] [Why it matters] [What to do next]`

### Success Messages

- Confirm the action was completed
- Be brief but warm
- Provide next steps if relevant
- Use positive, encouraging tone

### Empty States

- Acknowledge the current state
- Explain why it's empty
- Provide clear call-to-action to add content
- Use encouraging, helpful tone

### Tooltips and Helper Text

- Provide additional context without repeating visible labels
- Keep under 2 sentences
- Only include if truly helpful
- Don't state the obvious

### Placeholders

- Show format or example, not instructions
- Use realistic examples
- Keep brief
- Don't replace labels

### Form Labels and Validation

- Use sentence case
- Be specific and descriptive
- Mark required fields clearly
- Provide inline validation with helpful messages
- Position labels above fields for accessibility

## Voice and Tone Principles

### Density Voice

The Density design system embodies BMW brand values. Key characteristics:

- **Professional yet approachable**: Not stiff or overly casual
- **Confident without arrogance**: Assured but humble
- **Precise and clear**: No ambiguity or unnecessary complexity
- **User-focused**: Always serving the user's needs and goals

For complete guidelines, see:

- `references/density-voice-and-tone.md` - Core voice and tone principles
- `references/density-text.md` - Text formatting and style
- `references/density-numerics.md` - Number and date formatting

### Tone Adaptation

Adjust tone based on context while maintaining consistent voice:

**Informational** (neutral, clear)

- Feature descriptions
- Settings labels
- Navigation elements

**Encouraging** (positive, supportive)

- Onboarding
- Empty states
- First-time user experiences
- Success messages

**Urgent** (direct, action-oriented)

- Warnings before destructive actions
- Time-sensitive notifications
- Critical errors

**Empathetic** (understanding, helpful)

- Error states
- Recovery flows
- Help and support content

## Examples

### Before and After Improvements

**Button - Before**: "Click here"
**Button - After**: "Download report"
_Rationale: Specific action, describes outcome, accessible_

**Error - Before**: "Invalid input"
**Error - After**: "Email must include '@' symbol"
_Rationale: Specific problem, clear fix, helpful_

**Empty State - Before**: "No items"
**Empty State - After**: "No projects yet. Create your first project to get started."
_Rationale: Contextual, encouraging, provides action_

**Tooltip - Before**: "This is the username field"
**Tooltip - After**: "Must be 3-20 characters, letters and numbers only"
_Rationale: Provides useful constraints, not obvious information_

## Resources

- **Voice and Tone**: See `references/density-voice-and-tone.md` for BMW Density voice, tone, and characteristics
- **Numerics**: See `references/density-numerics.md` for date, time, number, phone, and currency formatting
- **Text**: See `references/density-text.md` for spelling, capitalization, punctuation, and gendering
- **Error Messages**: See `references/density-error-messages.md` for error message principles
- **Action Labels**: See `references/density-action-labels.md` for standardized UI action labels (English/German)
- **Imprint**: See `references/density-imprint.md` for legal and contact information requirements
- **Copy Patterns**: See `references/copy-patterns.md` for component-specific examples and templates
- **External Resources**:
  - Content Design book by Sarah Richards
  - Nielsen Norman Group UX Writing articles
  - Material Design writing guidelines
  - Apple Human Interface Guidelines

## When NOT to Use This Skill

This skill focuses on interface microcopy. For these scenarios, consider other approaches:

- **Long-form content** (articles, documentation): Use standard content writing practices
- **Marketing copy**: Follow marketing team guidelines
- **Legal text**: Work with legal team
- **Technical documentation**: Use documentation style guide
- **API responses**: Follow API design patterns

## Quality Standards

All copy must meet these standards:

1. **Readability**: 8th-grade reading level or lower (use Hemingway Editor or similar)
2. **Scannability**: Front-load key information
3. **Actionability**: Include clear next steps when appropriate
4. **Consistency**: Match existing patterns and terminology
5. **Accessibility**: Screen reader friendly, meaningful without visual context

## Testing Your Copy

Validate copy effectiveness by:

1. **Read aloud test**: Does it sound natural?
2. **Out-of-context test**: Is it clear without surrounding UI?
3. **Scan test**: Can users get key info in under 3 seconds?
4. **Accessibility test**: Does it work with a screen reader?
5. **Translation test**: Will it work in other languages?

## UX Copy Review Report Structure

When conducting a UX copy audit or review, use a structured format that includes:

1. Executive summary and recommendation
2. Metrics dashboard (scores and issue counts)
3. Positive findings
4. Critical issues with current text, impact, and fix
5. Prioritized action plan with quick wins
6. Before/after examples and next steps

For the complete template, severity model, and examples, see:

- `references/ux-copy-review-report-template.md`

## Collaboration

When working with others:

- **Designers**: Ensure copy fits layout and visual hierarchy
- **Developers**: Confirm technical feasibility and character limits
- **Product**: Align on user flows and business goals
- **Localization**: Provide context for translators
- **Accessibility**: Test with assistive technologies

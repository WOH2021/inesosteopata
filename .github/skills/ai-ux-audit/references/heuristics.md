# AI UX Heuristics Framework — 6 Groups, 19 Heuristics

Work through each group and heuristic. Per heuristic: score each checklist item, calculate health, note findings.

---

## GROUP 1 — Trust & Understanding

> Build user confidence through transparency and appropriate expectations.

### Heuristic 1.1 — Make AI Reasoning Visible and Understandable

Users should understand what the AI can do, how it works, and why it made specific decisions.

- [ ] Does the AI show sources or cite evidence when making claims?
- [ ] Is there a visible confidence or certainty indicator on outputs?
- [ ] Are AI processing steps shown (e.g. "searching…", "analysing…")?
- [ ] Can users trace why the AI gave a specific answer?
- [ ] Are uncertainty caveats present on low-confidence outputs?

**Owners:** Product defines output types requiring citation · Design creates confidence tier components · Dev includes confidence score metadata in outputs

---

### Heuristic 1.2 — Balance Personality with Realistic Expectations

Give AI human-like qualities without misleading users about feelings, memory, or capabilities.

- [ ] Does the AI avoid claiming feelings, emotions, or personal experiences?
- [ ] Is memory scope clearly communicated (e.g. "I don't retain previous conversations")?
- [ ] Does the AI use warm language without implying sentience?
- [ ] Are capability limits disclosed proactively, not only on failure?
- [ ] Is there a personality guideline document AI copy follows?

**Owners:** Product writes personality brief with tone guardrails · Design creates session-start UI patterns · Dev implements system prompts preventing emotion/memory claims

---

### Heuristic 1.3 — Build Appropriate Trust Levels

Users should trust AI appropriately — neither blindly over-relying nor dismissing useful outputs.

- [ ] Are high-stakes outputs (medical, financial, legal) flagged with a verification prompt?
- [ ] Does the UI differentiate high-confidence from low-confidence outputs visually?
- [ ] Is there onboarding content explaining when to trust vs. verify?
- [ ] Are AI errors acknowledged clearly, not silently corrected?
- [ ] Is there a mechanism for users to report incorrect outputs?

**Owners:** Product defines high-stakes categories · Design creates visual trust tiers · Dev builds confidence thresholds triggering UI states

---

### Heuristic 1.4 — Help Users Understand How to Interact

Users should quickly understand what inputs the AI accepts, how to phrase requests, and what outputs to expect.

- [ ] Is there a visible prompt guide or example prompts on first use?
- [ ] Does the AI recover gracefully from unclear or ambiguous inputs?
- [ ] Is the input interface labelled with accepted formats (text / voice / file / image)?
- [ ] Does the AI clarify what it needs when a request is incomplete?
- [ ] Is there a capability overview accessible from within the product at any time?

**Owners:** Product defines capability taxonomy · Design creates onboarding prompts and input affordances · Dev handles input validation and clarification flows

---

## GROUP 2 — User Empowerment & Control

> Humans stay in charge; AI assists but never overrides.

### Heuristic 2.1 — Keep Humans in Control

Users must be able to override, modify, or reject any AI decision — especially before irreversible actions.

- [ ] Can users override or reject any AI recommendation before it is actioned?
- [ ] Are irreversible AI actions gated behind a confirmation step?
- [ ] Is there a visible undo or rollback option after AI-initiated changes?
- [ ] Can users pause or stop an AI process mid-execution?
- [ ] Is there a reversibility matrix defining which actions require approval?

**Owners:** Product maintains reversibility matrix · Design creates confirmation dialog patterns · Dev gates destructive API calls behind confirmation states

---

### Heuristic 2.2 — Enable Improvement from User Input

The system should actively respond to user corrections and feedback — not just passively receive it.

- [ ] Is there a visible and accessible feedback mechanism on AI outputs?
- [ ] Does the AI adapt within a session based on user corrections?
- [ ] Is there a feedback loop to Product/Dev from submitted corrections?
- [ ] Are users informed that their feedback improves the system?
- [ ] Can users edit or regenerate an unsatisfactory AI output?

**Owners:** Product defines feedback taxonomy and routing · Design creates thumbs up/down and regeneration patterns · Dev builds feedback ingestion pipeline

---

### Heuristic 2.3 — Enable Diverse Input and Output Methods

The AI should accommodate a range of interaction styles, devices, input types, and user abilities.

- [ ] Does the product support at least two input modalities (e.g. text + voice or text + file upload)?
- [ ] Are AI outputs available in more than one format (e.g. summary + detail, text + visual)?
- [ ] Is the interface accessible to screen reader users (WCAG 2.2 AA minimum)?
- [ ] Does the product support RTL languages if serving MENA or APAC markets?
- [ ] Are input format error messages present to guide users to the correct format?

**Owners:** Product defines input/output modality roadmap · Design runs WCAG 2.2 compliance audit · Dev implements input normalisation pipeline

---

## GROUP 3 — System Communication

> The AI explains itself clearly at every step.

### Heuristic 3.1 — Visible System Status

Users should always know what the AI is doing, how long it will take, and whether it succeeded or failed.

- [ ] Is there a loading/processing indicator for all AI operations over 1 second?
- [ ] Are multi-step processes broken into visible stages ("Step 2 of 4: Analysing…")?
- [ ] Is a success state clearly communicated after each AI task completes?
- [ ] Is system capability status visible (e.g. rate limits, degraded mode)?
- [ ] Are long operations cancellable with a visible stop control?

**Owners:** Product defines SLA thresholds for status indicators · Design creates progress and status component set · Dev emits progress events streamed to frontend

---

### Heuristic 3.2 — Handle Uncertainty and Errors Elegantly

When the AI doesn't know something or can't complete a task — it should say so clearly and offer a next step.

- [ ] Does the AI distinguish between "I don't know" and "I made an error"?
- [ ] Are error messages in plain language (not technical codes)?
- [ ] Does every error state offer a clear next action (retry, rephrase, contact support)?
- [ ] Is fallback content available when the AI cannot generate a valid response?
- [ ] Has every error state been copy-reviewed and UX-tested?

**Owners:** Product owns error taxonomy · Design creates error state component library · Dev classifies error types and maps to UI states

---

### Heuristic 3.3 — Maintain Coherent AI Character

The AI should have a consistent personality, tone, and communication style across sessions, features, and edge cases.

- [ ] Is there a documented tone of voice guide for all AI-generated copy?
- [ ] Is tone consistent across product surfaces (onboarding, errors, help)?
- [ ] Does the AI avoid switching registers unexpectedly (formal → casual)?
- [ ] Is personality consistent under stress or edge-case inputs?
- [ ] Are regular tone audits conducted across AI outputs?

**Owners:** Product maintains tone of voice document · Design reviews all AI-generated copy touchpoints · Dev applies consistent system-level prompts across all model calls

---

## GROUP 4 — Personalisation & Context

> The AI adapts without overstepping.

### Heuristic 4.1 — Adapt to User Context and Situation

The AI should recognise and adapt to the user's current situation without requiring explicit configuration.

- [ ] Does the AI adjust response length based on request complexity?
- [ ] Does the product adapt to device context (mobile vs. desktop)?
- [ ] Does the AI recognise user expertise level and adjust language accordingly?
- [ ] Is session context used to improve later responses?
- [ ] Can users set or update personalisation preferences?

**Owners:** Product defines context signals used in inference · Design creates preference settings and adaptive layout patterns · Dev passes context object (device, user tier, history) to every inference call

---

### Heuristic 4.2 — Reveal Features as Users Are Ready

Introduce advanced AI capabilities progressively — surfacing complexity only when users demonstrate readiness.

- [ ] Is onboarding limited to core features only?
- [ ] Are advanced features hidden by default and revealed based on usage signals?
- [ ] Is there a contextual tooltip or hint system surfacing relevant features at the right moment?
- [ ] Does the product have a defined progressive disclosure framework?
- [ ] Are power-user features accessible without cluttering the default UI?

**Owners:** Product defines feature reveal triggers and usage thresholds · Design creates contextual disclosure patterns · Dev tracks usage and triggers reveal conditions

---

### Heuristic 4.3 — Respect User Time and Attention

AI outputs should be appropriately concise — not padded for thoroughness, not truncated when completeness matters.

- [ ] Have default response lengths been validated against user expectations?
- [ ] Does the AI offer "summarise" or "expand" options on long outputs?
- [ ] Are notifications and AI interruptions minimised by default?
- [ ] Does the AI avoid repeating information the user has already confirmed?
- [ ] Has response length been tested across user segments and contexts?

**Owners:** Product sets response length SLAs per use case · Design tests response density in usability sessions · Dev tunes model prompts for appropriate verbosity

---

## GROUP 5 — Ethics & Responsibility

> The AI treats everyone fairly and handles data honestly.

### Heuristic 5.1 — Make Data Handling Transparent

Users should see exactly what data the AI uses, why, and how long it is retained — in plain language, not buried in legal text.

- [ ] Is there a plain-language data usage summary (not just a privacy policy link)?
- [ ] Do users know if their data is used to train the AI model?
- [ ] Is consent obtained before using personal data for personalisation?
- [ ] Can users view what data the AI currently holds about them?
- [ ] Is a data retention timeline communicated clearly in the product?

**Owners:** Product owns data transparency narrative · Design creates data dashboard and consent UI patterns · Dev maintains audit log of data usage per user

---

### Heuristic 5.2 — Avoid Bias and Ensure Fairness

The AI should actively identify and reduce bias in outputs — and communicate this work when relevant.

- [ ] Has the model been tested for demographic, linguistic, and cultural bias?
- [ ] Are bias test results documented and accessible internally?
- [ ] Is there a mechanism for users to flag biased or unfair outputs?
- [ ] Are fairness metrics included in the CI/CD pipeline?
- [ ] Is there a bias disclosure visible for outputs in high-stakes domains?

**Owners:** Product defines fairness criteria by use case · Design creates bias disclosure and flagging patterns · Dev integrates fairness metrics into CI/CD

---

## GROUP 6 — Security & Privacy

> User data is protected, and users know it.

### Heuristic 6.1 — Data Collection — Minimum Necessary

Collect only data genuinely needed for the AI to function — and make this visible to users as a trust signal.

- [ ] Has a data minimisation audit been conducted in the last 12 months?
- [ ] Are data collection purposes documented and enforced at the development level?
- [ ] Does the onboarding flow explain what data is collected and why?
- [ ] Are optional data fields clearly marked as optional (not pre-ticked)?
- [ ] Is data collection reviewed before each new feature launch?

**Owners:** Product approves data collection scope per feature · Design labels optional fields and shows collection rationale · Dev implements purpose-limited data storage

---

### Heuristic 6.2 — Transparency — Inform About Incidents

If a data breach, model failure, or significant AI error occurs — users must be informed promptly and clearly.

- [ ] Is there a documented incident response and user notification process?
- [ ] Have notification templates been prepared for common incident types?
- [ ] Are regulatory notification timelines documented and owned?
- [ ] Is there a status page or equivalent for system incidents?
- [ ] Has the incident communication process been tested in a drill?

**Owners:** Product owns incident communication plan · Design creates incident notification UI patterns · Dev maintains status page and alert infrastructure

---

### Heuristic 6.3 — Security and Data Protection

Implement strong technical data protection — and make evidence of that protection visible to users when they need reassurance.

- [ ] Is all data encrypted in transit (TLS 1.2+) and at rest (AES-256 or equivalent)?
- [ ] Are sensitive actions gated behind step-up authentication?
- [ ] Is training data anonymised by default before use in model improvement?
- [ ] Are security status indicators visible at points of sensitive data entry?
- [ ] Has a third-party penetration test been conducted in the last 12 months?

**Owners:** Product defines sensitive action list · Design adds security indicators at key UI moments · Dev implements TLS 1.3, AES-256, and anonymisation pipeline

---

### Heuristic 6.4 — Privacy Best Practices

Implement privacy-by-design throughout — from architecture to interface.

- [ ] Are the most privacy-protective settings the defaults (not opt-in)?
- [ ] Is account and data deletion accessible within 3 taps from any main screen?
- [ ] Is deletion completed within 30 days and confirmed to the user?
- [ ] Is there a Privacy Impact Assessment (PIA) process for new AI features?
- [ ] Is there a data flow diagram maintained for the current product architecture?

**Owners:** Product runs PIA for every new AI feature · Design places data deletion in primary settings · Dev implements hard-delete pipeline with 30-day SLA

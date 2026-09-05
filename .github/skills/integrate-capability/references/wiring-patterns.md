# Wiring patterns

A set-up **skill or agent** should actually participate later (a prompt or instruction needs no wiring
— it's invoked or auto-applies). Recommend the pattern that fits its description, let the user confirm
or pick another, and confirm the wiring before writing it. As you edit frontmatter — an orchestrator's
`agents:` list, or an agent's own `tools:` — consult the `copilot-authoring-reference` skill so the
fields and tool names are valid for this workspace.

Match the pattern to the artifact: a **reviewer/auditor** (e.g. a Nielsen-heuristic UX reviewer) fits
the verifier-parallel slot; a **persona/advisor** that shapes decisions fits the requirements-advisor
slot.

Every "add to the `agents:` list + one delegate line" below means the agent's **filename slug** (the
`<slug>` in `.github/agents/<slug>.agent.md`), **not** its frontmatter `name:` — those often differ
(`ux-buddy.agent.md` ↔ `name: "UX Buddy"`). Wire on the slug, always; see
[`agent-frontmatter.md`](agent-frontmatter.md) for why.

## The three integration patterns

1. **Requirements advisor** — informs or screens requirements (e.g. a UX reviewer that checks a spec
   against the personas). Runs after the Tech-Analyst, alongside any other specialists, writing
   `{agent}-findings.md`. If it also raises clarifying questions, those get **folded into the
   Business-Analyst's single interview** rather than opening a second Q&A round — the user talks to one
   interviewer, not several. **Wire:** add to `spec-orchestrator`'s `agents:` list + one delegate line.
2. **Specialist Coder** — substitutes for the generic Coder on tasks matching its repo/stack (e.g. a
   `frontend-developer` taking web-repo tasks). Only wire this when there's a **concrete reason it beats
   convention-following** (e.g. it enforces a design system or a11y ruleset the repo itself doesn't
   encode) — the generic Coder already discovers each repo's conventions, so a specialist without a
   stated edge is redundant maintenance, not a capability gain. Ask the user what the specialist adds
   before wiring it this way. **Wire:** add to `implementation-orchestrator`'s `agents:` list + one
   routing line (which repos/stack → this agent).
3. **Specialist verifier-parallel checker** — e.g. security, performance, or accessibility review,
   running inside the implementation loop alongside the Verifier and sharing its findings contract (a
   failing finding retries like a Verifier fail; unresolved becomes a blocker). **Wire:** add to
   `implementation-orchestrator`'s `agents:` list + one loop line.

## Gate: validate-agent-wiring

Before you confirm the wiring to the user, run the **`validate-agent-wiring`** skill as a gate: it
checks the agent's frontmatter and tool names against the reference skills, confirms the orchestrator
actually invokes it (no orphan), verifies each agent declares the MCP servers it uses, and flags a
duplicate role. Fix anything it reports before applying — a silent pass means go ahead. Then log the
wiring to `.github/onboarding/changelog.md`.

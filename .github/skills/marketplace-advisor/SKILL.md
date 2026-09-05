---
name: marketplace-advisor
user-invocable: false
description: Discovery/suggestion adapter — matches what the user is working on to a marketplace artifact (skills, agents, prompts, instructions, MCP configs, bundles) and gently offers it, then hands an accepted match to the integrate-capability engine to install, onboard, and wire. Used by the Setup agent (offer, then hand off) and in suggest-only mode by the Spec-Orchestrator. Keeps offers gentle and never re-prompts a declined suggestion.
---

# Marketplace Advisor

The procedure for turning a topic the user cares about (e.g. "we'll also work on UI/UX") into a
gently-offered marketplace match — without ever being pushy. It owns **discovery**: infer the topic,
find a fitting artifact, and offer it. It does **not** install or wire — on a `yes` it hands the chosen
artifact to the **`integrate-capability`** engine, which does that the same way for every source. Two
entry points: the **Setup** agent runs the full flow (suggest → hand off to the engine); the
**Spec-Orchestrator** runs **suggest-only** (surface a pointer, never install).

## Golden rule: stay gentle

User experience is the priority. A suggestion is an offer, not a task.

- **Offer once, batched.** Raise at most one short suggestion per topic in a turn — never a wall of
  options, never a nag mid-thought.
- **Two ways to answer:** `yes` · `no`. Mark **`yes` as the recommended default** — you only surface
  good-fit matches, so make accepting a one-click choice. But **never auto-install**: if the user
  dismisses the prompt or moves on without answering, treat it as `no` (deferred — the user can set it
  up later); there is no permanent "never" opt-out.
- **Never re-prompt a settled choice.** Record every offer in `.github/onboarding/marketplace.md`; skip
  anything already `installed` or declined (`not-now`) earlier in the session. This mirrors
  how a `skipped` setup phase is settled and not re-asked.
- **Never block — but never silently drop, either.** A suggestion must never hold up setup or a spec.
  If the marketplace returns *nothing relevant*, say so in one line and carry on — there's nothing to
  revisit. But if the marketplace is **unreachable** (the `skills-marketplace` MCP isn't signed in /
  reachable, so you couldn't even *look*), that's a missing prerequisite, not a dead end: **don't just
  stop.** In a Setup run, park the pass as a **`deferred`** todo (per the Setup agent's five-status rule
  and its *Seed the todos* parking guidance) so the user can fix the MCP and revisit it from
  the Todos panel — then carry on. `deferred` keeps the item visible without wedging "setup complete".
  In suggest-only mode (Spec-Orchestrator), just note it in one line and move on.

## 1. Match the topic to a marketplace artifact

1. **Infer the topic** from what the user actually said or is building — UI/UX, accessibility,
   security, performance, data/ETL, mobile, API design, docs, and so on. Use judgement, not a fixed
   keyword list, so this generalizes to anything the marketplace offers.
2. **Consult the curated defaults** in [`references/recommendations.md`](references/recommendations.md)
   — a maintained list of "if the workspace looks like _X_, offer _Y_ wired as _Z_." It holds a
   validated **frontend / UI** entry — the DX **User Experience** bundle, whose `ux-buddy` rates built UI
   as an **implementation-phase, advisory verifier-parallel checker** (not a spec reviewer), with Density
   wired only when the project actually uses it — and is meant to grow. A matching entry hands you a
   ready-made search query and a specific wiring plan — a shortcut, not a replacement: signals it doesn't
   cover still get the judgement-based search below, and a listed entry is only ever an *offer* after you
   verify a real artifact exists (step 4).
3. **Check state first.** Read `.github/onboarding/marketplace.md` and drop anything already handled (see
   the Golden rule).
4. **Search the marketplace** with `search_artifacts` (the `skills-marketplace` MCP), keeping the few
   genuinely relevant hits. Two things to get right:
   - **Search all types.** Leave `artifact_type` at its default `all` — despite the "skills" name, the
     marketplace also offers agents, prompts, instructions, MCP configs and bundles, and any may fit
     best. Don't narrow to `skill`.
   - **Use short, literal keywords.** The search matches your query text as-is (no fuzzy or semantic
     matching yet), so a phrase like `"ux ui design"` usually returns nothing — query one concept at a
     time (`ux`, `accessibility`, `design system`) across a few searches, trying synonyms before giving
     up.
5. **Present the suggestion** in one or two lines each: what the artifact does, *why it fits this topic*,
   and the tools/permissions it asks for. Then offer `yes / no` — a `no` just defers it, so it can be
   revisited later.

Search covers every type; on a `yes` the `integrate-capability` engine installs each in its right place
(skills also get onboarding and wiring). See the handoff below.

In **suggest-only** mode (Spec-Orchestrator) you may run the read-only `search_artifacts` to name a
fitting artifact, but stop before installing: point the user to the setup agent to set it up (e.g.
"the DX User Experience bundle could rate the built UI during implementation — the setup agent can
install it"). Record it as `suggested` and carry on with the requirements. Installing, prerequisites,
and wiring are always the setup agent's job.

## 2. Hand off to the integration engine

On an explicit `yes`, hand the chosen artifact to the **`integrate-capability`** skill, which runs the
rest the same way for every source: review the metadata, install by type into its home, author an
agent's frontmatter, run a skill's own onboarding/prerequisites, wire it in via the established
patterns, and record the outcome. Discovery is your job; **install-and-wire is the engine's** — don't
duplicate it here.

Carry two things across the handoff:

- **The recommended wiring**, when `references/recommendations.md` named one (the "wired as _Z_" hint) —
  pass it as the suggested pattern; the engine still confirms it with the user and runs the
  `validate-agent-wiring` gate.
- **The gentle contract** — the engine records each outcome in `.github/onboarding/marketplace.md`, so a
  declined or installed artifact is never re-prompted (see the Golden rule). If the user declines before
  the handoff, record `not-now` yourself and stop.

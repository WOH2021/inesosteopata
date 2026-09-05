# Default recommendations (human-curated)

A **maintained starting list** of "if the workspace looks like _X_, a good marketplace artifact to
offer is _Y_, wired as _Z_." These are human-defined defaults — opinionated shortcuts that save the
advisor from re-deriving well-known matches every time. They **seed** the match in
[`marketplace-advisor` §1](../SKILL.md) and the first-run signal-scan in
[`workspace-lifecycle` bootstrap §3](../../workspace-lifecycle/references/bootstrap.md); they do **not** replace judgement.
The list is meant to grow — add a row whenever a signal → artifact match proves useful repeatedly.

## How to use this list

1. **Consult it first — the table is an index, not the whole entry.** When you scan the knowledge base
   (or the user's stated topic) for signals, check [the table](#the-recommendations) below for a match
   before improvising a search. **On a match, follow the row's link to that artifact's detail section
   and read it before offering** — the row is a one-line summary, but the query, the exact wiring, and
   any conditions (e.g. a bundle member that's only wired sometimes) live in the section. Acting on the
   row alone will miss them.
2. **Then use judgement for the rest.** This list is a seed, not an allowlist — signals it doesn't
   cover still get the judgement-based search of §1. Don't refuse to offer something just because it
   isn't listed, and don't offer something listed if it plainly doesn't fit this workspace.
3. **Verify before offering.** An entry names a *search*, not a guaranteed artifact. Run the query with
   `search_artifacts`, review the real hit with the matching `get_*` tool, and only then offer it. If
   the marketplace returns nothing relevant, drop it silently and move on — a stale entry is never a
   reason to push a non-existent artifact.
4. **All the golden-rule guarantees still hold.** Offer once, `yes` / `no`, skip
   anything already settled in [`.github/onboarding/marketplace.md`](../../../onboarding/marketplace.md),
   and cap first-run recommendations at **1-2** total — never a wall.

## The recommendations

Each row is a validated signal → artifact match. The **Artifact** cell links to that artifact's detail
section — the row summarizes, the section is authoritative. On a match: read the linked section, verify
the artifact really exists (step 3 above), then offer. Add rows as matches prove out.

| Signal / when it applies | Artifact (→ details) | Wiring pattern |
| --- | --- | --- |
| Frontend / UI project — a web/SPA stack (React, Angular, Vue, …) in `system/tech-stack.md` / `system/architecture.md`, UI code in a checked-out repo, or (greenfield) `frontend-stack: density` (or a UI `other`) with `has-frontend: yes` in `onboarding-answers.json`. Skip for backend-only workspaces (`frontend-stack: none`) and deferred stack choices (`frontend-stack: decide-later`). | DX **[User Experience bundle](#user-experience-bundle)** (`ux-buddy` + UX skills; Density and Playwright MCPs) | **Verifier-parallel checker** — `ux-buddy` rates built UI in the implementation loop (advisory). Density is **conditional** — see the section. |

### User Experience bundle

**When to offer.** On the table's frontend / UI signal (see the row above for the exact triggers) —
a web/SPA stack, UI code in a checked-out repo, or a greenfield `frontend-stack: density` (or UI
`other`) with `has-frontend: yes`. **Skip it entirely for backend-only workspaces (`frontend-stack:
none`) and deferred stack choices (`frontend-stack: decide-later`).**

**What to offer.** The **User Experience** bundle from the BMW skills marketplace —
`https://skills.bmwgroup.net/bundles/dx/user-experience`. It ships the **`ux-buddy`** agent and its UX
skills (`ux-reviewer`, `ux-writing`, `ux-report-generation`, `synthetic-user-simulation`, `density`).
Search keyword: `ux` (also try `user experience`, `design`); the bundle above is the direct match.
Review it with `get_bundle` and, **only on an explicit `yes`**, install with `download_bundle` — it
expands to its members, each installed in its home by the
[`integrate-capability` engine](../../integrate-capability/SKILL.md): the skills under
`.github/skills/`, the MCP servers into `.vscode/mcp.json`, and
the `ux-buddy` agent — which arrives as a **prose description with no frontmatter**, so author its
Copilot header per the
[`integrate-capability` agent-frontmatter guide](../../integrate-capability/references/agent-frontmatter.md)
(`name` / `description` / `user-invocable: false` / `tools`) before wiring. Save it as
**`ux-buddy.agent.md`** and wire on that slug — a friendly `name: "UX Buddy"` is fine as the picker
label, but every reference below (and the orchestrator's `agents:` list) uses the `ux-buddy` slug, never
the spaced display name. Its `tools` must list the servers it actually calls — `playwright/*`
(drive/screenshot the running app), plus `search` / `fetch`, and `density/*` **only when Density is
wired** (see step 3). The UX skills it depends on must be installed, or it stalls on its own
availability check at runtime.

> **`ux-buddy` rates results — it does not advise on specifications.** It is built to judge a built UI
> (or an existing mockup), not to shape requirements. Wire it in the **implementation phase**, never as
> a requirements advisor in the Spec-Orchestrator. We do **not** generate design mockups during
> requirements — the Figma-mockup flow was removed as too fragile. If a design reference already lives in
> the spec (e.g. a screenshot the team added by hand), the checker may compare against it; we just never
> create one.

### After install — the exact integration to wire

Follow these steps as specified rather than re-deriving the wiring. Each remains an opt-in offer: run it
only on the user's confirmation, pass every frontmatter edit through the `validate-agent-wiring` gate and
the `copilot-authoring-reference` skill, and log each change to `.github/onboarding/changelog.md`.

1. **Connect and test the MCP servers.** Once a UX MCP block (Playwright, and Density only if you wire it
   in step 3) is in `.vscode/mcp.json`, verify it actually connected — the user may need to
   **Start/reload the MCP server** (VS Code: *MCP: List Servers* → Start, or reload the window). Probe
   each with a trivial call and only surface a fix if the test fails (the same connectivity-gate pattern
   used for Atlassian). Don't wire a capability whose MCP isn't reachable — note it and let the user
   defer.

2. **Wire `ux-buddy` as a verifier-parallel UX checker (advisory).** Add it to the
   **`implementation-orchestrator`**'s `agents:` list with one loop line, so it runs **alongside the
   Verifier — but only when the built change includes UI**. It **rates the result** from a UX standpoint
   (and compares against any design reference already captured in the spec) and returns **advisory,
   non-blocking findings**: a UX finding is surfaced to the user, it does **not** trigger a Verifier-style
   retry or become a merge blocker. It runs on the built artifact, never on the draft spec — a non-UI
   change skips it entirely.

3. **Give the Density skill to the Coder and Verifier — only when the project uses Density.** This is
   **conditional, not automatic**: wire Density only if there's evidence the workspace already uses it —
   a Density dependency/import/config in a checked-out repo, or `system/tech-stack.md` naming Density —
   **or** the user explicitly says they want to adopt it (greenfield: only when the `frontend-stack`
   answer is `density`). **If a brownfield project shows no Density signal, do not offer or wire Density**
   — offer the rest of the bundle (advisory `ux-buddy` + Playwright) without it. When Density *is* in
   play: reference the bundle's **`density`** skill from both the `coder` and `verifier` agents (Coder
   builds UI with Density, Verifier checks against it), and because that skill calls the **Density MCP**,
   add its block to `.vscode/mcp.json` and `density/*` to the **Coder's and Verifier's own `tools`** — a
   skill can't reach a server the agent it runs in hasn't been granted.

4. **Give the Verifier the Playwright MCP.** Enable the Playwright MCP (its block in `.vscode/mcp.json`
   — the same one [`workspace-lifecycle` bootstrap §1](../../workspace-lifecycle/references/bootstrap.md) offers for UI
   workspaces) and add `playwright/*` to the **`verifier` agent's own `tools`**, so the Verifier (and the
   `ux-buddy` checker beside it) can drive the running app and **inspect the built UI** — comparing it
   against a design reference in the spec when one exists.

Wire the steps that apply — `ux-buddy` (advisory checker) and Playwright are the core; Density is
conditional on step 3. A user may still accept only some.

## Maintaining this list

This file is meant to be **hand-edited** as the marketplace and our conventions evolve:

- Add a row when a signal → artifact match proves useful repeatedly. Keep search keywords short and
  literal, and specify the wiring pattern (reviewer/rater → verifier-parallel; advisor that shapes
  decisions → requirements advisor; stack-idiomatic builder → specialist Coder; a bundle may span
  several, and a member may be conditional — like Density in the UX bundle above).
- Remove or fix a row when an artifact is renamed, retired, or stops fitting.
- Keep it a **short seed**, not an exhaustive catalogue — judgement covers the long tail. If the list
  grows unwieldy, prune the least-used rows rather than letting it become a rigid keyword table.

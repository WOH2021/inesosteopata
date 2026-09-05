# Workspace Configure

The step-by-step procedure for changing an already-set-up workspace. The Setup agent follows
this when the user asks to add a capability, adjust a prompt, or refresh knowledge — the user never
hand-edits internals. Each flow below is **small and scoped** (not a re-onboard), and each ends the
same way: show the change, get approval, apply it, log it.

> **This is a menu, not a sequence.** Do only the flow the user asked for. Everything here is optional
> — if the user just wanted an answer, or changes their mind partway, stop cleanly; nothing is left
> half-applied.

## Add a capability (skill, agent, MCP config, …)

Adding any artifact — a skill, agent, prompt, instruction, MCP config, or bundle — runs through the
**`integrate-capability`** engine, which acquires it (the **skills marketplace by default**, or a local
path if the user points at one), reviews it for approval, installs it by type into its home, authors an
agent's frontmatter, runs a skill's own onboarding, wires it in via the established patterns, and
records the outcome. Don't re-derive any of that here — pick the source and let the engine run:

- **From the marketplace (default).** If the user describes a *topic* rather than a specific artifact,
  run the **`marketplace-advisor`** skill first to find and gently offer a match; on a `yes` it hands
  off to the engine. If they already named an artifact or gave a link, go straight to
  **`integrate-capability`**.
- **From a local source (on request).** When the user points at a local artifact — a path they give, or
  a child repo already open as a sibling root — **`integrate-capability`** reads its files in place
  instead of downloading; the review, onboard, and wire steps are identical.

## Edit a prompt

Change an orchestrator or subagent prompt to adjust behaviour (e.g. approval counts, when to skip the
Tech-Analyst). Show the before/after of the passage, apply on approval, and summarize the change. If the
change touches frontmatter (`tools`, `agents:`, `name`), check it against the `copilot-authoring-reference`
skill first so fields and tool names stay valid.

## Change an earlier setup choice (sources, stack, ticket tracking, repositories)

When the user changes a structured answer the onboarding form originally captured — a Confluence/Jira
source, the frontend/backend stack, the ticket-tracking system, or the repository list — the change is
made **conversationally** (ongoing mode never re-opens the form), but it must stay coherent: the same
`onboarding-answers.json` is still the form-first input that a later *Generate / Refresh Knowledge* run
reads, so a change applied only to derived files leaves the authoritative answers stale and a refresh can
resurrect the old value. So reconcile **from the answer outward**:

1. **Write the changed answer back into `.github/onboarding/onboarding-answers.json`.** Update the
   affected `answers.{stepId}` record — set its new `value`, mark `source: "human"` (the user just stated
   it), and set a fresh `updatedAt` (ISO). Bump the file's top-level `updatedAt` too. **Preserve
   `submittedAt`** unchanged — setup stays complete; you are editing a submitted answer, not re-submitting.
   Never invent a step id — use the one from `onboarding-config.json`.
2. **Re-run the checks that answer gates.** If the change is a source/credential (Confluence, Jira, `gh`),
   re-run its connectivity check and update the corresponding `command` answer's `value`/`output`; if it
   now fails, route it to a `blocked`/`deferred` todo per the Setup agent's five-status rule rather than
   silently proceeding.
3. **Propagate to every dependent file**, exactly as the bootstrap closeout's propagation rule does: the
   pointers (`external/*`), config (`.vscode/*`, `.github/copilot-instructions.md`), `system/repos.md`,
   `knowledge/process/spec-lifecycle.md` (tracking system), and any knowledge file whose `sources`
   frontmatter names the changed source — then regenerate both INDEX linktrees. A changed source may need
   a scoped **Refresh a single knowledge phase** (below) to redraft from the new source.

Show the full set of changes for approval before applying, and log it to the changelog (Safety & audit).

## Refresh a single knowledge phase

Re-run any one phase via the bootstrap procedure ([bootstrap.md](bootstrap.md)) to update its file(s) when reality changes —
without touching the rest of the knowledge base.

## Add a knowledge category

Create a new `knowledge/{category}/` folder and its files (each with `owner`/`last_updated`/`sources`
frontmatter and section placeholders), then wire it into the linktrees — add a section to
`knowledge/INDEX.md`, and to `external/INDEX.md` if it's an external source.

## Import an existing repo's config

Bring existing investment into the BASE default instead of starting empty — whether from a separate repo
the user points to, or a **child repo already open as a sibling root** that ships its own config (as
surfaced by `workspace-setup`'s *capabilities* report). Opt-in per item, never a blind copy:

- **Skills / agents (as full artifacts)** — list what's found; on approval, integrate each through the
  **`integrate-capability`** engine with the local source, so an imported artifact gets the same review,
  onboarding, and wiring as a marketplace one — not just a file copy left un-wired.
- **Agent / instruction content** — propose specific passages to merge (e.g. a coding-standards block
  into an orchestrator prompt), showing a diff per change; merge intent, not whole files, so the
  default structure stays intact.
- **MCP configs** — propose discovered servers for copy into `.vscode/mcp.json` (secrets → `.env`),
  the user approving each.

## Safety & audit (applies to every flow above)

- **Review before install.** Show what a marketplace agent/skill does and what tools/permissions it
  requests; wait for explicit approval. Never install silently or grant elevated permissions silently.
- **Never copy secrets/tokens** into committed config.
- **Approve before apply.** Show the change (summary or diff), apply only on confirmation.
- **Log everything.** Append every customization (prompt edit, agent install, skill install, imported
  config) to `.github/onboarding/changelog.md` for an auditable, reversible trail.

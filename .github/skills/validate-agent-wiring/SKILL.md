---
name: validate-agent-wiring
user-invocable: false
description: Structural quality gate the Setup agent runs right after it writes or wires an agent into an orchestrator — checks frontmatter and tool names against the reference skills, confirms the orchestrator actually invokes the agent (no orphan), verifies each agent declares the MCP servers it uses, flags duplicate roles, and re-validates. Silent on pass, surfaces issues on failure, never applies over a failure.
---

# Validate Agent Wiring

A **"validate wiring before apply"** gate. Run it the moment an agent is installed or edited and an
orchestrator is wired to call it — *before* confirming the change to the user. It mirrors the
Coder/Verifier rigor on the implementation side: catch orphan agents, duplicate roles, invalid tool
names, and missing per-agent MCP access **at wiring time** instead of at runtime.

**Contract:** silent on success (say "wiring checks passed" and move on). On any failure, list each issue
with the file and a concrete fix, and **do not apply the change** until it's resolved. This is a gate,
not advice.

Use the `copilot-authoring-reference` skill as the source of truth for fields
and tool names.

## What "wired" means here

Wiring a specialist into this workspace is two edits, both keyed on the agent's **filename slug**
(the `<slug>` in `<slug>.agent.md`, never its frontmatter `name:` — see Check C):

1. the agent file exists at `.github/agents/<slug>.agent.md`, and
2. the target orchestrator (`spec-orchestrator` or `implementation-orchestrator`) has `<slug>` in its
   `agents:` list **and** a prose line in its body that actually delegates to it.

Both must be true — a file with no orchestrator reference is an **orphan**; an `agents:` entry with no
prose delegate line is a declared-but-never-called agent.

## Checks

### A — Frontmatter (per `copilot-authoring-reference`)

- [ ] The file has YAML frontmatter **at all** — a marketplace agent often ships as a bare prose body
      with no header; if it's missing, author `name` / `description` / `user-invocable` / `tools` (see
      the `integrate-capability` skill's [`references/agent-frontmatter.md`](../integrate-capability/references/agent-frontmatter.md)) before wiring, don't wire a header-less file.
- [ ] The agent file has a non-empty, specific `description` (not "helps with various things").
- [ ] A specialist subagent sets `user-invocable: false` (it shouldn't appear in the picker).
- [ ] `tools` is a list; `agents`, if present, is a list.

### B — Tool names (per `copilot-authoring-reference`)

- [ ] Every `tools` entry is one of our tool-sets (`edit` `search` `fetch` `runTasks`
      `testFailure` `agent` `todo`), a native VS Code tool (the terminal tools `execute/runInTerminal` ·
      `execute/getTerminalOutput` · `read/terminalLastCommand` · `read/terminalSelection`, or a
      `vscode/*` / `vscodeGeneral/*` tool), or an MCP wildcard / specific
      tool for a server **present in `.vscode/mcp.json`** (the shipped `skills-marketplace` /
      `mcp-atlassian` / `playwright`, plus any a marketplace bundle added, e.g. the UX bundle's `density`).
- [ ] No out-of-workspace names slipped in from the source (e.g. `read/readFile`, `edit/editFiles`,
      `run_vscode_command`, `simpleBrowser.show`) — re-express them in our tool-sets or drop them.
- [ ] Least privilege: the tools match the agent's job. A read-only reviewer/checker has **no** `edit`.

### C — No orphan, no dangling

- [ ] The new agent is in the target orchestrator's `agents:` list, **by its filename slug** — the
      `<slug>` in `.github/agents/<slug>.agent.md`, **not** the frontmatter `name:`. The two often
      differ (`ux-buddy.agent.md` carries `name: "UX Buddy"`); an `agents:` entry of `UX Buddy` resolves
      to no file and the delegation silently never fires. The delegate prose line references the same
      slug. This is the most common breakage for a freshly created agent.
- [ ] The orchestrator body has a prose line that delegates to it (which phase / when / blocking or
      advisory) — it is genuinely invoked, not just declared.
- [ ] Every entry in that `agents:` list — the new one and every sibling — resolves to a real
      `.github/agents/<entry>.agent.md` file (the entry *is* the slug; the edit didn't break a sibling).

### D — MCP access is declared per agent

A custom agent runs with **its own** `tools` — they override anything inherited from the parent, so
there is no reliable "the orchestrator has it, so the subagent gets it." Grant each server to every
agent that actually calls it.

- [ ] Every agent that calls an MCP server lists that server in its **own** `tools` — the new
      specialist *and* any existing agent you extended. E.g. `ux-buddy` needs `playwright/*` (and
      `density/*` only when Density is wired); a Verifier you gave the Density/Playwright MCP needs
      `density/*` / `playwright/*` in the **Verifier's** own `tools`, not just the orchestrator's.
- [ ] The server is actually present in `.vscode/mcp.json` — grant only wired servers.
- [ ] If a required skill calls an MCP server, the agents that load that skill also carry the server
      (e.g. the `density` skill uses the Density MCP, so the Coder/Verifier that use it need `density/*`).

### E — No duplicate role *(replace or coexist)*

- [ ] Scan existing `.github/agents/` for an agent that already covers this role (e.g. a second security
      reviewer, a second frontend coder). If one exists, **stop and ask** the user: replace the existing
      one, or coexist deliberately? Never silently add a redundant agent.

### F — Re-validate

- [ ] After the edits are drafted, re-read the changed files and confirm A–D still hold before
      confirming to the user. If a later tweak touches `tools` or the `agents:` list, run this gate again.

## Not in scope (deliberately)

- **No fixed description-length limit.** Our agent descriptions are a sentence or two; judge by clarity,
  not a character count.
- **No `handoffs:` / display-name matching.** We don't use `handoffs:` frontmatter, and wiring never
  keys off the frontmatter `name:` — it's the `agents:` list (filename slugs) plus a prose delegate
  line (see `copilot-authoring-reference`). Check C is precisely that the entries are slugs, not names.
- **No placement/distribution decisions.** Where an artifact is authored or how it's distributed is out
  of scope; this gate only checks that a wired agent is structurally sound in *this* workspace.

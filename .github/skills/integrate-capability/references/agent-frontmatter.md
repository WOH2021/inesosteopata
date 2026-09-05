# Authoring an installed agent's Copilot frontmatter

A downloaded (or locally imported) agent usually arrives as a **prose description only** — a Markdown
body with its behaviour, principles, and the skills/MCPs it expects, but **no VS Code frontmatter**.
Dropping that body at `.github/agents/{slug}.agent.md` does **not** produce a runnable agent. Before
wiring it, convert it into a valid custom agent — consult the `copilot-authoring-reference` skill for
the fields and tool names, and re-run the `validate-agent-wiring` gate afterwards:

- **`name`** and a specific one-line **`description`**.
- **`user-invocable: false`** — a wired specialist is a subagent, not a picker entry.

> **Critical — the wiring identifier is the *filename slug*, not `name`.** An agent is referenced
> everywhere by its file's slug (the `<slug>` in `.github/agents/<slug>.agent.md`, minus the
> `.agent.md`), **never** by its frontmatter `name:`. The two routinely differ: a file named
> `ux-buddy.agent.md` may carry `name: "UX Buddy"`. The slug goes in every orchestrator's `agents:`
> list and every prose delegate line; `name:` is only the human label shown in the agent picker.
> So when the artifact arrives, **decide the slug first** (pick the filename you save it under —
> lower-kebab-case, e.g. `ux-buddy`), then set `name:` to whatever reads well ("UX Buddy"). Wire on
> the slug. Mixing them up — putting `UX Buddy` in an `agents:` list, or renaming the file to match a
> spaced `name:` — is the most common breakage for a freshly created agent, because the `agents:`
> entry then resolves to no file.
- **`tools:` — the crux.** Read the body and grant **exactly** the capabilities it actually uses,
  re-expressed in our vocabulary: every **MCP server** it calls (e.g. `density/*`, and `playwright/*`
  for screenshots) plus `edit` / `search` / `fetch` / the terminal tools as needed. **Re-express or drop
  names that don't exist here** — a marketplace body often names raw tools like `run_vscode_command` or
  `simpleBrowser.show` that aren't our tool-sets; map them to the nearest shipped capability or omit
  them. Least privilege still applies.
- **`agents:` / `model:`** only if the body delegates to other agents or pins a model.
- **Install the skills it references, too.** If the body lists required skills (a "missing skills"
  table or `<skill>…</skill>` tags), each one must exist under `.github/skills/` — install any that are
  missing through this same procedure, or the agent stalls on its own availability check at runtime.

> **Critical — MCP access is granted per agent.** A custom agent runs with *its own* `tools:`, which
> override anything the parent orchestrator carries — there is no reliable inheritance to lean on. So
> **every agent that must reach an MCP server has to list that server in its own `tools:`**. Whenever
> you add a server to `.vscode/mcp.json`, grant `server/*` (or the specific tools) to *each* agent that
> uses it: the new specialist **and** any existing agent you're extending. Giving the Verifier the
> Density or Playwright MCP means editing the **Verifier's** own `tools:`, not the orchestrator's. An
> agent that calls an MCP it doesn't declare simply can't reach it — this is the most common wiring bug,
> so `validate-agent-wiring` checks it explicitly.

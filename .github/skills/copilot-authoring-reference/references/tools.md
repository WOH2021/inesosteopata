# Copilot Tools Reference (BASE workspace)

The exact tool vocabulary our agents use in `.agent.md` frontmatter. Consult it whenever you **write or
edit an agent's `tools` list**. This is deliberately *our* allowlist — not every VS Code tool — so an
installed marketplace agent gets re-expressed in names this workspace accepts.

## Tool-sets (the shorthand we use)

Prefer these grouped tool-sets; they are what our agents declare:

| Entry | Grants | Typical users |
|-------|--------|---------------|
| `edit` | edit / create files and folders | setup, coder |
| `search` | codebase / file / text search, list dir, usages | every working agent |
| `fetch` | fetch content from a URL | setup, spec-orchestrator, retrieval |
| `runTasks` | run VS Code tasks | as needed |
| `testFailure` | read test-failure details | verifier |
| `agent` | delegate to subagents | orchestrators, setup |
| `todo` | track progress with a todo list | orchestrators |

## Native VS Code tools

- **Terminal** (these replace the deprecated `runCommands` tool-set) — `execute/runInTerminal` (run a
  command), `execute/getTerminalOutput` (read a running command's output), `read/terminalLastCommand`
  (read the last command run), `read/terminalSelection` (read the terminal selection). Grant all four
  to any agent that needs to run commands.
- `vscode/askQuestions` — structured, UI-backed clarifying questions (closed-set answers), used by
  setup. Any `vscode/<tool>` or `vscodeGeneral/<tool>` name is accepted.

## MCP wildcards (servers we ship)

Grant a whole MCP server with `server/*`, or a single tool with `server/tool`:

| Pattern | Server | Used by |
|---------|--------|---------|
| `base-skills-marketplace/*` | BMW skills marketplace (search / list / get / download artifacts) | setup |
| `playwright/*` | browser automation for UI checks | verifier (when the product has a UI) |

`mcp-atlassian` is deliberately **not** granted as a wildcard: the server exposes many write tools
(create/update/delete page, set restrictions, etc.) that our read-only knowledge agents never use, and
enumerating a large server bloats context (and can surface a malformed tool schema). Grant the specific
**read** tools instead:

| Tool | Grants |
|------|--------|
| `mcp-atlassian/confluence_search` | find Confluence pages |
| `mcp-atlassian/confluence_get_page` | read a page |
| `mcp-atlassian/confluence_get_page_children` | walk a page's direct children |
| `mcp-atlassian/confluence_get_space_page_tree` | read a whole space's page tree |
| `mcp-atlassian/jira_search` | find Jira issues (JQL) |
| `mcp-atlassian/jira_get_issue` | read an issue |
| `mcp-atlassian/jira_get_board_issues` | read a board's issues |

This exact set is what `setup`, `retrieval`, and `knowledge-scout` each declare **in their own
frontmatter**. A custom agent runs with *its own* `tools` — they override anything the parent
orchestrator carries, so **each agent that uses a server must list it itself; don't rely on inheriting
it from an orchestrator.** Keep the three in sync because they each independently use these read tools
(and `setup` also uses them directly when it delegates).

The specific-tool form — e.g. `base-skills-marketplace/search_artifacts` — is also fine when you want to
narrow access.

## Rules and conventions

- **Subagent delegation is prose.** Include the `agent` tool-set and list subagents under `agents:`; the
  "call X for Y" instruction goes in the body, not in `tools`. (We don't use the long
  `agent/runSubagent` spelling.)
- **Keep tool lists tight** — grant only what the agent uses. Read-only agents (verifier,
  knowledge-scout) get no `edit`.
- **After editing `tools`, re-check every name here.** The VS Code tool-picker UI can inject
  non-canonical session tool IDs (e.g. `read/readFile`, `vscode/runCommand`) that this workspace does not
  use — replace them with the tool-set shorthand above.
- **A marketplace bundle may add servers.** When an installed artifact writes a new MCP server into
  `.vscode/mcp.json` (e.g. the UX bundle's `density` server, or `playwright`), it becomes grantable the
  same way — add `density/*`, `playwright/*`, etc. to the `tools:` of **each agent that uses it**. Grant a
  server only after it is actually present in `.vscode/mcp.json`.
- **Only reference servers we actually wire.** Don't add an MCP wildcard for a server that isn't in
  `.vscode/mcp.json`.

---
name: copilot-authoring-reference
user-invocable: false
description: Authoring reference for this BASE workspace's VS Code Copilot customization files (.agent.md, SKILL.md, .instructions.md) — the frontmatter fields and this repo's conventions (references/frontmatter.md), and the tool vocabulary of tool-set shorthand, native terminal and askQuestions tools, and the MCP wildcard patterns for the servers we ship (references/tools.md). Consult when writing, editing, reviewing, or wiring an agent, skill, or instruction file, or when re-expressing an installed marketplace artifact's frontmatter and tool names, so they are valid for this workspace rather than guessed.
---

# Copilot Authoring Reference (BASE workspace)

The authoritative reference for the VS Code Copilot customization files this workspace ships —
trimmed to what we actually use. Consult it whenever you **write or wire an agent**, **add a skill**,
**install an instruction file**, or **re-express an installed marketplace artifact** — so frontmatter
fields, values, and tool names are real, not guessed.

It has two parts, each loaded on demand (progressive disclosure):

- **[Frontmatter fields & conventions](references/frontmatter.md)** — required/optional keys for
  `.agent.md`, `SKILL.md`, and `.instructions.md`, this repo's conventions (prose delegation, no
  `handoffs:`, hidden subagents), and how progressive disclosure works. Consult when writing or
  reviewing any customization file.
- **[Tool vocabulary](references/tools.md)** — the tool-set shorthand (`edit`, `search`, `fetch`,
  `runTasks`, `testFailure`, `agent`, `todo`), the native VS Code tools (terminal execution,
  `vscode/askQuestions`), and the MCP wildcard patterns for the servers we ship. Consult whenever you
  write or edit an agent's `tools` list.

After editing an agent's `tools`, sanity-check every name against
[the tool vocabulary](references/tools.md) — the VS Code tool-picker UI can silently inject
non-canonical tool IDs.

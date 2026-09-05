# Copilot Frontmatter Reference

Authoritative frontmatter spec for the files this workspace ships, trimmed to what we actually use.
Consult it whenever you **write or wire an agent**, **add a skill**, or **install an instruction file** —
so frontmatter fields and values are real, not guessed. For tool *names* specifically, see
[tools.md](tools.md).

## Agent files — `.github/agents/<name>.agent.md`

| Key | Required | Type | Notes |
|-----|----------|------|-------|
| `name` | recommended | string | Display name in the agent picker (e.g. `Setup`). Omit → the filename is shown. **Purely cosmetic — never the wiring identifier.** May differ from the filename slug (`ux-buddy.agent.md` ↔ `name: "UX Buddy"`). |
| `description` | **yes** | string | One or two sentences; drives discovery. Keep it tight. |
| `tools` | no | list | Tool-sets / tool names the agent may use — see [tools.md](tools.md). Omit → the agent gets all tools. |
| `agents` | no | list | Subagent **filename slugs** (the `<name>` in `<name>.agent.md`, **without** `.agent.md`) this agent may delegate to — **not** their frontmatter `name:` values. Every entry must resolve to a real file in `.github/agents/`; a spaced display name like `UX Buddy` resolves to nothing. |
| `user-invocable` | no | bool | `false` hides the agent from the slash-command / picker surface (we use this for subagents). Default `true`. |

Our conventions:

- **Subagent delegation is prose, not a tools entry.** Declare access with `agents:` (plus the `agent`
  tool-set); the actual "call X to do Y" instruction lives in the body, not in `tools`.
- **We do not use `handoffs:`.** VS Code shows handoff buttons after *every* response with no conditional
  syntax, which nudges users to switch phase too early. Phase agents give a **state-gated verbal**
  recommendation to switch instead.
- Subagents set `user-invocable: false` so they don't clutter the picker; the three phase agents
  (`Setup`, `Requirements`, `Implementation`) get friendly `name:` values.

## Skill files — `.github/skills/<name>/SKILL.md`

| Key | Required | Type | Notes |
|-----|----------|------|-------|
| `name` | **yes** | string | **Must match the folder name.** |
| `description` | **yes** | string | Task-matching text — this is what triggers the model to load the skill. Make it specific. |
| `user-invocable` | no | bool | We set **`false`** on every skill: skills are agent-loaded procedures, not slash commands. Model-invocation stays on, so they still auto-load by description. |

Files under the skill folder (`references/`, `scripts/`, `templates/`) load only when the body points at
them (progressive disclosure, level 3).

## Instruction files — `.github/instructions/<name>.instructions.md`

We don't ship any, but a marketplace instruction artifact may install here.

| Key | Required | Type | Notes |
|-----|----------|------|-------|
| `applyTo` | **yes** | string (glob) | When the instruction auto-applies, e.g. `**`, `**/*.ts`, `src/**`. |
| `description` | no | string | Purpose. |

## Progressive disclosure (why these fields matter)

1. **Discovery** — only `name` + `description` are scanned (near-zero tokens). A vague description means
   the skill or agent never gets picked.
2. **Body** — the full file loads when a task matches the description.
3. **Resources** — files the body references load only when needed.

## Where these files live

| Type | Path |
|------|------|
| Agents | `.github/agents/*.agent.md` |
| Skills | `.github/skills/<name>/SKILL.md` |
| Prompts | `.github/prompts/*.prompt.md` |
| Instructions | `.github/instructions/*.instructions.md` |

After editing an agent's `tools`, sanity-check every name against [tools.md](tools.md) —
the VS Code tool-picker UI can silently inject non-canonical tool IDs.

---
name: integrate-capability
user-invocable: false
description: Source-agnostic engine that turns a chosen artifact (skill, agent, prompt, instruction, MCP config, bundle) into a set-up, wired-in capability — acquire (the skills marketplace by default, or a local path on request), review, install by type, author an agent's frontmatter, run a skill's own onboarding/prerequisites, wire it into the workflow, and record the outcome. Called by the Setup agent's first-run flow, by the workspace-lifecycle configure procedure, and after marketplace-advisor picks a match. Never installs without explicit approval.
---

# Integrate Capability

The reusable engine for turning a **chosen** artifact into a running, wired-in capability —
independent of where it came from. *Discovery* is a separate concern: the `marketplace-advisor` skill
(the default path) or the user (pointing at a local artifact) decides *what* to integrate; this skill
does everything after that the same way every time.

Its callers:

- **First-run setup** — a signal-scan match (`workspace-lifecycle` bootstrap §3) the user accepts.
- **Ongoing reconfigure** — the `workspace-lifecycle` configure menu's "add a capability" flow.
- **A marketplace suggestion** — `marketplace-advisor` hands off an accepted match here.

Every run ends the same way: show the change, get approval, apply it, record it. **Never install
silently or grant elevated permissions.**

## 0. Acquire the artifact's files

Get the raw artifact files into place from whichever source applies — the **default is the skills
marketplace**; a local path is the opt-in alternative when the user points at one.

- **Marketplace (default).** Review-and-download by type with the `skills-marketplace` MCP — the
  `get_*` tool for metadata, then the matching `download_*` (see the install table in §1). This is the
  normal path; if the user hasn't named another source, use it. Search with **short, literal keywords
  across all types** — the search isn't fuzzy yet, so a full phrase often returns nothing.
- **Local folder / existing repo (on request).** When the user proactively points at a local artifact
  — a path they give, or a child repo already open as a sibling root (surfaced by `workspace-setup`'s
  *capabilities* report) — read its files in place instead of downloading. Everything downstream
  (review, install, onboard, wire, record) is identical.

Whatever the source, the artifact's files are now reviewable; continue to §1.

## 1. Install a chosen artifact (with review)

Only after **explicit approval**. **Review first, always:** for a marketplace artifact call the
matching `get_*` tool for the metadata — description, `version`, `license`, `author`, `compatibility`,
tags (for a local one, read the equivalent files) — and show a short summary so the user approves with
eyes open. Then install by type — everything is written **project-local and committed**, so the whole
team gets it:

| Type | Review · acquire | Lands in | After install |
|------|------------------|----------|---------------|
| **skill** | `get_skill` · `download_skill` | `.github/skills/{slug}/` (keep its `references/`, `scripts/`, …) | onboard (§3) + wire (§4) |
| **agent** | `get_agent` · `download_agent` | `.github/agents/{slug}.agent.md` | author frontmatter (§2) + wire (§4) |
| **prompt** | `get_prompt` · `download_prompt` | `.github/prompts/{slug}.prompt.md` | usable from chat |
| **instruction** | `get_instruction` · `download_instruction` | `.github/instructions/{slug}.instructions.md` | auto-applies via its own `applyTo` |
| **MCP config** | `get_mcp_configuration` | `.vscode/mcp.json` (secrets → `.env`) | — |
| **bundle** | `get_bundle` · `download_bundle` | expand, then install each member by its type above | per member |

(From a **local source**, read the equivalent files rather than the `get_*` / `download_*` calls; the
*Lands in* and *After install* columns are unchanged.) `get_install_link` returns the `ttt` CLI as an
alternative, but it installs **globally** by default — prefer the project-local write here. **Register**
a skill or agent in `.github/copilot-instructions.md` and **log** every install to
`.github/onboarding/changelog.md`.

## 2. Author an installed agent's frontmatter

An agent usually arrives as a **prose description only** — a Markdown body with its behaviour and the
skills/MCPs it expects, but **no VS Code frontmatter** — so dropping it at
`.github/agents/{slug}.agent.md` does not yet produce a runnable agent. Before wiring it (§4), convert
it into a valid custom agent: a `name` and one-line `description`, `user-invocable: false`, a
**least-privilege `tools:` set that lists every MCP server it calls**, and any skills it references
installed too. **The file's `{slug}` — not its frontmatter `name:` — is the identifier every
orchestrator wires to (`ux-buddy.agent.md` ↔ `name: "UX Buddy"`); decide the slug when you save the
file and wire on it.** See [`references/agent-frontmatter.md`](references/agent-frontmatter.md) for the
full field-by-field procedure, the slug-vs-name rule, and the critical per-agent MCP-access rule.

## 3. Run the skill's own onboarding

Applies to **skills** (and any artifact that ships `metadata.deps` or a setup routine); a plain prompt,
instruction or MCP config is ready as soon as it's written. This is what makes setup feel guided rather
than "installed, now what?". A skill's onboarding has two parts: **prerequisites it depends on** and any
**guided setup routine** it ships. Handle prerequisites first (§3a), then the routine (§3b).

Find the guided setup routine, if any, in this order — take the first that matches:

1. **A setup section** in the SKILL.md — `## Setup`, `## Getting started`, `## First run`, or
   `## Prerequisites`.
2. **A companion file** — `ONBOARDING.md` / `SETUP.md`, or a helper the skill ships under `scripts/`
   or `references/` (e.g. an install-check or requirements-validation guide).
3. **Heuristic fallback** — scan the SKILL.md for imperative "run this first / initialize / configure
   before use" instructions and treat those as the setup, best-effort.

If there's no routine and no unmet prerequisites, installation alone is complete — say so briefly and
stop; don't invent a setup step.

### 3a. Satisfy prerequisites first

Read the installed SKILL.md frontmatter for a **`metadata.deps`** block — the marketplace's convention
for declaring dependencies — and satisfy each **before** running any setup (respect an `optional: true`
entry, and don't block core use on it):

- **`mcp_servers`** — the skill needs an MCP server (e.g. `persona-buddy-mcp`). Fetch a ready-to-use
  config with `get_mcp_configuration` and add it to `.vscode/mcp.json`; put any secret in `.env` (never
  commit it). Then **test it actually reaches before relying on it** — probe with a trivial call; if it
  needs a **Start/reload** (*MCP: List Servers* → Start) or a sign-in, walk the user through it and
  don't proceed until it responds. An MCP that's been written to config but never confirmed reachable is
  not yet usable.
- **`external`** — a CLI tool with a `check:` command and an `install_hint:`. Run the check; if it's
  missing, show the hint and let the user install it.
- **`internal`** — another skill; install it through this same procedure.
- **`env_vars`** — add each to `.env` (values stay out of committed config).
- **`config`** — capture the config keys the skill expects.

If a prerequisite can't be met, note it and let the user defer — don't run a setup that will fail. A
skill with no `deps` and no setup routine is ready the moment it's installed.

### 3b. Offer the setup, run only on confirmation

Summarize in plain terms what the setup will do (e.g. "this skill can create UX personas it will screen
future work against"), then run it **only on an explicit `yes`**. Record the result as `done` or, if
declined, `declined`.

> **Invariant — where setup output goes.** Anything the setup produces is *project content*: write it
> to `knowledge/` or `specs/` (add a knowledge category if it fits — e.g. a `knowledge/{category}/`
> folder for UX personas), **never** inside `.github/skills/`. The reusable skill layer stays
> project-agnostic and shareable; the project-specific artifacts it generates live in the knowledge
> base, and the skill is pointed at them.

## 4. Wire it into the workflow

A set-up **skill or agent** should actually participate later (a prompt or instruction needs no wiring —
it's invoked or auto-applies). Recommend one of three established integration patterns — the fit for
its description, letting the user confirm or pick another:

- **Requirements advisor** — informs or screens requirements; wire into the `spec-orchestrator`.
- **Specialist Coder** — substitutes for the generic Coder on matching work, **only** with a concrete
  edge over convention-following; wire into the `implementation-orchestrator`.
- **Verifier-parallel checker** — screens the built work alongside the Verifier; wire into the
  `implementation-orchestrator`.

Before writing the wiring, run the **`validate-agent-wiring`** skill as a gate; fix anything it flags,
confirm the wiring, then log it to `.github/onboarding/changelog.md`. See
[`references/wiring-patterns.md`](references/wiring-patterns.md) for each pattern's exact wiring edit
and the gate's checklist.

## 5. Record the outcome

For every artifact you touch, update `.github/onboarding/marketplace.md`: its `type`, the trigger topic
or source, the `status` (`suggested` / `not-now` / `installed`), the `onboarding` result
(`n/a` / `offered` / `done` / `declined`), and how it's `wired`. This table is what keeps offers
non-repetitive and the whole flow auditable.

## Notes

- **Personas nuance.** The Business-Analyst already elicits *business* personas for a PRD. A persona or
  UX skill's personas are a different, complementary artifact — keep them in their own knowledge area
  so the two never overwrite each other.

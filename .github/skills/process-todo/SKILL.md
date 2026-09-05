---
name: process-todo
user-invocable: false
description: Procedure the Setup agent follows to process a BASE workspace todo — the deferred setup items in .base-todos.json shown in the BASE Todos panel, NOT general/ad-hoc to-do lists or the built-in todo tool. When the user triggers one, locate the entry in .base-todos.json by its id/title, mark it in-progress, run the work it describes (loading the matching procedure skill), then flip it to done, or mark it blocked with a reason. Load whenever a hand-off says it was triggered from the BASE Todos panel.
---

# Process a Todo

Deferred setup work lives in **`.base-todos.json`** at the workspace root and is surfaced in the
**Todos** panel. When the user clicks a `prompt` todo, the extension resumes you with that todo's
prompt, prefixed with its identity — *"… triggered from the Todos panel — you are processing the todo
`<id>` …"*. This skill is how you run one of those hand-offs to completion and keep the todo list
honest. You **execute and record** a todo that already exists; you never invent a new list here (seeding
is a separate step — see the Setup agent's *Seed the todos*).

## 1. Identify the todo

The hand-off names the todo by its **`id`** (or its **`title`** when it has no id). Open
`.base-todos.json`, find the single entry whose `id` (or `title`) matches, and act on **that entry
only**. If nothing matches — the file changed since the panel rendered — say so and stop rather than
guessing which item was meant.

## 2. Mark it in-progress

Before starting, set that entry's `status` to `in-progress` (and refresh `updated`). That is the live
feedback the user sees in the panel while the work runs. Change only `status`/`updated`; leave `title`,
`action`, `priority`, `createdBy`, and `notes` exactly as they are.

## 3. Run the work

The entry's `action.prompt` describes what to produce. Do it the way you would any Setup work —
**load the matching procedure skill instead of improvising**:

- A knowledge phase (refresh Tech & Architecture, extract from Confluence, clone-gated drafting, …) →
  follow the **`workspace-lifecycle`** skill's bootstrap procedure, delegating the heavy gathering to the `knowledge-scout` subagent.
- An ongoing reconfiguration (install a skill/agent, edit a prompt, add a knowledge category) → follow
  the **`workspace-lifecycle`** skill's configure procedure.

The **closeout** (*Final review & approve*) is **not** one of these triggered todos — the Setup agent
seeds no such todo and runs its *Close out* steps itself once every
other todo is settled (`done`/`skipped`/`deferred` — a `deferred` optional todo counts as settled and
does not hold the closeout back). Don't seed or expect a clickable closeout item here.

Never fabricate content: extract from the reachable sources, exactly as those skills require, and
surface the scout's per-claim confidence so the user reviews low-confidence items first.

## 4. Record the outcome — keep the ledger honest

When the work settles, update the ledger entry so it reflects reality:

- **Done** → set the entry's `status` to `done` (done entries drop out of the panel). If the todo
  advanced a knowledge phase, regenerate the INDEX linktrees per the `workspace-lifecycle` bootstrap procedure §2, and
  propagate any changed `owner`/source/ticket key across the files that mention it.
- **Blocked / needs input (required work)** → set `status` to `blocked` and add a one-line `notes`
  saying why. If it's blocked purely for want of structured user input, leave (or seed) a `prompt` todo
  to Setup that asks the user for that specific input when they start it, then resumes the work from
  their answer. Use `blocked` only for work the workspace genuinely still needs — it keeps blocking
  "setup complete".
- **Optional work whose prerequisite is still missing** → set `status` to `deferred` (not `blocked`,
  which would wedge completion, and not `skipped`, which would hide it). This is the case when a
  triggered *optional* todo — e.g. *Recommend marketplace enhancements* — still can't run because its
  MCP isn't reachable: leave it `deferred` with `notes` naming the missing prerequisite and the one fix,
  so it stays visible in the panel to revisit, while setup can still complete. (See the Setup agent's
  five-status rule and its *Seed the todos* parking guidance.)

**Trust the files, not the stored status.** Before you call a todo `done`, glance at its output file(s):
if they still hold `TODO` markers or lack `owner`/`last_updated`, the work isn't actually finished — keep
it open. Never leave a completed phase showing an open todo, or a `done` todo whose file is still a stub.
**If you reopen a todo whose output regressed, also reset the `Final review & approve` entry to
`pending`** (a prior approval no longer covers the changed files), so the self-triggered closeout
re-runs and re-approves after the reopened work settles — never leave a `done` closeout next to a
reopened `pending` todo. **This applies only to todos that change the reviewed knowledge base**
(`knowledge/**` and the config/pointers the closeout approved). A todo that touches *none* of that —
the marketplace pass is the prime example, whether it runs the first time or is re-triggered later; it
records to `.github/onboarding/marketplace.md` and installs artifacts, but doesn't alter the approved
knowledge — must **not** reset the closeout. Running or re-running it leaves a completed setup complete.

## Schema discipline

Edit todos **in place** and keep the canonical shape the extension reads — `title`, `action`, `status`
(`pending` / `in-progress` / `blocked` / `done` / `skipped` / `deferred`, **not** `todo`), `priority`,
`createdBy`, `notes`.
Don't rename the entry, swap its `action`, or add fields the reader ignores (`kind`, `trigger`, `why`,
`provenance`); a wrong shape stops the todo from rendering. Re-running a todo that is already `done`
simply refreshes its file(s) — that's fine and never re-blocks a settled phase.

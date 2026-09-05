---
name: spec-status
description: The per-spec working-state file format and its deterministic linter. Both orchestrators read and write specs/{slug}/status.json as a machine-readable blackboard (entry point, subagents run, Definition-of-Ready boxes, per-repo branches/PRs, per-task results) and lint it with validate_status.py so its structure stays valid across sessions. Loaded by the Spec- and Implementation-Orchestrators.
user-invocable: false
---

# spec-status

`specs/{slug}/status.json` is the **living blackboard** both orchestrators use to resume a spec
cleanly across sessions. It is JSON (not prose) on purpose: a fixed shape can be checked
**deterministically** by a script instead of by eyeballing Markdown. It records *state* — it is
**never a gate** and blocks nothing.

You are loaded by the **Spec-Orchestrator** (requirements phase) and the
**Implementation-Orchestrator** (implementation phase). Use this skill whenever you create or update
a spec's status file.

## Create it

Copy the `_template-status.json` template from `specs/` to `specs/{slug}/status.json` when you first
touch a spec. It
ships with valid enum defaults and `{placeholder}` tokens for the free fields — fill the tokens as
you go, and update only the block for the phase you're in (leave the other as shipped).

## The shape

The `requirements` block is owned by the **Spec-Orchestrator**; the `implementation` block by the
**Implementation-Orchestrator**. Where a value below shows `a | b | c`, those are the allowed enum
values — pick one. Every `{token}` is a free field to fill in.

```json
{
  "spec": "{yyyy}-{kebab-title}",
  "phase": "requirements | implementation",
  "updated": "{date}",

  "requirements": {
    "entry_point": "idea | prd | technical",
    "confidence": "high | medium | low",
    "route_override": "none | {note}",
    "subagents": {
      "business_analyst": "not-run | in-progress | done",
      "tech_analyst": "not-run | in-progress | done",
      "specialists": []
    },
    "awaiting": "nothing | user-answers | user-approval",
    "jira": { "key": "none", "url": "none", "last_synced_status": "none" },
    "definition_of_ready": {
      "acceptance_criteria_testable": false,
      "out_of_scope_present": false,
      "repos_affected_filled": false,
      "open_questions_resolved": false,
      "depends_on_listed": false
    }
  },

  "implementation": {
    "baseline": { "captured": false, "branch": "none", "date": "none" },
    "repos": [
      {
        "repo": "{repo}",
        "branch": "feature/{slug}",
        "state": "in-progress | blocked | done",
        "commit_or_pr": "none | {link}"
      }
    ],
    "tasks": [
      {
        "id": "T1",
        "advances": "AC-1",
        "repo": "{repo}",
        "iterations": "0/3",
        "result": "pending | passed | blocked"
      }
    ],
    "blockers": "none | {reason + which task / AC-{n}}"
  }
}
```

- `subagents.specialists` is a list of `{ "name": "{name}", "state": "not-run | in-progress | done" }`.
- `route_override` records **why**: either the user's own explicit override ("user has a PRD, skip
  BA"), or — for an orchestrator-inferred route — a short note that the user confirmed it via
  `askQuestions` (e.g. `"confirmed: direct-write, no discovery needed"`). A route is never silently
  inferred without one of these two notes.
- `definition_of_ready` booleans are advisory — approval never requires them all green.
- `jira` is set on approval by `jira-sync`.

Keep it valid JSON: double-quoted keys and strings, no trailing commas, one object per list item.

## Lint it (deterministic gate)

After every write, run the linter and read its findings. Try `python3` first, then `python`:

```
python3 .github/skills/spec-status/validate_status.py specs/{slug}/status.json --json
```

It reports:

- **`error`** (exit `1`) — a structural break: invalid JSON, not an object, a missing required
  top-level key (`spec`, `phase`, `updated`), an out-of-range enum (e.g. a repo `state` outside
  `in-progress | blocked | done`), or a boolean/list field holding the wrong type. Fix these.
- **`warning`** (exit `0`) — advisory only: an unfilled `{template-token}`, an unknown key
  (likely a typo), or a **consistency** hint — a repo marked `state: done` whose `commit_or_pr` is
  still empty/`none`/a `{token}`. That last one is the stale-write footprint that strands a spec
  showing `in-progress` with no PR button (the extension renders the button only from a real PR URL
  in `commit_or_pr`): the status was written before the push/PR existed and never corrected. It stays
  a warning — status is continuity, never a gate — but the Implementation-Orchestrator's done
  self-check treats it as a contradiction to fix before declaring the spec done. A partially-filled
  status file mid-phase is normal; warnings never block.

Read the outcome by how the command ended: exit `0` (clean or warnings) or `1` (errors). A shell
"command not found" (exit `127`) for *both* `python3` and `python`, or a missing script, is the only
"unavailable" case — fall back to checking the shape above by hand; do **not** treat it as a pass.

The linter is pure standard library (no third-party deps) and tolerates leftover `{tokens}`, so it
runs anywhere Python 3.8+ is available.

## Keep it out of Jira

`status.json` is internal working state, not a stakeholder artifact. `jira-sync` attaches every file
in `specs/{slug}/` **except** `status.json`, and never mirrors it to a ticket.

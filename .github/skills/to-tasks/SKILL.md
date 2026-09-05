---
name: to-tasks
description: "Break an approved spec into independently-grabbable, tech-agnostic vertical-slice tasks and write specs/{slug}/tasks.json. Loaded by the Implementation-Orchestrator at the start of the implementation phase."
user-invocable: false
---

# to-tasks

Turn an approved spec into `specs/{slug}/tasks.json` — the machine-readable backlog the
Implementation-Orchestrator's Coder/Verifier loop consumes. You are loaded by the
**Implementation-Orchestrator**; you produce the breakdown, the user approves it, and the orchestrator
drives it. You do **not** write feature code.

## Inputs & outputs

- **Inputs** (from `specs/{slug}/`): `spec.md` (goal + `AC-{n}` acceptance criteria + `repos_affected`
  as the guaranteed-present baseline) is always read. When it exists, **`tech-analysis.md` is your
  primary source for each task's `repo` and dependency order** — its per-dimension breakdown and
  cross-repo ripple are richer than spec.md's summary, so prefer it over re-deriving the breakdown
  yourself. `prd.md` (user stories, scope), when present, adds business framing only. On the
  technical-direct route neither exists — `spec.md`'s own `repos_affected` + `Out of scope` is the
  fallback. Read `knowledge/system/repos.md` for the valid repo keys.
- **Output:** `specs/{slug}/tasks.json`, conforming to `specs/_template-tasks.json`.

## Process

### 1. Draft tracer-bullet vertical slices

Break the spec into **tracer-bullet** tasks. Each task is a thin vertical slice that cuts end-to-end
through every layer it touches (schema → logic → API/UI → tests), **not** a horizontal slice of one
layer.

- Each slice delivers a narrow but **complete, verifiable** path — demoable on its own.
- Prefer the **coarsest slice that's still independently verifiable**. Don't fragment one cohesive
  change into a task per `AC-{n}` when several criteria form a single vertical slice in one repo/file
  cluster — a slice can carry several `AC-{n}`, and the Verifier still reports per-criterion. Each
  extra task is another full Coder/Verifier round-trip, which is the expensive part of the loop. Split
  only where a real dependency, a different repo, or a genuinely separable path calls for it: thin
  enough to verify cleanly, not so thin that every tiny edit costs its own round-trip.
- **Assign each slice a `repo`** from the tech-analysis impact (a key in `knowledge/system/repos.md`).
  A slice targets exactly one repo (the checkout/branch boundary); if a change genuinely spans repos,
  split it into per-repo slices linked by `dependsOn`.
- Give each slice `acceptanceCriteria`; where the spec has stable `AC-{n}` ids, tag the criterion with
  its `ac` so the spec → task → check trace is preserved. **Every `AC-{n}` in the spec must be advanced
  by at least one slice.**
- Do **not** encode a verification method — the Verifier decides for itself how to verify each task.

### 2. Order with priority + dependencies

- **`dependsOn`** is the hard constraint: a task can't start until every task it lists is `passed`.
- **`priority`** is the schedule within that constraint (1 = first). Tasks that can run **in parallel**
  share the **same** priority; sequential steps get increasing numbers. Add blockers before the work
  that needs them (e.g. a schema slice before the endpoint slice that uses it).

### 3. Quiz the user

Present the breakdown as a numbered list — for each slice: title, `repo`, `dependsOn`, epic,
and the `AC-{n}` it advances — plus an execution overview:

| Priority | Tasks | Parallel? | Depends on |
|----------|-------|-----------|------------|
| 1 | Task-001 | — | — |
| 2 | Task-002, Task-003 | yes | Task-001 |

Ask: is the granularity right (too coarse / too fine)? are the dependencies correct? should any slices
merge or split? Iterate until the user approves.

### 4. Write `tasks.json`

Write `specs/{slug}/tasks.json` conforming to `specs/_template-tasks.json`:

- Carry the epics forward as a top-level `epics[]` array; tag each slice with the `epicId` it primarily
  advances (a slice may span epics — pick its primary). Tasks stay a **flat, priority-ordered list**;
  `epicId` is grouping/traceability metadata only.
- Set `status: "draft"` at the top level (the user sets it to `"approved"` when satisfied — the
  orchestrator refuses to start until then).
- Leave the loop-state fields at their defaults (`status: "not-started"`, `attempts: 0`,
  `maxAttempts: 3`, criteria `passes: false`) — the Coder/Verifier loop writes them.
- Lint it: `python3 specs/validate_spec.py` — resolve any errors (schema violations) before handing back.

```jsonc
{
  "schemaVersion": "1.0.0",
  "status": "draft",
  "spec": "{slug}",
  "description": "{one-line feature summary}",
  "epics": [{ "id": "Epic-001", "title": "…", "description": "…" }],
  "tasks": [
    {
      "id": "Task-001", "epicId": "Epic-001",
      "title": "…", "description": "As a … I want … so that …",
      "repo": "api", "priority": 1,
      "acceptanceCriteria": [{ "criterion": "…", "ac": "AC-1", "passes": false }]
    }
  ]
}
```

## Reminders

- **One repo per task.** The `repo` field is the checkout/branch boundary; cross-repo work becomes
  linked per-repo slices, never one task touching two repos.
- **No stack assumptions.** Don't bake framework/build details into tasks — the Coder and Verifier
  discover those from each repo and `knowledge/`.
- **Lean coarse; the orchestrator still merges at run time** (via `delegation-protocol`). Your job is
  a clean slice + dependency graph — but don't split a cohesive, one-repo change just for form's sake:
  each extra task is another Coder/Verifier round-trip, and same-repo tasks (even ones touching the
  same file) can be merged into a single Coder pass at run time.

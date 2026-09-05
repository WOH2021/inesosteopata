---
name: evolve-spec
user-invocable: false
description: How the orchestrators handle a follow-up change once a spec exists — a three-tier triage (trivial → implement directly; fits-the-spec → edit the spec first then re-run; new work → a superseding spec), the spec-first + commit-per-change discipline that keeps spec.md the source of truth, and the ticket write-back procedure that keeps the originating Jira/GitHub issue in sync. Load when the user asks for a change to work that is already specced or in-flight.
---

# Evolve a Spec

A spec already exists (approved, in-progress, or done) and the user asks for a follow-up change —
"actually, make the button yellow, not red". Don't guess where it lands: **triage the size, announce
the route, then act.** The user never has to know whether to switch agents — you decide and tell them.

## 1. Triage — three tiers

| Tier | Trigger | What you do |
|---|---|---|
| **1 — Trivial** | touches **no** acceptance criterion (1px larger font, a copy tweak, a colour the spec never named) | implement it directly; record one line in `decisions.md` (committed with the change). No spec edit — the spec never claimed the detail, so there is no drift. |
| **2 — Fits the spec** | same intent; it edits/adds a **bounded** set of ACs; the spec is **not** `done` (or it is `done` but its PR is still open); no fresh Business-/Tech-Analyst work is needed | **edit the spec first** (§2), update `tasks.json` directly, re-run the loop on the affected task(s), then write back the ticket (§3). |
| **3 — New work** | intent changed, scope exploded, it needs BA/TA or a **new repo**, or the spec is already `done` **and its PR is merged/shipped** | **stop.** Create a follow-up spec with `supersedes: {old-id}`, commit it, and route the user to the **Requirements** agent. |

### Tie-breakers (safe by default)

- **Unsure Tier 1 vs 2 → treat as Tier 2.** Never let code silently diverge from a written AC — that
  is the exact drift the process guards against.
- **Unsure Tier 2 vs 3 → default to Tier 2**, *unless* the spec is already `done` **and merged** or the
  intent changed. When it is genuinely ambiguous, ask the user **one** `vscode/askQuestions` (the
  forward-moving option — "update this spec" — is the recommended default).
- **"It needs the Requirements orchestrator's depth"** (real BA/TA re-analysis, a new repo) **is
  itself the Tier-3 signal.** That is why you never run the Spec-Orchestrator as a subagent — the two
  are peer agents; you route the *user* instead.

> Borrowed principle: *update preserves context, a new spec provides clarity.* Choose to update while
> it is the same work; start a new (superseding) spec when patching would confuse more than clarify.

## 2. Tier-2 mechanic — spec-first, then commit, then cascade

Order matters. The spec is the source of truth, so it changes **before** the code.

1. **Confirm** the change with the user (one `askQuestions`, affirmative default).
2. **Edit `spec.md`**: change or add the acceptance criterion (e.g. `AC-3: the primary button is
   yellow`), bump the `updated` frontmatter **timestamp** (a full ISO 8601 date-time, so a same-day
   edit still registers), and note the change + rationale in `decisions.md`.
3. **Commit the spec change** in the home base — a discrete, reversible commit is the versioning
   record. **Path-scope it** (`git add specs/{slug}/…`, never `git add -A`) so it never sweeps in the
   user's unrelated staged work, and commit on a real content change (not the loop's per-iteration
   `tasks.json`/`status.json` churn). Follow the workspace `knowledge/process/git-conventions.md`
   (default: Conventional Commits), e.g. `docs(spec): evolve 2026-billing-retry — button yellow not red
   (AC-3)` with the ticket in the footer (`Refs PROJ-123`); mention it to the user in one line. Commit on
   the spec's `feature/{slug}` branch and **`git push`** so a teammate on another device pulls the change —
   it isn't shared until pushed. **If the workspace repo has no remote** (not published yet), tell the user
   ("no remote origin — no push available") and continue. If the workspace isn't a git repo at all (or
   `specs/` is gitignored), skip the commit and flag it rather than blocking.
4. **Update `tasks.json` directly** — you just made the edit, so don't wait for the next-iteration drift
   check to notice it: mark the affected task(s) not-passed, add a task if the change introduced one, and
   **re-run the Coder/Verifier loop on only the affected task(s)** — not the whole spec. (Drift detection
   stays a *backstop* for edits made **outside** the loop — in another session or by hand — which is why
   `updated` is a full timestamp, not just a date.)
5. **Write back the ticket** (§3).

If a PR is already open for the spec, the fix pushes to the same branch and the existing remote-check
loop applies. If the spec is `done` **but its PR is still open**, reopen it (status → `in-progress`) and
ride that same PR — that is still Tier 2. Only a spec that is `done` **and merged/shipped** is Tier 3.

## 3. Ticket write-back — keep the tracker in sync

When a spec's acceptance criteria materially change (Tier 2) and again at `done`, update the
originating ticket named in the spec's `tracking:` frontmatter (`system` = `jira` | `github` | `none`,
plus `id`/`url`). Setup records which system the workspace uses in
`knowledge/process/spec-lifecycle.md`; if `system` is `none` or the field is empty, there is nothing
to sync — skip silently.

**Only the Implementation-Orchestrator writes to tickets** (least privilege). Mirror the knowledge-update
permission split:

- **A comment** noting the spec change (append-only, low-risk) — post it **automatically and tell the
  user in one line** (like the knowledge-scout update at `done`). Jira: `mcp-atlassian/jira_add_comment`.
  GitHub: `gh issue comment <id> -R <owner/repo>` via `execute/runInTerminal` — derive `<owner/repo>`
  from `tracking.url`, since an issue number alone is ambiguous across a multi-repo workspace.
- **Editing the ticket's description / acceptance-criteria fields** (higher-impact, harder to reverse)
  — **ask once before doing it**, like the PR. Jira: `mcp-atlassian/jira_update_issue`. GitHub:
  `gh issue edit <id> -R <owner/repo>`.

**Degrade gracefully, but never silently.** If the tracking source is unreachable or unauthenticated,
name the ticket that was *not* updated and what the user should do (sign in / reload the MCP server) —
never report the ticket synced when it wasn't.

## 4. Tier-3 mechanic — a superseding spec

When the change is new work, don't overload the current spec:

1. Create (or have the user create) a new spec with `supersedes: {old-id}` in its frontmatter, carrying
   `tracking:` for its own ticket, and link it from the old spec's `## References`.
2. Commit the new spec stub.
3. Tell the user plainly: *"This is a new piece of work — I've started a follow-up spec that supersedes
   the current one. Switch to the Requirements agent to shape it."* The old spec stays as the record of
   what shipped.

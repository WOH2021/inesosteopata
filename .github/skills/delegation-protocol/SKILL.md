---
name: delegation-protocol
user-invocable: false
description: How the Spec- and Implementation-Orchestrators write subagent hand-off prompts and decide what may run in parallel — a structured TASK/CONTEXT/CONSTRAINTS/ACCEPTANCE/FILES skeleton that points at specs/ artifacts, anti-vagueness prompting rules, and a three-dimension independence check for batching and concurrent delegation. Load when delegating to a subagent (Business-Analyst, Tech-Analyst, Coder, Verifier, specialists).
---

# Delegation Protocol

How an orchestrator hands a task to a subagent so it can execute correctly **on the first try, with no
shared conversation state**. Two parts: a **hand-off skeleton** (what every delegation prompt contains)
and an **independence check** (what may run in parallel).

Subagents in this workspace are stateless and coordinate through the `specs/{slug}/` artifacts — so a
hand-off prompt *points at those files*, it does not paste their contents.

## 1. The hand-off skeleton

Every delegation carries these five parts:

```
TASK: {one sentence — what to produce}

CONTEXT: {2–3 sentences — the user's original ask + decisions already made.
          Point at the artifact, don't paste it: "see specs/2026-x/spec.md".}

CONSTRAINTS:
- MUST {required convention / pattern / repo}
- DO NOT {the shortcut this subagent is likely to take}
- {the user's explicit choice} is non-negotiable

ACCEPTANCE CRITERIA:
- [ ] {concrete, checkable condition — for a Coder task, the AC-{n} it advances}

FILES:
- Read:   {exact paths — e.g. specs/{slug}/spec.md, knowledge/system/repos.md}
- Modify: {exact paths in the affected child repo}
- Create: {exact paths}
```

### Anti-vagueness rules

Subagents cut corners when the prompt is loose. For every hand-off:

- **Echo the user's requirement verbatim** — don't paraphrase it into something softer; paraphrase is
  how intent gets lost across a delegation (the "telephone game").
- **Pair every positive spec with a negative one** — "DO NOT also refactor X", "DO NOT skip the tests".
- **Give exact paths**, never "the relevant files".
- **Point at artifacts, not context** — the durable state lives in `specs/{slug}/` (`spec.md`, `prd.md`,
  `tech-analysis.md`, `tasks.json`, `verification-report.md`); name the file and keep the prompt lean.
- **The checker is a different agent than the doer, and it gets the original requirements** — never the
  doer's summary. (This is already how the Verifier works: fresh context, sees the diff + `AC-{n}`, not
  the Coder's reasoning. Keep it that way.)

### Smell test

Before sending: *"Could a subagent with no prior context execute this correctly on the first try?"* If
not, add the missing path, constraint, or acceptance criterion — not more prose.

### Size guide

Too short (a bare instruction) → the subagent improvises. Aim for enough *specific* context to execute
and no more; if a hand-off grows very large, the task probably needs splitting.

## 2. Independence check — merging vs. parallelising

Two different decisions use different bars; don't conflate them:

- **Merging tasks into one work package** (one Coder pass doing several tasks in sequence) is
  **permissive**. Because a single subagent runs them in order, tasks that touch the **same file** or
  have a `dependsOn`/ordering between them can still share a package — the Coder just sequences the
  edits. Merge freely to avoid a full Coder+Verifier round-trip per tiny task; the round-trip is the
  cost, not the code. The only real limits: keep the package **reviewable in one pass** and
  **same-repo** (the checkout/branch boundary).
- **Running packages concurrently** (separate subagents at the same time) is **strict**. Parallel
  subagents must never touch the same file or depend on each other's output. Test each pair on three
  dimensions — **all three must be independent** to run them in parallel:

| Dimension | Question | If "yes" → |
|-----------|----------|-----------|
| Files | Do they touch the same file(s)? | not parallel (can still merge) |
| Data | Does one need the other's output? | not parallel (can still merge, in order) |
| Ordering | Does correctness depend on the order? | not parallel (can still merge, in order) |

So: **merge** cohesive same-repo tasks into few packages (same-file is fine); **parallelise** only
across packages that pass all three dimensions — tasks in different repos pass by construction (isolated
checkouts and branches). Keep concurrent delegations to **at most ~4** so collecting results stays
manageable, and **never** let two parallel subagents edit the same file.

Design and synthesis are **not** parallelizable — the Spec-Orchestrator writes the single `spec.md`
itself after its subagents return, because coherence needs one deliberation.

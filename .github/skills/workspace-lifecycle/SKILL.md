---
name: workspace-lifecycle
user-invocable: false
description: Procedures the Setup agent follows across the workspace's life — the first-run onboarding pass and the Generate-knowledge task (references/bootstrap.md), and ongoing reconfiguration after first run such as adding a capability, editing a prompt, refreshing a knowledge phase, adding a category, or importing an existing repo's config (references/configure.md). Bootstrap connects and records the reachable sources, writes config and pointers, drafts knowledge via the knowledge-scout subagent, regenerates the INDEX linktrees, and recommends marketplace enhancements; configure makes small scoped changes, each shown for approval before it is applied and logged to the changelog.
---

# Workspace Lifecycle

Everything the Setup agent does to stand up and evolve this workspace. Two procedures, each loaded on
demand (progressive disclosure) — follow only the one the current task calls for:

- **[Bootstrap — first run & knowledge generation](references/bootstrap.md)** — turn the empty skeleton
  into a working workspace: connect/record the reachable sources, write config + pointers, draft the
  knowledge base (via the `knowledge-scout` subagent) on the user-triggered Generate-knowledge task,
  regenerate the INDEX linktrees, and recommend marketplace enhancements. It is **form-first** — start
  from `.github/onboarding/onboarding-answers.json`, never a chat interview. Run it for the onboarding
  pass, the *Generate the knowledge base* task, and any granular knowledge refresh. Its steps carry
  stable section numbers (§1, §2, §3) that other skills link to.
- **[Configure — ongoing reconfiguration](references/configure.md)** — change an already-set-up
  workspace: add a capability, edit a prompt, refresh a single knowledge phase, add a knowledge
  category, or import an existing repo's config. A menu, not a sequence — each flow is small, scoped,
  shown for approval, and logged to `.github/onboarding/changelog.md`.

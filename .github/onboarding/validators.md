# Setup Validators — "complete" checklist

> The **per-file acceptance criteria** below are checked phase by phase, right when the Setup agent ticks a phase `done` (fail-fast, not deferred). The checklist right below is the final, cross-cutting gate — it spans multiple phases and is confirmed once, after the last phase.

Setup is complete when:

- [ ] Every `knowledge/**` file has its TODO markers replaced (or sections marked **N/A**, or the phase **skipped**).
- [ ] Each knowledge file has `last_updated` set; `owner` is filled from the sources (CODEOWNERS / Confluence owners / `repos.md` maintainers, at the role/team level) where discoverable and left blank otherwise — **never asked of the user**.
- [ ] Each drafted knowledge file records its provenance in `sources` frontmatter (the repos/Confluence/Jira it was drafted from); empty only for **N/A** sections.
- [ ] `knowledge/INDEX.md` links every category (external files are listed in `knowledge/external/INDEX.md`).
- [ ] `system/repos.md` lists every repo (cloning is the `workspace-setup` skill's job, run when ready).
- [ ] `.vscode/settings.json` has been reviewed and approved.
- [ ] `.github/copilot-instructions.md` is personalized: the "What this workspace builds" summary and the "Primary stack" line hold the real project domain and stack — **the shipped italic placeholders (`*BASE fills this in during setup…*`, `*set during setup…*`, and any `[brackets]`/`TODO`) are replaced**, not left as-is.
- [ ] The user has confirmed the knowledge files are accurate — **satisfied automatically when `.github/onboarding/knowledge-review.json` marks every `knowledge/**` doc reviewed** (that *is* the user's confirmation; don't re-ask). Otherwise confirm the still-unreviewed files.
- [ ] The user has explicitly approved the full configuration in one final review pass (not just the per-phase confirmations).
- [ ] The approval is **recorded**: a `Final review & approve` entry exists in `.base-todos.json` and is `done`, and **no other entry is still open** (`pending`/`in-progress`/`blocked`). This recorded, self-triggered closeout — not the act of approving alone — is what marks setup complete for the extension (`isSetupComplete`). The entry is **not seeded** up front; the closeout creates it and sets it `done` on approval. Until it exists and is `done`, setup stays incomplete even when every other box above is ticked.

Per-file acceptance criteria (each passes only when **true**, not merely present):

- **business/overview.md** — product, core users, and value are filled; no TODO; consistent with the entry-point summary.
- **business/glossary.md** — the **technical and business/domain** terms agents will encounter are defined (or **N/A** for greenfield).
- **business/stakeholders.md** *(optional)* — if used, ownership is at the **role/team level** (never individual names); otherwise `skipped`/`N/A`.
- **system/repos.md** — each repo has name, purpose, clone URL, and main branch; every repo the specs will touch is listed. For a **greenfield** project with no repo yet, a real row for the scaffolded placeholder sibling (Name = the project slug, Clone URL `— (local, not yet published)`) is acceptable until the repo is published.
- **system/tech-stack.md** — languages, frameworks, and datastores are named (**no version numbers** — they churn too fast).
- **system/architecture.md** — components, boundaries, and the main data flows are described.
- **system/deployment.md** — environments, CI/CD, release process, and who can deploy are stated.
- **process/*.md** — dev flow, git conventions (branch + commit + PR rules), and spec lifecycle are stated.
- **external/*.md** — Confluence spaces, Jira keys/boards, and other links recorded as **pointers** (no copied content); `external/INDEX.md` lists them.
- **knowledge/INDEX.md** — one summary + link per file, regenerated from the files.
- **.vscode/mcp.json** — the sources the team uses are wired (Atlassian PATs entered at the VS Code prompt, never committed); `gh` authenticated.
- **Low-confidence items reviewed** — any `knowledge-scout` claim tagged **low** confidence was confirmed or corrected by the user.
- **Provenance recorded** — each drafted file's `sources` frontmatter names the repos/Confluence pages/Jira projects it was built from, so the knowledge agent can later detect which source changed.

Marketplace artifacts (only if any were installed):

- [ ] Any installed marketplace artifact was recorded in `.github/onboarding/marketplace.md`; for a skill, its declared prerequisites (`metadata.deps`) were satisfied or explicitly deferred and any guided setup **offered** (run or declined).

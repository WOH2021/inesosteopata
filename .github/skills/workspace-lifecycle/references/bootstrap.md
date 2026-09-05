# Workspace Bootstrap

The step-by-step procedure to turn the empty skeleton into a working workspace. The Setup agent runs
this for the **onboarding pass** and for the separate **Generate the knowledge base** task (and any
granular knowledge refresh). It is **form-first**: start from the user's answers in
`.github/onboarding/onboarding-answers.json` (never a chat interview). **Onboarding is deliberately
thin** — connect the sources, write config, and record pointers — while **knowledge generation is its
own user-triggered task** (the *Generate / refresh knowledge* button / `base.generateKnowledge`, or the
`prompt` todo the Setup agent seeds in `.base-todos.json`); never draft knowledge content on the
onboarding pass. The answers are just values + provenance; how to *act* on each one lives beside it in
`.github/onboarding/onboarding-config.json` — read each answered step's `description.agent` (plus the
chosen option's description and any `remediation.agent`) as the authoritative per-field guidance rather
than re-deriving it. You orchestrate and write; the `knowledge-scout` subagent does the heavy gathering
when the Generate-knowledge task runs.

Knowledge files ship as a template (headers + hints + TODO + `owner`/`last_updated`/`sources`
frontmatter): **replace TODOs, never invent content.** The `owner`/`last_updated`/`sources` frontmatter
is **internal maintenance metadata for staleness tracking — never a user-facing question.** Fill `owner`
from the role/team signals the scout turns up (CODEOWNERS, Confluence page owners, `repos.md`
maintainers); if nothing surfaces, leave it blank. Do **not** ask the user "who owns this?" to fill it —
it's bookkeeping, not something they should have to reason about. For `system/*` and `business/*`, ask the
`knowledge-scout` to draft from the checked-out repos and Confluence (it loads the `codebase-analysis` /
`domain-analysis` skills); surface its **per-claim confidence and open questions** so the user reviews
low-confidence items first, then write only after they confirm. Keep `external/*` as **pointers** to
sources — distilled business content goes in `business/*`.

Whenever you write a knowledge file, **record its provenance in the `sources` frontmatter** — the exact
repos (with the commit/branch the draft reflects), Confluence pages (with space), and Jira
projects/boards the content was drafted from. This is what lets the knowledge agent later detect *which*
source changed and refresh precisely; a file written without `sources` can only be checked by age.

## 1. Connect the sources first (every session — a gate, not a one-time step)

The scout can only draft from sources it can reach, so check reachability **first, every session** —
but the onboarding form already ran the connectivity checks, so **start from its results** in
`onboarding-answers.json` (the `command`-sourced answers) rather than re-testing from scratch. Keep it
silent and fast when everything's already fine; when something is missing or broken, **route it to a
todo** instead of blocking the run:

- **Jira/Confluence (read the form's result first).** The form ran the Atlassian MCP check
  (`atlassian-mcp`) and collected the specific Confluence page(s) (`confluence-pages`); read those.
  If the check **passed**, the MCP is reachable — record the named pages in `external/confluence.md`
  and **scope every scout search to them** (never blind-search whole spaces). If it **failed or is
  missing**, don't block: **seed a todo** to connect it (a `prompt` todo to Setup that walks the user
  through it — uncommenting the hosted **`mcp-atlassian`** block in `.vscode/mcp.json` and taking the
  Jira + Confluence PATs at the **VS Code prompt**, stored encrypted, **not** in `.env`). If an
  Atlassian MCP is already reachable at the VS Code **user level**, it's done — don't re-configure it.
- **GitHub (read the form's result):** the form's `gh-auth` / `github-access` results say whether `gh`
  is signed in. If missing, delegate `gh auth status` to `workspace-setup` (the Setup agent has no
  shell) and read its report — **never ask "did you run `gh auth login`?"**. Only if it genuinely
  fails, seed a todo to walk the user through `gh auth login`. Git, PRs, and issue/PR reads go through
  `gh` — no GitHub MCP needed.
- **Ticket source (already answered):** the form's `task-management` answer (with `jira-key` or
  `github-kind`) says where the team tracks work; record it in the external knowledge map so
  `spec-orchestrator` and `retrieval` know where tickets live. Don't re-ask it.
- **Repos (clone is long — seed a todo, then run it this session):** once `system/repos.md` exists, the
  repos from the `repositories` answer need cloning as sibling roots next to the home base, which is
  slow — **seed a `shell`/`prompt` todo** that triggers the `workspace-setup` subagent. Seeding keeps
  the ledger honest, but on a first run you then **run that todo yourself in the same session** (don't
  leave it for the user to click); it just runs after the cheap config work, not before. When it runs
  and `workspace-setup` reports **capabilities** (agents, skills, or MCP a child repo ships
  in its own `.github/`/`.vscode/`), proactively **offer to integrate them** via the *Import an
  existing repo's config* flow in the configure procedure ([configure.md](configure.md)) (opt-in per item, never a blind copy).
  - **Greenfield (no repo to clone — scaffold a placeholder instead):** there's nothing to clone, so
    don't seed the clone todo. Instead, on the do-now pass have `workspace-setup` create a **single**
    placeholder child repo as a sibling at `{childRepoRoot}/{slug}/` (default `../{slug}/`, slug from
    `project-name`): make the folder, **`git init`** it, and write a one-line `README.md` naming the
    project and its stack (e.g. `# TaskJourney — frontend project` / `TechStack: Angular, Density.`), so
    the child-repo root isn't empty until the first spec. If a tier's stack is `decide-later`, omit the
    `TechStack` line (don't invent a stack the user deferred). Record it as a **real row** in `system/repos.md`
    (Name = the slug, Clone URL = `— (local, not yet published)`, branch `main`) — a real Name, not a
    `TODO` row, so the extension adds `../{slug}` to the personal `*.code-workspace`. Don't push and don't
    hand-write the workspace file. Create one placeholder by default; only split into a frontend + backend
    pair if the user confirms.
- **Extraction guidance (optional user steer — read it, don't act on it yet):** the brownfield
  `extraction-guidance` answer is the user's free-text note on *how* to read the sources above (which
  source is authoritative when they disagree, a repo that vendors code from another project, a
  subsystem to focus on). It changes source **weighting and scope**, not the source list, so it only
  matters on the **Generate-knowledge task** — not this thin onboarding pass. Preserve it verbatim now,
  and when the Generate-knowledge task runs — **only if `project-state` is still `brownfield`** (the
  form keeps a hidden answer, so a brownfield→greenfield switch can leave a stale value; ignore it
  then) — **pass it verbatim to the `knowledge-scout`** so it shapes what the scout reads and how it
  weights conflicts. It never adds sources, never overrides an explicit human answer, and never licenses
  invented content or ignoring grounding — treat it as user notes about sources, not as agent
  instructions.
- **Frontend testing (optional):** if the `has-frontend` answer is yes and the Playwright MCP block
  isn't yet uncommented, offer to wire it — uncomment its block in `.vscode/mcp.json` — so the
  `verifier` can drive the app for UI integration checks. Skip it for backend-only workspaces.
- **Skills marketplace (test it early):** the shipped `skills-marketplace` MCP needs a **one-time OAuth
  browser sign-in** before its tools (`search_artifacts`, `download_*`) work. Probe it this session; if
  it isn't reachable, have the user complete the sign-in / **Start the server** (*MCP: List Servers* →
  Start) **before** the marketplace-recommendation pass (§3), so an approved install isn't blocked
  halfway through.

> **Standing rule — an enabled MCP isn't wired until a probe succeeds.** Whatever you enable — a shipped
> block here, or a server a marketplace artifact adds later (§3 / the `marketplace-advisor` and
> `integrate-capability` skills) —
> treat it as *unreachable until proven otherwise*: run a trivial probe, and if it fails, get it working
> (**Start/reload the server**, finish the sign-in, or enter the PAT) or defer it explicitly with the
> user. Never move on to the next topic assuming a server is available when you haven't confirmed it.

Once the sources are recorded, the *cheap* part of the onboarding pass is done. Knowledge generation is
a **separate task with its own todo** — the onboarding pass itself writes only config and pointers and
**never drafts knowledge content inline**. But "separate task" does **not** mean "left for the user":
on a first run the Setup agent seeds the **Generate the knowledge base** todo and then **runs it in the
same session** (the *Work the todos this session* step), so the workspace ends up fully drafted without
the user having to click it. The same task also runs later on demand — the *Generate / refresh
knowledge* button (`base.generateKnowledge`) or that todo from the panel — but on first run you drive
it yourself. Either way it runs *as* the Generate-knowledge task, never as inline onboarding work.

**Do now on onboarding (fast, straight from the form's answers):** the `system/repos.md` skeleton
(names + clone URLs) from the `repositories` answer, the `external/*` pointers from the
`confluence-pages` and ticket-source answers, and the Agent-Configuration files from the stack answers.
**Do not draft any knowledge *content* here** (identity/overview, tech, architecture, process, …).

**Defer to the Generate-knowledge task (all knowledge content) and other todos:** the whole knowledge
base — Identity, each repo's purpose, Tech & Architecture, Deployment, Process, and Team — is drafted
by the **Generate the knowledge base** task, gated on the repos being cloned. A field that's genuinely
unknowable **and** blocking becomes a **`prompt` todo to Setup** that asks the user for that specific
input when they start it (never a mid-run interrogation). Mark a section **N/A** if it genuinely doesn't apply.

When the Generate-knowledge task runs, consult the `extraction-guidance` answer — but **only when the
workspace is actually brownfield**. Gate on **both** `project-state` being `brownfield` **and** the
guidance being non-empty; a value alone is not enough. The form keeps a hidden step's answer when its
`when` stops matching, so a user who filled in guidance and then switched `project-state` to
`greenfield` leaves a **stale** `extraction-guidance` record on disk — ignore it in that case (there are
no listed repos/Confluence sources for it to steer anyway). When both hold, **brief the
`knowledge-scout` with it verbatim** before it reads anything, and weight the sources the way it says —
honor the stated authority when sources conflict, note any cross-project code provenance it flags, and
bias depth toward the focus areas it names. It steers *how* the listed sources are read; it never adds
sources or overrides an explicit human answer. Then let the `knowledge-scout`
draft **silently** from every source it can reach and **write the draft straight into the file** —
extract, don't ask, for anything a source can yield, in particular:

- **Identity** — the product **title and description** from repo READMEs + the named Confluence pages.
  The organization is **always BMW** — never ask for or invent a company name. This is the
  same signal that fills each file's `owner` metadata — derive it, never ask the user for it.
- **Repositories** — each repo's **name and purpose** from the repo itself (README/description). The
  *which repos* choice was already made in the form (the `repositories` answer); never re-ask it in chat.
- **Team** *(optional)* — **stakeholders** discovered while building the rest (CODEOWNERS, Confluence
  page owners, `repos.md` maintainers). Fill what's found; leave blank if nothing surfaces.

**Don't ask who reviews or approves specs** — the user approves; there's no approver role to capture.

Two rules for the drafts themselves:

- **Repo-qualify every reference.** The workspace spans multiple repos, so whenever a knowledge file
  names a file, directory, or command, **prefix it with the repo** — `wiki2graph: src/kg_generator/`,
  not a bare `src/kg_generator/`. An agent reading the knowledge base must never have to guess which
  repo a path belongs to.
- **Business content comes from business sources.** Draft `business/*` (product, users, value, glossary,
  stakeholders) from the **Confluence/Jira sources the user named** — *not* from code. Repos are the
  source for `system/*` (technical). If the business sources are thin, mark the gap low-confidence;
  **never backfill `business/*` with technical detail scraped from a README.**
- **Record provenance in `sources`.** For every file you write, fill the `sources` frontmatter with the
  repos (and the commit/branch the draft reflects), Confluence pages (and space), and Jira
  projects/boards it was drafted from — the same sources the scout cited its claims against. Leave it
  empty only for a section marked **N/A**. The knowledge agent uses `sources` to decide when a refresh
  is needed, so an unrecorded source is invisible to drift detection.

1. Identity → `business/overview.md`, `business/glossary.md` — *Generate-knowledge task* (drafted from the sources)
2. Repositories → `system/repos.md` — skeleton (names + URLs) *onboarding do-now*; clone + per-repo purpose → *Generate-knowledge task*. **Greenfield:** the do-now instead scaffolds a placeholder child repo — a `git init`-ed sibling `{childRepoRoot}/{slug}/` with a one-line README, recorded as a real `repos.md` row (Clone URL `— (local, not yet published)`).
3. Tech & Architecture → `system/tech-stack.md`, `system/architecture.md` — *Generate-knowledge task* (needs cloned repos)
4. Deployment → `system/deployment.md` — *Generate-knowledge task* (needs cloned repos)
5. Process → `process/development-flow.md`, `process/git-conventions.md`, `process/spec-lifecycle.md` — *Generate-knowledge task*
6. External Knowledge → `external/confluence.md`, `external/jira.md`, `external/other.md`, `external/INDEX.md` — *onboarding do-now* (pointers from the answers)
7. Team *(optional)* → `business/stakeholders.md` — *Generate-knowledge task* (auto-filled from what the scout finds)
8. Agent Configuration → `.vscode/settings.json`, `.vscode/mcp.json`, `.github/copilot-instructions.md` — *onboarding do-now*

> **Team is light, optional, and auto-filled.** Capture ownership only at the **role/team level** (e.g.
> "the Platform team owns infra", "the Payments team owns the checkout service"), drawn from what the
> scout finds (CODEOWNERS, Confluence, `repos.md`) — don't ask for it, and **never name individual
> people**. Don't record who "approves" specs: the user approves, so there's no approver to capture. If
> nothing surfaces, skip it.

## 2. Regenerate the linktrees and do a final pass

Each phase is checked against its own acceptance criterion in `.github/onboarding/validators.md` when
it's ticked `done` (whether done-now on the onboarding pass or by the Generate-knowledge task) — this
step is a final cross-cutting pass, not a re-check of each file. It runs **automatically** once the
Generate-knowledge task and every other setup todo are settled — `done`, `skipped`, or `deferred` (a
`deferred` optional todo, e.g. the marketplace pass with its MCP down, counts as settled and does not
hold the closeout back) — the Setup agent moves into it itself
(and into the *Final review & approve* closeout), rather than waiting for the user to trigger a todo.
Regenerate `knowledge/INDEX.md` and `knowledge/external/INDEX.md` **from the files as the last step**,
then confirm the checklist at the top of `validators.md` (the criteria that span multiple phases: INDEX
links every file, `.vscode/settings.json` reviewed, the user has confirmed overall accuracy). For that
accuracy gate, **read `.github/onboarding/knowledge-review.json` first**: when its `reviewed` map
already covers every `knowledge/**` doc, the user has stated the knowledge is accurate — treat that gate
as met and don't re-ask; only chase confirmation for docs it doesn't yet list.

**Then run the closeout and record it — the step that actually marks setup complete.** Confirming the
checklist is not the end: hand off to the Setup agent's *Close out* steps (final review, workflow,
recommendations), present the single approve-or-change prompt, and **on approval write the closeout to the
ledger** — add a `Final review & approve` entry to `.base-todos.json` (with `createdBy: "Setup"`) if it
isn't already there, and set its `status` to `done`. That recorded entry, with no other entry still
open, is exactly what the extension reads (`isSetupComplete`) to unlock the workspace. The entry is
**not seeded** up front, so if you finish this pass without creating it the workspace stays locked even
though every file is done — never stop here without recording the `done` closeout.

**Regeneration and propagation are not one-time.** Any later correction — during the final review or
afterwards — must **re-regenerate both INDEX files** and **propagate the change everywhere**: an edited
`owner`, Confluence space, or Jira project/board key has to be updated in *every* file that mentions it
(`process/*`, other `business/*` / `system/*` files, and the INDEX summaries), not just the one file the
user pointed at — including that file's `sources` frontmatter. Never leave the INDEX or a sibling file
describing the pre-correction state.

You don't clone or build repos yourself — that's the `workspace-setup` subagent (see §1, *Repos*).

## 3. Recommend marketplace enhancements (after the final review, before hand-off)

Run as **step 4 of the self-triggered closeout** (the Setup agent's *Final review, workflow, and
recommendations*), right after the final review is approved — it is **not** a separate user-clickable
todo. Take the **one proactive first-run pass** over the marketplace:
scan what was just written for signals that map to a useful marketplace artifact. Start from the
**curated defaults** in the `marketplace-advisor` skill's
[`references/recommendations.md`](../../marketplace-advisor/references/recommendations.md) — a maintained
list of stack/signal → artifact matches (today: a **frontend / UI** project → the DX **User Experience**
bundle — `ux-buddy` wired as an implementation-phase advisory UX checker, Density only if the project
uses it) that hands you a ready-made query and wiring plan. Beyond that
seed, don't try to hardcode every signal (too brittle) — turn what's actually in `business/overview.md`,
`system/architecture.md`, `system/tech-stack.md`, and `process/*` into search terms with judgement.
Examples of signals worth a query: security/compliance-critical data, regulated industries, strict
perf/scale SLAs, a design system or a11y ruleset, heavy async/messaging architecture.

**Greenfield — the stack answers are the signals.** On a greenfield onboarding pass the knowledge
*content* isn't drafted yet (it's the Generate-knowledge task), so `system/*` / `business/*` are still
templates and a knowledge-only scan finds nothing. Do **not** treat that as "no fit" and skip the pass —
read the stack answers from `onboarding-answers.json` (`frontend-stack`, `backend-stack`, `has-frontend`,
`audience`) and map them to searches directly: `frontend-stack: density` (or any UI stack) with a
frontend → `ux`, `design system` (the UX / Density bundle in `recommendations.md`); `backend-stack:
quarkus-java` → `quarkus`, `java`; `backend-stack: python` → `python`. A tier answered `decide-later`
is **not** a signal — skip it (don't guess a deferred stack; the match surfaces once it's chosen, e.g. at
the first spec). Keep the keywords short and literal (§1 of `marketplace-advisor`), run at most a couple
of queries, and drop silently if the marketplace returns nothing.

**Unreachable ≠ no match — park it `deferred`, don't drop it.** "Drop silently" applies only when you
*searched* and found nothing relevant. If instead the `skills-marketplace` MCP is **unreachable** (not
signed in, so `search_artifacts` errors and you can't even look), do not skip the pass with no trace:
record a **`deferred`** todo — *"Recommend marketplace enhancements"* — whose `notes` name the missing
sign-in and say that starting the todo re-runs the pass (per the Setup agent's five-status rule and its
*Seed the todos* parking guidance). `deferred` is terminal for completion, so the closeout still finishes, and the
item stays visible in the Todos panel for the user to trigger once they've signed in.

The search and offer follow the **`marketplace-advisor`** skill (discovery), and a `yes` hands off to
the **`integrate-capability`** engine (install/onboard/wire) — so this pass stays consistent with
reactive suggestions and never double-offers:

- **Search via marketplace-advisor** — all artifact types, **short literal keywords** per signal (the
  marketplace search isn't fuzzy, so a natural-language phrase often returns nothing). Run at most a
  **couple** of queries and cap surfaced recommendations at **1-2** — not an upsell wall; the user can
  ask "what else fits?" for more.
- **Skip anything already settled** — check `.github/onboarding/marketplace.md` first and don't re-offer
  an artifact already `installed` or `not-now`; this pass and the reactive one share that state.
- For each good match, one `vscode/askQuestions` prompt naming the signal and the artifact (e.g. "This
  system looks security-critical — install the Security-Manager agent to review technical specs?").
- A **yes** hands off to the `integrate-capability` engine (review → install by type → for a skill,
  onboard → wire → log). Record the outcome (`installed` / `not-now`) in
  `.github/onboarding/marketplace.md`. Never auto-install.

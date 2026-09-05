# Copilot instructions for Body Motion Pilates

## Project shape
- This is a static marketing site, not a JS app or framework project. Most work happens directly in HTML/CSS files under the site root and `/en` mirror pages.
- Main content pages: `index.html`, `about.html`, `schedule.html`, `contact.html` and their English equivalents in `en/`.
- Shared styling lives in `css/styles.css`; interaction logic is minimal and lives in `js/main.js`.
- Visual assets are in `assets/images/` and the site relies on static generated/served files; there is no bundler, build step, or test suite.

## Architecture and conventions
- The site is intentionally bilingual: every Portuguese page has a matching English page with the same section structure and similar content.
- Keep translations in sync: if you update nav links, CTAs, SEO metadata, or service details in one language, update the paired file in `en/`.
- Relative paths differ by locale: root pages link to `en/...` and English pages link back with `../`.
- Metadata is important here: each page includes canonical URLs, hreflang tags, Open Graph/Twitter tags, and JSON-LD structured data for local SEO and business discovery.
- Preserve the existing branded design language: warm cream background, dark brown text, serif headings, sans-serif body copy, and the original palette values in `css/styles.css`.

## Editing patterns
- Prefer small, targeted HTML/CSS edits. Do not introduce framework dependencies or rewrite the site into a build-heavy app.
- Reuse the existing semantic structure: `header`, `main`, `section`, `footer`, `nav`, and CTA/button classes already defined in CSS.
- Keep mobile-first behavior intact; the site uses responsive breakpoints and a hamburger menu for smaller screens.
- For a new page, mirror the same structure as the existing pages and update the desktop/mobile nav and language switcher in both languages.

## JavaScript and behavior
- `js/main.js` only handles the mobile menu toggle and the dynamic footer year. Keep behavior tiny and plain DOM-based.
- Follow the existing pattern: `DOMContentLoaded`, query selectors, class toggles, and `aria-expanded` updates for accessible menu behavior.
- Avoid adding new runtime dependencies or client-side state management; this codebase expects lightweight browser behavior only.

## Local workflow
- Local preview: `cd /Users/whaltonhippertt/code/repositories/bodymotion/bodymotion && python3 -m http.server 8080` then open `http://localhost:8080`.
- There is no build, lint, or test command to run for normal changes; validate by checking the rendered HTML/CSS in a browser and confirming the language/version parity.
- For deployment/content changes, keep the static hosting pattern in mind: GitHub Pages or similar static hosting is the intended deployment model.

## Examples to follow
- The navigation and footer patterns are repeated across `index.html`, `about.html`, `contact.html`, and `services.html`.
- The header/footer structure and `lang-btn`/`menu-toggle` behavior are used consistently across both Portuguese and English pages.
- SEO is not optional here: follow the same meta-tag and structured-data conventions used in `index.html` and `en/index.html`.

##Instructions for Copilot
- When generating content, maintain the bilingual structure and ensure that any new sections or edits are mirrored in both Portuguese and English.
- Keep the design and layout consistent with the existing pages, using the established CSS classes and HTML structure.
- Avoid introducing new frameworks, libraries, or complex JavaScript; the site should remain lightweight and static.
- Ensure that all links, images, and assets are correctly

# BASE — Agent Instructions

Welcome to **BASE**: your team's home base for spec-driven development across many repositories. BASE runs on a small team of agents — no central router — each owning one phase from idea to shipped code.
You are one of them, and this is how BASE works; every agent reads it on every request.

> BASE personalizes this file during setup (what you're building, your stack). It stays short by design — it loads on every request, so the detail lives in `knowledge/`, not here.

## What this workspace builds

<!-- setup: 1–2 sentences — what the product/project does, who it's for, and the problem it solves, so an
     agent grasps the purpose before opening knowledge/. Keep it short; depth lives in
     knowledge/business/overview.md. -->
Primary stack: Existing repository; frontend and backend technologies will be verified from the checked-out codebase. Workspace conventions use the current design system where applicable.

## What this repo is

This is your **home base**: it holds **knowledge, configuration, and specs** — *not* application code.
Your code lives in child repositories, opened as **sibling workspace roots** alongside the home base.
**Never write code in this repo.**

## Pick the right agent

BASE has no central router — you pick the agent for the phase you're in:

| You want to…| Use…|  ----------------------------------------- -------------------------------|
| Know where you are / why you're blocked / what to do next | `guide`     |
| Set up or reconfigure the workspace     | `setup`                       |
| Turn an idea / PRD / ticket into a spec | `spec-orchestrator`           |
| Implement an approved spec              | `implementation-orchestrator` |
| A trivial, one-off edit                 | just ask here, inline         |

`guide` is **read-only self-service orientation** — stuck, or unsure which agent you need? Ask it; it
reads the workspace state and explains your current stage, why you're there, and the single next step.
It never edits anything and never runs another agent.

Spec → implementation is an **artifact hand-off**: the Spec-Orchestrator leaves an approved `spec.md`;
you switch to the Implementation-Orchestrator, which picks it up from `specs/_status.md`. BASE's agents
are peers — they never run each other as subagents.

## Before each task

1. **Ground yourself in `knowledge/` first — this is not optional.** Read `knowledge/INDEX.md`, then load the files relevant to your task (e.g. `system/` for code work, `business/` for requirements, `process/` for workflow). **If it's missing or not deep enough, escalate to the `retrieval` subagent** for external sources (Confluence, Jira, GitHub issues/PRs, URLs). Never guess or stop short of it.
2. Check `specs/_status.md` for where features stand.
3. For code work, make sure the target repo is open as a **sibling root** next to the home base. The `workspace-setup` subagent clones it, and BASE adds it to your personal `*.code-workspace` and to the sandbox filesystem allow-list (in the workspace file's `settings` and in `.vscode/settings.json`) so reads and writes into the sibling repo don't prompt. If a not-yet-opened sibling still prompts, that's expected transient state — let BASE widen the list; don't disable the sandbox.

## Rules (non-negotiable)

- **NEVER** commit to `main`; **NEVER** merge, deploy, or force-push; and **NEVER** push code branches or open/merge PRs without explicit human confirmation. *(Exception: an agent commits **and pushes** a spec's own `feature/{slug}` branch in the home base repo — spec artifacts only — so the spec reaches teammates on other devices. If the repo has no remote, it says so and moves on without pushing.)*
- All code goes through PRs. Code lives in the affected child repos, opened as sibling workspace roots; spec artifacts in `specs/`. Never mix them.
- **NEVER** commit secrets — use the environment or the secrets manager.
- Destructive or infra changes require explicit human confirmation.
- By default, BASE requires a spec to be `status: approved` before implementation. *(A configurable default — change it here if your team works differently.)*
- When a business decision is unclear, ask — don't assume.

## Operating standard (every agent)

These are commitments, not suggestions. Meet all of them before you claim a step is done.

- **Ground truth first** — read real files/command output; prefer deterministic sources over guesses.
- **Work through artifacts** — read your input artifact; write your output to its canonical template.
- **Evidence + confidence** — cite the source for each claim; tag uncertain ones high/medium/low; show evidence, don't assert.
- **State boundaries** — say what's out of scope / not owned / not done.
- **Escalate, don't spin** — keep loops bounded; on a stalemate or genuine ambiguity, ask the human.
- **A source or tool that's *optional* to the task is unreachable** → proceed best-effort and **flag the gap** in your output; never let it vanish. Optional work parked for a missing prerequisite is recorded as visible, revisitable follow-up (e.g. Setup's `deferred` marketplace todos) — it does **not** stop the task.
- **A tool or MCP server *required by the current task* fails** (e.g. the Playwright/Density MCP for a UI check the task depends on) → **stop that task and make it visible**: name the server, what it blocks, and the fix (*Start/reload the server* via **MCP: List Servers**, sign in, or enter the PAT). **Never report a step done or a check passed when you couldn't run it** — say "couldn't verify X". A subagent must carry any such failure in the summary it returns, so the orchestrator surfaces it. *(Required vs. optional is per task: `skills-marketplace` being down blocks an install you were explicitly asked to do, but is merely deferred for Setup's optional recommendation pass — see `setup` agent.)*

## Find more

- Knowledge linktree → `knowledge/INDEX.md` · External sources → `knowledge/external/INDEX.md`
- Active specs → `specs/_status.md`

## Sandbox

BASE runs your commands sandboxed by default, with one narrow exception. On macOS, authenticated GitHub CLI operations and Git remote operations need the user's Keychain credential, which the VS Code sandbox cannot retrieve. Run these commands with an unsandboxed-execution request, stating that the GitHub credential helper requires Keychain access: GitHub `gh` queries or mutations, and remote Git commands such as `git fetch`, `pull`, `push`, `ls-remote`, and private-repository clones. Keep local Git inspection and all other commands sandboxed. Never read, print, or write tokens or Keychain data. If GitHub authentication still fails outside the sandbox, report the failure and ask the user to authenticate with `gh auth login`.
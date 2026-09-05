---
name: codebase-analysis
user-invocable: false
description: Procedure for profiling a checked-out repository — extracting its structural facts (stack, modules, APIs, integrations, messaging, workflows) as ground truth, then enriching them with architectural context — to draft system/* knowledge or to assess whether a git diff affects knowledge. Grounds every claim in source and tags confidence. Used by the knowledge-scout subagent.
---

# Codebase Analysis

A repeatable procedure to characterize an affected child repo (an open sibling root). Produce **drafts** for
`system/tech-stack.md` and `system/architecture.md`, or — in drift mode — a list of knowledge files
a diff likely affects. **Extract deterministic facts first, then enrich** — never lead with
inference. Ground every statement in a file you actually read, tag how confident you are, and mark
unknowns as open questions rather than guessing.

## Method: extract → enrich → verify

1. **Extract (ground truth).** Pull structural facts from the sources that state them outright —
   manifests, config, annotations, routing tables, schema/migration files. These are deterministic;
   trust them over inference.
2. **Enrich (context).** Add the architectural and business meaning the raw facts don't carry: what
   each module is *for*, how data flows, where the boundaries are.
3. **Verify.** Confirm enriched claims against the source. Where static signals and code disagree, or
   a fact is built dynamically (routes registered at runtime, topic names from config, builder-pattern
   clients), note it — those are exactly what a shallow scan misses.

## 1. Extract the stack (ground truth)

- Identify languages and package managers from manifests: `package.json`, `pyproject.toml` /
  `requirements.txt`, `go.mod`, `pom.xml` / `build.gradle`, `Cargo.toml`, `*.csproj`, `Gemfile`, etc.
- Note frameworks, runtimes, and pinned versions. Record databases, queues, and caches referenced in
  config or compose/manifest files.

## 2. Find the commands (for the toolchain note only)

- Locate build/test/run/lint commands in the repo (scripts sections, `Makefile`, `Taskfile`, CI
  workflows under `.github/workflows`, or `CONTRIBUTING`/README). Note the toolchain for the
  tech-stack draft, but **the repo is the source of truth** — the Coder and Verifier read the exact
  invocations from the repo at run time; don't copy them into `knowledge/`.

## 3. Map the architecture (the checklist)

Walk this checklist; it is language-agnostic. Mark any item **N/A** if the repo doesn't have it —
absence is information too.

- **Modules / bounded contexts** — top-level components and their responsibilities, from the
  directory layout and entry points (`main`, `cmd/`, `src/`, feature/route/controller folders).
- **Domain model** — the key data types / aggregates / entities the code is organized around.
- **Inbound APIs** — endpoints (HTTP/gRPC/GraphQL) grouped by area, with method + path; note auth.
- **Outbound integrations** — external services this repo calls, and the adapter/client pattern used.
- **Messaging** — events/topics published and consumed (queues, buses, streams). *Only if present.*
- **Workflows / state machines** — long-running processes, sagas, BPMN, schedulers. *Only if present.*
- **Data flows & boundaries** — how a request/event moves through the components; where the seams are.
- **Configuration & tenancy** — key config, environments/profiles, multi-tenancy model if any.
- **Observability & resilience** — logging/metrics/health; transactions, retries, idempotency.
- **Scheduled jobs** — cron/timer/queue-driven background work.

## 4. Surface risks, boundaries & gaps

- Notable third-party dependencies, and any that look outdated, security-sensitive, or load-bearing.
- **What this repo does NOT own** — concepts it delegates to other services (prevents over-claiming).
- **Not implemented** — resilience/scale patterns you specifically looked for and didn't find.
- Areas with no tests, heavy coupling, unclear ownership, or `TODO`/`FIXME` markers, with locations.

## 5. Output

Keep drafts at **overview level**; push exhaustive tables (full endpoint list, every aggregate field,
complete event catalog) into a clearly-labelled appendix section only when they're large enough to
warrant it — mirroring the progressive-disclosure model (overview in the file, detail on demand).
Emit the messaging/workflow sections only when those exist.

- **Characterize mode:** a draft for `system/tech-stack.md` (stack + toolchain) and
  `system/architecture.md` (modules, domain model, integrations, data flows, boundaries), each claim
  traceable to a file and tagged with confidence — **high** (stated in a manifest/config/annotation),
  **medium** (inferred from consistent code), **low** (a guess to confirm). Low-confidence items
  become open questions. Also emit the **provenance** for each drafted file — the repo(s) it was built
  from and the commit/branch you read (`{ type: repo, ref: <repo>, at: <commit-or-branch> }`) — so
  setup can write it into the file's `sources` frontmatter for later drift detection.
- **Roll-up (optional, multi-repo):** when asked, also emit a ~1–2 KB condensed summary of the repo
  (purpose, stack, key modules, integration points) suitable for a workspace-level architecture
  overview across the affected repos.
- **Drift mode:** given a git diff, return the `knowledge/**` files the change likely affects
  (e.g. an endpoint or dependency change → `architecture.md` / `tech-stack.md`), prioritized by
  `last_updated`, with a one-line reason each. Use each file's `sources` frontmatter to focus the
  check: a file is a refresh candidate when a repo it records has advanced past the recorded commit
  (`at`) in a way the diff touches — name that source in the reason.

Read-only: never edit files. Hand drafts back for setup/the user to approve and write.

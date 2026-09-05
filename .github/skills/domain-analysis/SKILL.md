---
name: domain-analysis
user-invocable: false
description: Procedure for distilling business/domain knowledge from Confluence (and Jira where useful) — product overview, glossary of domain terms, and stakeholders/ownership — to draft business/* knowledge. Keeps external/* as source pointers only. Used by the knowledge-scout subagent.
---

# Domain Analysis

A procedure to distil **business** knowledge from external sources into `business/*` drafts. Most of
this content lives in Confluence. Ground every statement in a page you actually read; link the
source, **tag your confidence**, and mark gaps or contradictions as open questions rather than
inventing.

## 1. Locate the sources

- Use `knowledge/external/INDEX.md` and `external/confluence.md` to find the relevant Confluence
  spaces and root pages; `external/jira.md` for project/board context where it clarifies ownership
  or terminology.

## 2. Distil, don't copy

- **Product overview** → draft `business/overview.md`: what the product does, who its users are, and
  the value it delivers, in a few tight paragraphs.
- **Glossary** → draft `business/glossary.md`: domain terms and acronyms with short, authoritative
  definitions.
- **Stakeholders** *(optional)* → draft `business/stakeholders.md`: which **role/team** owns/approves
  what (services, specs, infra). Use roles/teams, **never individual names**; skip if no clear source.

Summarize and synthesize — never paste whole pages. Raw content stays in Confluence and is fetched
on demand via the `retrieval` subagent.

## 3. Keep `external/*` as pointers

- Update `external/*` only as an **overview of where things live** (which space, which board, what
  lives where) — never as a copy of page content.

## 4. Output

- Drafts for `business/overview.md`, `business/glossary.md`, `business/stakeholders.md`, each claim
  **traceable to a source link and tagged with confidence** — **high** (stated on an authoritative
  page), **medium** (synthesised across pages), **low** (a guess to confirm).
- The **provenance** for each drafted file — the Confluence pages (with space) and Jira
  projects/boards it was distilled from (`{ type: confluence, ref: <page>, space: <key> }`,
  `{ type: jira, ref: <key> }`) — so setup can write it into the file's `sources` frontmatter and the
  knowledge agent can later detect when one of those pages/projects has changed.
- A **gaps & contradictions** list: terms with no owner or definition, pages that disagree, and areas
  where no source exists — surfaced as open questions for the user, never invented answers.

Read-only: never edit files. Hand drafts back for setup/the user to approve and write.

#!/usr/bin/env python3
"""Deterministic structural linter for a spec's `status.json` working-state file.

The two orchestrators keep `specs/{slug}/status.json` as a machine-readable blackboard of where a
spec stands (which subagents ran, the Definition-of-Ready boxes, per-repo branches/PRs, per-task
results). Because it is JSON with a fixed shape, its structure can be checked *deterministically*
instead of by eyeballing prose — that is what this script does, mirroring `validate_spec.py`.

Philosophy (matches the artifact contract: "status is continuity, never a gate")
--------------------------------------------------------------------------------
  • ERROR (exit 1)  — the file is structurally broken: invalid JSON, not an object, a required
                      top-level key missing, an out-of-range enum value, or a field that must be a
                      boolean/list holding the wrong type.
  • WARNING (exit 0) — advisory: an unfilled `{template-token}`, or an unknown key (likely a typo).
                       Never blocks — a partially-filled status file is normal mid-phase.

Usage
-----
  python3 validate_status.py [PATH ...]   # status.json files and/or spec dirs (default: cwd)
  python3 validate_status.py --json       # machine-readable findings for the agent

Pure standard library — no third-party deps, so it runs anywhere Python 3.8+ is available. Leftover
`{tokens}` are ordinary JSON strings, so the template parses cleanly before its fields are filled.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Tuple

STATUS_FILENAME = "status.json"

# A single finding, decoupled from its file: rules yield (level, message) pairs and the file loop
# stamps in the path once (see `validate_file`).
Level = str  # "error" | "warning"
RawFinding = Tuple[Level, str]


@dataclass(frozen=True)
class Finding:
    level: Level            # "error" | "warning"
    path: str               # the status.json file this finding is about
    message: str

    def as_dict(self) -> dict:
        return {"level": self.level, "file": self.path, "message": self.message}


# --- the schema (fixed, unlike validate_spec.py which derives from the template) ----------------
# Everything the linter knows about status.json lives here as data, so adding a field is a one-line
# edit rather than another hand-written `if` block. The three allowed-value vocabularies:
SUBAGENT_STATES = frozenset({"not-run", "in-progress", "done"})
REPO_STATES = frozenset({"in-progress", "blocked", "done"})
TASK_RESULTS = frozenset({"pending", "passed", "blocked"})

REQUIRED_TOP = ("spec", "phase", "updated")
KNOWN_TOP = frozenset({"spec", "phase", "updated", "requirements", "implementation"})

TOKEN_RE = re.compile(r"\{[A-Za-z][\w -]*\}")

_MISSING = object()  # sentinel: distinguishes "key absent" from "value is null" for boolean checks


def _is_token(value) -> bool:
    """True if `value` still carries an unfilled `{template-token}`."""
    return isinstance(value, str) and TOKEN_RE.search(value) is not None


def _dig(data: dict, dotted: str, default=None):
    """Walk a dotted path (`a.b.c`) through nested mappings, returning `default` if it dead-ends."""
    node = data
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


class Rule:
    """A single declarative check. `check` yields `(level, message)` pairs, path-free."""

    def check(self, data: dict) -> Iterator[RawFinding]:  # pragma: no cover - interface
        raise NotImplementedError


@dataclass(frozen=True)
class EnumRule(Rule):
    """A scalar at `dotted` must be one of `allowed` (a leftover `{token}` counts as unfilled)."""

    dotted: str
    allowed: frozenset

    def check(self, data: dict) -> Iterator[RawFinding]:
        value = _dig(data, self.dotted)
        if value is None or _is_token(value):
            return
        if not isinstance(value, str) or value not in self.allowed:
            yield "error", f"`{self.dotted}` is `{value}` — expected one of {sorted(self.allowed)}"


@dataclass(frozen=True)
class BoolRule(Rule):
    """A field at `dotted`, when present, must be a real boolean."""

    dotted: str

    def check(self, data: dict) -> Iterator[RawFinding]:
        value = _dig(data, self.dotted, _MISSING)
        if value is not _MISSING and not isinstance(value, bool):
            yield "error", f"`{self.dotted}` must be true/false"


@dataclass(frozen=True)
class ListRule(Rule):
    """A list-of-mappings at `dotted`; each item needs `required` keys and a valid enum field."""

    dotted: str
    label: str                              # singular noun for messages: "repo", "task", ...
    id_key: str                             # key used to name an item in messages
    enum_field: str                         # per-item field constrained to `allowed`
    allowed: frozenset
    required: tuple = ()

    def check(self, data: dict) -> Iterator[RawFinding]:
        node = _dig(data, self.dotted)
        if node in (None, []):
            return
        if not isinstance(node, list):
            yield "error", f"`{self.dotted}` must be a list"
            return
        for idx, item in enumerate(node):
            if not isinstance(item, dict):
                yield "error", f"`{self.dotted}[{idx}]` must be a mapping"
                continue
            for key in self.required:
                if not item.get(key):
                    yield "error", f"`{self.dotted}[{idx}]` is missing `{key}`"
            value = item.get(self.enum_field)
            if value is not None and not _is_token(value) and value not in self.allowed:
                name = item.get(self.id_key, idx)
                yield "error", (f"{self.label} `{name}` {self.enum_field} `{value}` — "
                                f"expected one of {sorted(self.allowed)}")


@dataclass(frozen=True)
class DoneRepoHasPrRule(Rule):
    """Consistency (not structure): a repo marked `done` should carry a recorded commit/PR.

    Emitted as a **warning**, never an error — this file is "continuity, never a gate", and a
    structurally valid status is still valid without a PR link. But a `done` repo whose
    `commit_or_pr` is empty/`none`/still a `{token}` is the exact stale-write footprint that strands
    a spec showing `in-progress`-with-no-PR-button in the extension (the PR button renders only from a
    real PR URL here): the status was written before the push/PR existed and never corrected. Surface
    it so the orchestrator's done-self-check catches it deterministically instead of by eyeballing.
    """

    def check(self, data: dict) -> Iterator[RawFinding]:
        repos = _dig(data, "implementation.repos")
        if not isinstance(repos, list):
            return
        for idx, item in enumerate(repos):
            if not isinstance(item, dict) or item.get("state") != "done":
                continue
            cell = item.get("commit_or_pr")
            recorded = isinstance(cell, str) and cell.strip().lower() not in ("", "none") \
                and not _is_token(cell)
            if not recorded:
                name = item.get("repo", idx)
                yield "warning", (f"repo `{name}` is `state: done` but `commit_or_pr` is "
                                  f"`{cell}` — no commit/PR recorded, so the extension will show no "
                                  f"PR button; if the PR exists, write its URL here")


# Ordered so findings surface top-to-bottom as they appear in the file.
SCHEMA: tuple[Rule, ...] = (
    EnumRule("phase", frozenset({"requirements", "implementation"})),
    EnumRule("requirements.entry_point", frozenset({"idea", "prd", "technical"})),
    EnumRule("requirements.confidence", frozenset({"high", "medium", "low"})),
    EnumRule("requirements.subagents.business_analyst", SUBAGENT_STATES),
    EnumRule("requirements.subagents.tech_analyst", SUBAGENT_STATES),
    EnumRule("requirements.awaiting", frozenset({"nothing", "user-answers", "user-approval"})),
    ListRule("requirements.subagents.specialists", "specialist", "name", "state", SUBAGENT_STATES),
    BoolRule("requirements.definition_of_ready.acceptance_criteria_testable"),
    BoolRule("requirements.definition_of_ready.out_of_scope_present"),
    BoolRule("requirements.definition_of_ready.repos_affected_filled"),
    BoolRule("requirements.definition_of_ready.open_questions_resolved"),
    BoolRule("requirements.definition_of_ready.depends_on_listed"),
    BoolRule("implementation.baseline.captured"),
    ListRule("implementation.repos", "repo", "repo", "state", REPO_STATES, required=("repo",)),
    ListRule("implementation.tasks", "task", "id", "result", TASK_RESULTS),
    DoneRepoHasPrRule(),
)


# --- validation ---------------------------------------------------------------------------------

def _token_warnings(node, path: str = "") -> Iterator[RawFinding]:
    """Advisory warning for every unfilled `{token}` anywhere in the tree."""
    if isinstance(node, dict):
        for key, value in node.items():
            yield from _token_warnings(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            yield from _token_warnings(value, f"{path}[{idx}]")
    elif _is_token(node):
        yield "warning", f"`{path}` still holds a template placeholder `{node}`"


def _analyze(data: dict) -> Iterator[RawFinding]:
    """Yield every `(level, message)` finding for an already-parsed status mapping."""
    for key in REQUIRED_TOP:
        if key not in data or data[key] in (None, ""):
            yield "error", f"missing required key `{key}`"

    for key in data:  # typo guard
        if key not in KNOWN_TOP:
            yield "warning", f"unknown top-level key `{key}`"

    for rule in SCHEMA:
        yield from rule.check(data)

    yield from _token_warnings(data)


def validate_file(path: Path) -> list[Finding]:
    rel = str(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        return [Finding("error", rel, f"cannot read file: {e}")]

    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return [Finding("error", rel, f"invalid JSON: {e}")]
    if not isinstance(data, dict):
        return [Finding("error", rel, "top level is not an object")]

    return [Finding(level, rel, message) for level, message in _analyze(data)]


def collect_paths(paths: list[str]) -> list[Path]:
    files: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_dir():
            direct = path / STATUS_FILENAME
            if direct.exists():
                files.append(direct)
            else:
                files.extend(sorted(path.rglob(STATUS_FILENAME)))
        else:
            files.append(path)
    return files


def main() -> int:
    ap = argparse.ArgumentParser(description="Structural linter for spec status.json files.")
    ap.add_argument("paths", nargs="*", default=["."],
                    help="status.json files and/or spec dirs (default: current dir)")
    ap.add_argument("--json", action="store_true", help="machine-readable findings")
    args = ap.parse_args()

    files = collect_paths(args.paths or ["."])
    if not files:
        msg = "no status.json files found"
        print(json.dumps({"findings": [], "note": msg}) if args.json else msg)
        return 0

    findings: list[Finding] = []
    for f in files:
        findings.extend(validate_file(f))

    errors = [f for f in findings if f.level == "error"]

    if args.json:
        print(json.dumps({"findings": [f.as_dict() for f in findings],
                          "errors": len(errors),
                          "warnings": len(findings) - len(errors)}, indent=2))
    else:
        for f in findings:
            print(f"{f.level.upper():7} {f.path}: {f.message}")
        print(f"\nChecked {len(files)} file(s) — {len(errors)} error(s), "
              f"{len(findings) - len(errors)} warning(s).")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

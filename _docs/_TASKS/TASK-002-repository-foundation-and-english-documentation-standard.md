[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-002: Repository Foundation and English Documentation Standard
# FileName: TASK-002-repository-foundation-and-english-documentation-standard.md

**Priority:** High
**Category:** Repository Foundation
**Estimated Effort:** Large
**Dependencies:** TASK-001
**Status:** **Done** (2026-03-13)

---

## Overview

Create the repository collaboration foundation needed before implementation starts in earnest.

Business goal:
- install repository-level quality gates before code work begins
- introduce `docs/` as the official application documentation space
- clarify repository ownership and contribution expectations
- move all Markdown documentation to English

---

## Sub-Tasks

### TASK-002-01: Pre-commit, official docs structure, and collaboration files

**Status:** Done

Create `.pre-commit-config.yaml`, official docs indexes, repository metadata, and contribution workflow files.

### TASK-002-02: English Markdown migration and documentation split

**Status:** Done

Translate repository Markdown files to English and codify English-only Markdown policy in `AGENTS.md`.

---

## Implementation Order

1. Inspect the repository state on the current implementation branch.
2. Add repository-level metadata and quality guardrails.
3. Create the new `docs/` structure with clear ownership rules.
4. Translate and align all Markdown files in the repository.
5. Update the task board and changelog history.

---

## Testing Requirements

- verify that `.pre-commit-config.yaml` covers repository text, docs, and future Python quality gates
- verify that every directory in `docs/` and `_docs/` has a `README.md`
- verify that all changed Markdown files are in English
- verify that task board and changelog indexes reflect the completed work

---

## Documentation Updates Required

- `README.md`
- `AGENTS.md`
- `CONTRIBUTING.md`
- `docs/README.md` and subdirectory indexes
- `_docs/README.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
- new task and changelog entries for TASK-002

[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-001: Repository Governance and Documentation Workflow
# FileName: TASK-001-repo-governance-i-workflow-dokumentacji.md

**Priority:** High
**Category:** Repository Governance
**Estimated Effort:** Medium
**Dependencies:** None
**Status:** **Done** (2026-03-13)

---

## Overview

Define the working rules for the repository so that every future implementation task follows one explicit workflow.

Business goal:
- establish a single source of truth for repository rules
- align task, documentation, and changelog workflow
- ensure future implementation work stays consistent with `_docs/_MVP/`

---

## Sub-Tasks

### TASK-001-01: `AGENTS.md` and task/changelog rules

**Status:** Done

Translate the MVP guidance into executable repository rules, task hierarchy, documentation navigation rules, and changelog updates.

---

## Implementation Order

1. Analyze all of `_docs/`, especially `_MVP`, `_TASKS`, and `_CHANGELOG`.
2. Record the repository rules and workflow in the main `AGENTS.md`.
3. Add missing documentation indexes (`README.md` in the root and `_docs/`).
4. Align the task and changelog README files with the workflow.
5. Document the completed work in the changelog and board.

---

## Testing Requirements

- verify that the rules are consistent with `_docs/_MVP/`
- verify that the task board and changelog index reflect the completed work
- verify that new and updated Markdown files include navigation controls

---

## Documentation Updates Required

- create the main `AGENTS.md`
- add the root `README.md`
- add `_docs/README.md`
- update `_docs/_TASKS/README.md`
- update `_docs/_CHANGELOG/README.md`
- add a changelog entry in `_docs/_CHANGELOG/`

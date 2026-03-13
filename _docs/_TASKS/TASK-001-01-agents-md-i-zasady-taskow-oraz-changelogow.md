[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-001-01: `AGENTS.md` and Task / Changelog Rules
# FileName: TASK-001-01-agents-md-i-zasady-taskow-oraz-changelogow.md

**Priority:** High
**Category:** Documentation Process
**Estimated Effort:** Medium
**Dependencies:** TASK-001
**Status:** **Done** (2026-03-13)

---

## Overview

Technical subtask that established working rules for both humans and agents in the repository.

Scope:
- extract product and implementation rules from `_docs/_MVP/`
- store them in `AGENTS.md`
- define task hierarchy and naming convention
- define documentation navigation rules
- align `_TASKS` and `_CHANGELOG` indexes with the workflow

---

## Architecture

Target state after completing the subtask:

```text
model-traffic-manager/
|-- README.md
|-- AGENTS.md
`-- _docs/
    |-- README.md
    |-- _MVP/
    |   `-- README.md
    |-- _TASKS/
    |   |-- README.md
    |   |-- EXAMPLE_TASK.md
    |   |-- TASK-001-repo-governance-i-workflow-dokumentacji.md
    |   `-- TASK-001-01-agents-md-i-zasady-taskow-oraz-changelogow.md
    `-- _CHANGELOG/
        |-- README.md
        |-- EXAMPLE_CHANGELOG.md
        `-- 1-2026-03-13-repo-governance-task-workflow-and-agents-rules.md
```

---

## Pseudocode

```text
on_every_repo_task():
    create main task file TASK-XXX-english-slug.md
    create technical subtask TASK-XXX-01-english-slug.md
    if the subtask becomes too large:
        split into TASK-XXX-01-01-english-slug.md or deeper
    write Documentation Updates Required in every work item
    execute the work
    create a changelog entry with all completed IDs
    update the _docs/_TASKS/README.md board
    update the _docs/_CHANGELOG/README.md index
```

---

## Implementation Order

1. Identify the rules implied by `_docs/_MVP/`.
2. Turn them into operational instructions in `AGENTS.md`.
3. Add task hierarchy and changelog workflow rules.
4. Add indexes and navigation controls for the documentation.
5. Update the board and changelog index.

---

## Testing Requirements

- verify that `AGENTS.md` covers product scope, architecture, stack, routing, auth, and tests
- verify that the task README explains main tasks, subtasks, and deeper breakdown levels
- verify that the changelog index contains the new entry
- verify that the Markdown files changed by the task expose navigation links

---

## Documentation Updates Required

- `README.md`
- `AGENTS.md`
- `_docs/README.md`
- `_docs/_TASKS/README.md`
- `_docs/_TASKS/EXAMPLE_TASK.md`
- `_docs/_CHANGELOG/README.md`
- `_docs/_CHANGELOG/EXAMPLE_CHANGELOG.md`
- `_docs/_CHANGELOG/1-2026-03-13-repo-governance-task-workflow-and-agents-rules.md`

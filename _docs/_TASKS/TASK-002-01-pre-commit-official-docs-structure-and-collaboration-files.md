[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-002-01: Pre-Commit, Official Docs Structure, and Collaboration Files
# FileName: TASK-002-01-pre-commit-official-docs-structure-and-collaboration-files.md

**Priority:** High
**Category:** Repository Process
**Estimated Effort:** Medium
**Dependencies:** TASK-002
**Status:** **Done** (2026-03-13)

---

## Overview

Technical subtask that establishes the repository collaboration baseline before runtime code is added.

Scope:
- add `.pre-commit-config.yaml`
- add local pre-commit scripts for repository-specific guardrails
- add `docs/` and its initial documentation map
- expand repository metadata files such as `README.md`, `CONTRIBUTING.md`, and PR template

---

## Architecture

Target structure added by this subtask:

```text
model-traffic-manager/
|-- .pre-commit-config.yaml
|-- CONTRIBUTING.md
|-- .github/PULL_REQUEST_TEMPLATE.md
|-- docs/
|   |-- README.md
|   |-- getting-started/README.md
|   |-- architecture/README.md
|   |-- configuration/README.md
|   |-- routing/README.md
|   |-- operations/README.md
|   `-- reference/README.md
`-- scripts/pre_commit/
    |-- check_text_guardrails.py
    |-- check_docs_guardrails.py
    `-- run_repo_quality_gate.py
```

---

## Pseudocode

```text
on_pre_commit():
    run text guardrails on changed text files
    run documentation structure guardrails
    if the Python application scaffold exists:
        run ruff, mypy, and pytest coverage gate
```

---

## Implementation Order

1. Add local pre-commit scripts that do not depend on external hook repositories.
2. Wire the scripts into `.pre-commit-config.yaml`.
3. Create the official `docs/` structure and explain why it is separate from `_docs/`.
4. Add contribution and pull request workflow files.

---

## Testing Requirements

- compile the pre-commit Python scripts
- run the repository guardrail scripts directly
- verify local documentation links in `docs/` and repository metadata files

---

## Documentation Updates Required

- `README.md`
- `CONTRIBUTING.md`
- `docs/README.md`
- `docs/getting-started/README.md`
- `docs/architecture/README.md`
- `docs/configuration/README.md`
- `docs/routing/README.md`
- `docs/operations/README.md`
- `docs/reference/README.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`

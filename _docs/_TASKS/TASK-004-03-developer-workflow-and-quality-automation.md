[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-004-03: Developer Workflow and Quality Automation
# FileName: TASK-004-03-developer-workflow-and-quality-automation.md

**Priority:** High
**Category:** Developer Experience
**Estimated Effort:** Medium
**Dependencies:** TASK-004-02
**Status:** **Done** (2026-03-13)

---

## Overview

Make the bootstrap runnable and checkable through one clear local and CI workflow.

Scope:
- define canonical local commands
- add CI workflow
- ensure local commands, pre-commit, and CI remain aligned

---

## Sub-Tasks

### TASK-004-03-01: Canonical local commands and task runner

**Status:** Done (2026-03-13)

Create one repository-level command surface for bootstrap, lint, type-check, tests, and app run flows.

### TASK-004-03-02: CI workflow and pre-commit parity

**Status:** Done (2026-03-13)

Make sure the same validation model runs both locally and in CI.

---

## Target Structure

```text
Makefile
.github/workflows/ci.yml
.pre-commit-config.yaml
```

---

## Pseudocode

```text
local_check():
    make bootstrap
    make lint
    make typecheck
    make test

ci_check():
    checkout
    setup python/uv
    sync environment
    run the same commands as local_check()
```

---

## Testing Requirements

- local task runner commands map to real project actions
- CI uses the same quality contract instead of a divergent one
- pre-commit and CI do not disagree on basic repository guardrails

---

## Documentation Updates Required

- `README.md`
- `CONTRIBUTING.md`
- `docs/getting-started/README.md`
- `_docs/_TASKS/TASK-004-03-developer-workflow-and-quality-automation.md`
- `_docs/_TASKS/TASK-004-03-01-canonical-local-commands-and-task-runner.md`
- `_docs/_TASKS/TASK-004-03-02-ci-workflow-and-pre-commit-parity.md`

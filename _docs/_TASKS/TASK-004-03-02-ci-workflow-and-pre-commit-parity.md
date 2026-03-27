[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-004-03-02: CI Workflow and Pre-Commit Parity
# FileName: TASK-004-03-02-ci-workflow-and-pre-commit-parity.md

**Priority:** High
**Category:** Developer Experience
**Estimated Effort:** Medium
**Dependencies:** TASK-004-03
**Status:** **Done** (2026-03-13)

---

## Overview

Ensure that CI validates the same repository contract contributors are expected to run locally.

This work item owns:
- `.github/workflows/ci.yml`
- the mapping between `pre-commit`, `Makefile`, and CI

---

## Target File

```text
.github/workflows/ci.yml
```

---

## Pseudocode

```text
ci_pipeline():
    setup python 3.12
    install uv
    sync dependencies
    run pre-commit
    run make check
```

---

## Detailed Work Items

1. Add a pull-request workflow for the implementation branch workflow.
2. Use the same Python version and dependency sync path as local development.
3. Run `pre-commit` and the aggregate local quality command, not a custom hidden CI-only sequence.
4. Define a simple cache strategy for `uv` artifacts if it materially speeds up CI.

---

## Testing Requirements

- CI definition is syntactically valid
- CI command sequence mirrors local quality flow
- CI does not skip checks that are mandatory before merge

---

## Documentation Updates Required

- `CONTRIBUTING.md`
- `docs/getting-started/README.md`
- `_docs/_TASKS/TASK-004-03-02-ci-workflow-and-pre-commit-parity.md`

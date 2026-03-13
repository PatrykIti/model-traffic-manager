[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-004-03-01: Canonical Local Commands and Task Runner
# FileName: TASK-004-03-01-canonical-local-commands-and-task-runner.md

**Priority:** High
**Category:** Developer Experience
**Estimated Effort:** Medium
**Dependencies:** TASK-004-03
**Status:** **Done** (2026-03-13)

---

## Overview

Define the single local command surface contributors should use once the Python scaffold exists.

Decision:
- use `Makefile` as the canonical task runner

---

## Target File

```text
Makefile
```

---

## Command Contract

Required targets:

- `bootstrap`
- `lock`
- `lint`
- `typecheck`
- `test`
- `check`
- `run`
- `docker-build`

Optional targets if helpful:

- `format`
- `clean`
- `smoke`

---

## Pseudocode

```text
make check:
    make lint
    make typecheck
    make test
```

---

## Testing Requirements

- every target executes a real command path
- `check` is the single aggregate command used by contributors and CI
- command naming is reflected consistently in `README.md` and `CONTRIBUTING.md`

---

## Documentation Updates Required

- `README.md`
- `CONTRIBUTING.md`
- `docs/getting-started/README.md`
- `_docs/_TASKS/TASK-004-03-01-canonical-local-commands-and-task-runner.md`

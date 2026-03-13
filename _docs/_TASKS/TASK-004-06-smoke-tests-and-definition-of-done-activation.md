[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-004-06: Smoke Tests and Definition-of-Done Activation
# FileName: TASK-004-06-smoke-tests-and-definition-of-done-activation.md

**Priority:** High
**Category:** Quality Assurance
**Estimated Effort:** Medium
**Dependencies:** TASK-004-02, TASK-004-03, TASK-004-04
**Status:** **Done** (2026-03-13)

---

## Overview

Close Phase 0 by proving the repository bootstrap is runnable and guarded by validation.

Scope:
- startup smoke tests
- health endpoint tests
- quality gate activation once `app/`, `tests/`, and `pyproject.toml` exist
- final alignment between local commands, pre-commit, and CI

---

## Target Structure

```text
tests/
|-- unit/
|   `-- entrypoints/api/test_health.py
`-- integration/
    `-- api/test_startup.py
```

---

## Pseudocode

```text
smoke_validation():
    import app
    start test client
    call /health/live
    call /health/ready
    run lint, typecheck, and tests through the canonical check command
```

---

## Detailed Work Items

1. Add unit coverage for health route behavior.
2. Add integration coverage for app startup and route registration.
3. Switch the repository quality gate from "skip because scaffold missing" to "execute because scaffold exists".
4. Ensure `Makefile`, `pre-commit`, and CI all exercise the same bootstrap checks.

---

## Testing Requirements

- health route unit tests pass
- startup integration test passes
- `scripts/pre_commit/run_repo_quality_gate.py` stops skipping once the scaffold is present
- `make check` and CI both cover the same bootstrap contract

---

## Documentation Updates Required

- `CONTRIBUTING.md`
- `docs/getting-started/README.md`
- `docs/operations/README.md`
- `_docs/_TASKS/TASK-004-06-smoke-tests-and-definition-of-done-activation.md`

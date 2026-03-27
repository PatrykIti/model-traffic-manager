[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-007-01: Official and Repository-Level Testing Policy Update
# FileName: TASK-007-01-official-and-repository-level-testing-policy-update.md

**Priority:** High
**Category:** Testing Strategy
**Estimated Effort:** Small
**Dependencies:** TASK-007
**Status:** **Done** (2026-03-13)

---

## Overview

Document the layered testing policy in both the official docs and repository operating rules.

Scope:
- define `unit`, `integration-local`, `integration-azure`, and `e2e-aks`
- define which phases require which levels
- define the rule that higher-level tests do not replace lower-level tests

---

## Testing Requirements

- the testing model is explicit and phase-aware
- lower-level test suites remain mandatory after higher-level environments are added
- local links and navigation controls remain valid

---

## Documentation Updates Required

- `AGENTS.md`
- `docs/operations/testing-levels-and-environments.md`
- `docs/operations/README.md`

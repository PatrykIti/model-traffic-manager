[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009-03-01: Single-Upstream Candidate Selection from the Deployment Registry
# FileName: TASK-009-03-01-single-upstream-candidate-selection-from-the-deployment-registry.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-009-03
**Status:** To Do

---

## Overview

Define the minimal selection rule before failover exists.

Decision target:
- for Phase 2, select the only upstream or the first upstream deterministically
- make this explicit in code so it can later be replaced by real routing policy

---

## Testing Requirements

- selection behavior is deterministic
- empty upstream case is handled before outbound invocation begins

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-009-03-01-single-upstream-candidate-selection-from-the-deployment-registry.md`

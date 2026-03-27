[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-016-03: `integration-azure` and `e2e-aks` Activation
# FileName: TASK-016-03-integration-azure-and-e2e-aks-activation.md

**Priority:** High
**Category:** Validation Infrastructure
**Estimated Effort:** Large
**Dependencies:** TASK-008, TASK-016
**Status:** **Done** (2026-03-14)

---

## Overview

Activate the higher-level validation model already planned in the repository.

Detailed work:
1. Implement `integration-azure` coverage for Managed Identity and Azure-native outbound auth scenarios.
2. Add the first `e2e-aks` proof for deployment, identity, and runtime behavior.
3. Keep temporary Azure environments explicitly triggered, bounded, and always destroyed.

---

## Testing Requirements

- `integration-azure` remains narrower and cheaper than `e2e-aks`
- AKS-backed runs are opt-in and always cleaned up
- workflow artifacts and failure output are sufficient for debugging without rerunning blindly

---

## Documentation Updates Required

- `docs/operations/testing-levels-and-environments.md`
- `_docs/_TASKS/TASK-016-03-integration-azure-and-e2e-aks-activation.md`

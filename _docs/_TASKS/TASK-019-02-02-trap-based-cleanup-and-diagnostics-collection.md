[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-019-02-02: Trap-Based Cleanup and Diagnostics Collection
# FileName: TASK-019-02-02-trap-based-cleanup-and-diagnostics-collection.md

**Priority:** High
**Category:** Developer Workflow
**Estimated Effort:** Small
**Dependencies:** TASK-019-02
**Status:** **Done** (2026-03-14)

---

## Overview

Guarantee local cleanup and collect enough diagnostics for AKS-backed failures.

---

## Testing Requirements

- `terraform destroy` is attempted under shell traps
- port-forward and temporary runtime processes are cleaned up
- cluster diagnostics are collected before destroy

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-019-02-02-trap-based-cleanup-and-diagnostics-collection.md`

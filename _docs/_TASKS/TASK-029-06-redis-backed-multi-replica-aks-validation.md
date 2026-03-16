[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029](./TASK-029-live-azure-validation-expansion-for-router-surfaces.md)

# TASK-029-06: Redis-Backed Multi-Replica AKS Validation
# FileName: TASK-029-06-redis-backed-multi-replica-aks-validation.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029, TASK-029-01
**Status:** **To Do**

---

## Overview

Add a dedicated AKS profile that proves the router behaves correctly with multiple replicas and Redis-backed shared runtime state.

Candidate checks:
- cooldown visibility across replicas
- circuit-open visibility across replicas
- request-rate and concurrency behavior across replicas
- failover stability with shared state enabled

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-029-06-redis-backed-multi-replica-aks-validation.md`

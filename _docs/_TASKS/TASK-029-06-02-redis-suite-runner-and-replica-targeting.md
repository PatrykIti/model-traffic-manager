[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029-06](./TASK-029-06-redis-backed-multi-replica-aks-validation.md)

# TASK-029-06-02: Redis Suite Runner and Replica Targeting
# FileName: TASK-029-06-02-redis-suite-runner-and-replica-targeting.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029-06-01
**Status:** **Done** (2026-03-18)

---

## Overview

Extend the shared Azure/AKS runner to support a dedicated Redis-backed suite with per-replica port-forward targeting.

## Documentation Updates Required

- `scripts/release/run_azure_test_suite.sh`
- `Makefile`
- `.env.example`

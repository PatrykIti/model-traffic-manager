[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029](./TASK-029-live-azure-validation-expansion-for-router-surfaces.md)

# TASK-029-06: Redis-Backed Multi-Replica AKS Validation
# FileName: TASK-029-06-redis-backed-multi-replica-aks-validation.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029, TASK-029-01
**Status:** **Done** (2026-03-18)

---

## Overview

Add a dedicated AKS profile that proves the router behaves correctly with multiple replicas and Redis-backed shared runtime state.

Candidate checks:
- cooldown visibility across replicas
- circuit-open visibility across replicas
- request-rate and concurrency behavior across replicas
- failover stability with shared state enabled

## Sub-Tasks

### TASK-029-06-01: Redis AKS scope and multi-replica router profile

**Status:** Done (2026-03-18)

Add a dedicated AKS scope with two router replicas and an in-cluster Redis backend.

### TASK-029-06-02: Redis suite runner and replica targeting

**Status:** Done (2026-03-18)

Extend the shared Azure/AKS runner with per-replica port-forward targeting for the Redis suite.

### TASK-029-06-03: Redis multi-replica live suite and docs rollout

**Status:** Done (2026-03-18)

Add the dedicated live suite, make target, and docs for Redis-backed multi-replica validation.

---

## Documentation Updates Required

- `infra/e2e-aks-redis/`
- `scripts/release/render_live_redis_router_config.py`
- `scripts/release/run_azure_test_suite.sh`
- `tests/e2e_aks_redis/`
- `Makefile`
- `.env.example`
- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
- `docs/getting-started/implementation-status.md`
- `_docs/_TASKS/TASK-029-06-redis-backed-multi-replica-aks-validation.md`
- `_docs/_TASKS/TASK-029-06-01-redis-aks-scope-and-multi-replica-router-profile.md`
- `_docs/_TASKS/TASK-029-06-02-redis-suite-runner-and-replica-targeting.md`
- `_docs/_TASKS/TASK-029-06-03-redis-multi-replica-live-suite-and-docs-rollout.md`

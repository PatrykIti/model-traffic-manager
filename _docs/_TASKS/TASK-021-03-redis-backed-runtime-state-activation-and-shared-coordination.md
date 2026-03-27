[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-021](./TASK-021-mvp-closure-runtime-state-activation-and-contract-hardening.md)

# TASK-021-03: Redis-Backed Runtime State Activation and Shared Coordination
# FileName: TASK-021-03-redis-backed-runtime-state-activation-and-shared-coordination.md

**Priority:** High
**Category:** Infrastructure and Runtime Wiring
**Estimated Effort:** Medium
**Dependencies:** TASK-021, TASK-014, TASK-015
**Status:** **Done** (2026-03-15)

---

## Overview

The repository already contains Redis-backed adapters for health and limits, but the active runtime still boots only in-memory state. This task activates the shared-state path needed for multi-instance deployments.

Detailed work:
1. Add runtime settings for state backend selection and Redis connection details.
2. Build a Redis client in bootstrap only when requested.
3. Wire Redis-backed health, request-rate, and concurrency adapters into the active container.
4. Preserve in-memory defaults for local development and tests.
5. Close runtime resources cleanly on shutdown.

---

## Testing Requirements

- settings coverage for state-backend selection
- container wiring tests for in-memory and Redis-backed modes
- adapter behavior tests remain deterministic without a real Redis server
- local integration tests still pass in the default in-memory mode

---

## Documentation Updates Required

- `docs/operations/deployment-model.md`
- `docs/routing/failover-and-health.md`
- `docs/getting-started/implementation-status.md`
- `_docs/_TASKS/TASK-021-03-redis-backed-runtime-state-activation-and-shared-coordination.md`

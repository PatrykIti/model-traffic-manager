[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-029: Live Azure Validation Expansion for Router Surfaces
# FileName: TASK-029-live-azure-validation-expansion-for-router-surfaces.md

**Priority:** High
**Category:** Validation Planning
**Estimated Effort:** Large
**Dependencies:** TASK-020, TASK-024, TASK-028
**Status:** **Done** (2026-03-16)

---

## Overview

Define the next live Azure validation profiles so every important router surface can be exercised against real Azure-backed environments instead of only local or synthetic tests.

Business goal:
- move beyond the current minimal live coverage
- prove chat, embeddings, shared-service execution, failover behavior, and shared runtime state with live infra
- keep each validation profile small enough to run intentionally and diagnose clearly

Key planning rule:
- do not collapse everything into one giant expensive suite
- split the matrix by behavior and dependency class so failures stay attributable

---

## Sub-Tasks

### TASK-029-01: Live Azure validation matrix and profile taxonomy

**Status:** Done (2026-03-16)

Define the target validation matrix across `integration-azure`, `e2e-aks`, and `e2e-aks-live-model`.

### TASK-029-02: `integration-azure` outbound provider probes for chat and embeddings

**Status:** To Do

Add lower-level Azure-backed checks that prove outbound auth and direct provider responses for both chat-related and embeddings-related dependencies.

### TASK-029-03: `e2e-aks-live-model` embeddings profile

**Status:** To Do

Add a live embeddings path through the router on AKS with real Azure OpenAI embeddings infrastructure.

### TASK-029-04: `e2e-aks-live-model` chat failover and health-state scenarios

**Status:** To Do

Add live cases that prove regional/account/model failover, cooldown, and circuit behavior for chat deployments.

### TASK-029-05: Live shared-services validation on Azure and AKS

**Status:** To Do

Add live validation for `router_proxy + single_endpoint`, `router_proxy + tiered_failover`, and direct-access shared-service semantics.

### TASK-029-06: Redis-backed multi-replica AKS validation

**Status:** To Do

Add live validation that proves health, cooldown, and limiter coordination across replicas with Redis-backed runtime state.

### TASK-029-07: Runner, workflow, and documentation rollout for expanded live suites

**Status:** To Do

Align local runners, CI workflows, env vars, and docs with the expanded live validation matrix.

---

## Validation Matrix

Recommended split:

1. `integration-azure`
   live auth and provider probes without AKS
2. `e2e-aks`
   cluster smoke plus infra/runtime wiring
3. `e2e-aks-live-model`
   real routed chat and embeddings, plus failover scenarios
4. dedicated Redis-backed AKS profile
   multi-replica coordination and state sharing proof
5. dedicated shared-service live profile
   router-proxied internal service execution and direct-access boundary checks

---

## Documentation Updates Required

- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-029-live-azure-validation-expansion-for-router-surfaces.md`
- `_docs/_TASKS/TASK-029-01-live-azure-validation-matrix-and-profile-taxonomy.md`
- `_docs/_TASKS/TASK-029-02-integration-azure-outbound-provider-probes-for-chat-and-embeddings.md`
- `_docs/_TASKS/TASK-029-03-e2e-aks-live-model-embeddings-profile.md`
- `_docs/_TASKS/TASK-029-04-e2e-aks-live-model-chat-failover-and-health-state-scenarios.md`
- `_docs/_TASKS/TASK-029-05-live-shared-services-validation-on-azure-and-aks.md`
- `_docs/_TASKS/TASK-029-06-redis-backed-multi-replica-aks-validation.md`
- `_docs/_TASKS/TASK-029-07-runner-workflow-and-documentation-rollout-for-expanded-live-suites.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`

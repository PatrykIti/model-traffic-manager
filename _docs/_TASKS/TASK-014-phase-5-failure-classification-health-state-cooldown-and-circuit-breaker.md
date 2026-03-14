[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-014: Phase 5 Failure Classification, Health State, Cooldown, and Circuit Breaker
# FileName: TASK-014-phase-5-failure-classification-health-state-cooldown-and-circuit-breaker.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Large
**Dependencies:** TASK-013
**Status:** **To Do**

---

## Overview

Add the health-state behavior that turns basic failover into an operationally sensible router.

Business goal:
- classify failures consistently
- persist upstream state across requests
- honor cooldown and circuit-breaker behavior before routing decisions are made

In scope:
- failure taxonomy
- cooldown after `429`
- circuit breaker after repeated failures
- in-memory and Redis-backed health repositories

Out of scope:
- metrics and traces
- production AKS proof

---

## Security Contract

- visibility: `internal`
- health state: repository-owned platform state, not client-controlled input
- `Retry-After`: must be parsed defensively and never trusted blindly beyond bounded cooldown rules
- observability hooks: prepare data for later metrics/logging without leaking secrets

---

## Sub-Tasks

### TASK-014-01: Failure taxonomy and retriable classification

**Status:** To Do

Define the failure model that drives retries and state updates.

### TASK-014-02: Health state repository and state-transition rules

**Status:** To Do

Implement how health data is stored and updated across attempts and requests.

### TASK-014-03: Circuit breaker thresholds and router integration

**Status:** To Do

Apply the new health state to routing decisions and failover behavior.

### TASK-014-04: Operations docs, observability hooks, and validation alignment

**Status:** To Do

Document the health model and prove the behavior through tests and tracking.

---

## Implementation Order

1. Finalize the failure classification model.
2. Implement the health repository and state updates.
3. Integrate cooldown and circuit breaker behavior into routing.
4. Add validation coverage and update docs.

---

## Testing Requirements

- unit tests for failure classification and state transitions
- local integration tests for cooldown and circuit-open behavior
- adapter tests for Redis-backed persistence semantics
- `pre-commit --all-files`

---

## Documentation Updates Required

- `docs/routing/failover-and-health.md`
- `docs/operations/observability-and-health.md`
- `docs/reference/decision-reasons.md`
- `_docs/_TASKS/TASK-014-phase-5-failure-classification-health-state-cooldown-and-circuit-breaker.md`
- `_docs/_TASKS/TASK-014-01-failure-taxonomy-and-retriable-classification.md`
- `_docs/_TASKS/TASK-014-01-01-http-network-and-quota-signatures-and-mapping-rules.md`
- `_docs/_TASKS/TASK-014-01-02-retry-after-parsing-and-cooldown-semantics.md`
- `_docs/_TASKS/TASK-014-02-health-state-repository-and-state-transition-rules.md`
- `_docs/_TASKS/TASK-014-02-01-in-memory-bootstrap-repository-and-transition-tests.md`
- `_docs/_TASKS/TASK-014-02-02-redis-backed-repository-adapter-and-persistence-behavior.md`
- `_docs/_TASKS/TASK-014-03-circuit-breaker-thresholds-and-router-integration.md`
- `_docs/_TASKS/TASK-014-04-operations-docs-observability-hooks-and-validation-alignment.md`

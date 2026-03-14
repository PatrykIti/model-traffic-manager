[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-013: Phase 4 Multi-Upstream Routing and Tiered Failover
# FileName: TASK-013-phase-4-multi-upstream-routing-and-tiered-failover.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Large
**Dependencies:** TASK-011, TASK-012
**Status:** **To Do**

---

## Overview

Replace the deterministic first-upstream bootstrap logic with the planned tier-aware routing model.

Business goal:
- route across multiple upstreams predictably and explainably
- honor tier ordering before weight-based balancing
- keep failover decisions deterministic enough to test and debug

In scope:
- routing decision model
- availability filtering and tier grouping
- weighted round robin inside a tier
- request-attempt orchestration for retriable failures

Out of scope:
- Redis-backed health persistence
- cooldown and circuit breaker state transitions
- metrics and traces

---

## Security Contract

- visibility: `internal`
- explainable routing: mandatory for every selection and failover decision
- failover policy: retry only for explicitly retriable failures
- non-retriable failures: must not silently fail over
- outbound auth: reuse previously implemented auth modes without changing client-auth assumptions

---

## Sub-Tasks

### TASK-013-01: Routing decision model and deterministic selection policy

**Status:** To Do

Implement the domain and application shape of tier-aware selection.

### TASK-013-02: Request-attempt orchestration and failover for chat and embeddings

**Status:** To Do

Teach the use cases to retry across eligible candidates without hiding non-retriable failures.

### TASK-013-03: API and local integration coverage with documentation alignment

**Status:** To Do

Prove the new routing path locally and update the official explanation of the strategy.

---

## Implementation Order

1. Finalize the route decision model and selection behavior.
2. Add attempt orchestration to the proxy use cases.
3. Expose the richer behavior through the existing API surfaces.
4. Prove the flow locally and update docs.

---

## Testing Requirements

- unit tests for weighted round robin and tier selection
- unit tests for failover attempt orchestration
- local integration tests for same-tier balancing and cross-tier fallback
- `pre-commit --all-files`

---

## Documentation Updates Required

- `docs/routing/routing-strategy.md`
- `docs/routing/failover-and-health.md`
- `docs/architecture/request-lifecycle.md`
- `_docs/_TASKS/TASK-013-phase-4-multi-upstream-routing-and-tiered-failover.md`
- `_docs/_TASKS/TASK-013-01-routing-decision-model-and-deterministic-selection-policy.md`
- `_docs/_TASKS/TASK-013-01-01-availability-filtering-by-state-and-tier-grouping.md`
- `_docs/_TASKS/TASK-013-01-02-weighted-round-robin-implementation-and-deterministic-tests.md`
- `_docs/_TASKS/TASK-013-02-request-attempt-orchestration-and-failover-for-chat-and-embeddings.md`
- `_docs/_TASKS/TASK-013-02-01-retriable-vs-non-retriable-failure-flow.md`
- `_docs/_TASKS/TASK-013-02-02-decision-reasons-and-next-candidate-transitions.md`
- `_docs/_TASKS/TASK-013-03-api-and-local-integration-coverage-with-documentation-alignment.md`

[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-021](./TASK-021-mvp-closure-runtime-state-activation-and-contract-hardening.md)

# TASK-021-04: Explainable Routing Rejection Diagnostics and Status Reconciliation
# FileName: TASK-021-04-explainable-routing-rejection-diagnostics-and-status-reconciliation.md

**Priority:** High
**Category:** Observability and Documentation Alignment
**Estimated Effort:** Medium
**Dependencies:** TASK-021, TASK-016
**Status:** **Done** (2026-03-15)

---

## Overview

The router already emits selection and completion events, but the MVP requires operators to reconstruct why a candidate was rejected and why the winning candidate was chosen.

Detailed work:
1. Expand routing events with failover reason and rejected-candidate metadata.
2. Keep decision reasons compact while making the rejection chain reconstructable.
3. Update metrics and trace payloads only where the extra fields are operationally useful.
4. Reconcile official status docs with the now-complete MVP implementation.

---

## Security Contract

- rejected-candidate diagnostics must not include tokens, secret values, or request payload bodies
- logs and metrics should only expose routing metadata already present in deployment definitions and health state

---

## Testing Requirements

- selector tests for rejected-candidate metadata
- use-case tests for failover reason propagation across retries
- recorder tests for structured event payload shape
- local integration tests that prove the request flow still succeeds while emitting richer metadata

---

## Documentation Updates Required

- `docs/reference/decision-reasons.md`
- `docs/routing/failover-and-health.md`
- `docs/getting-started/implementation-status.md`
- `_docs/_TASKS/TASK-021-04-explainable-routing-rejection-diagnostics-and-status-reconciliation.md`

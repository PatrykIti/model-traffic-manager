[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-016: Explainable Routing, Observability, and Release Hardening
# FileName: TASK-016-explainable-routing-observability-and-release-hardening.md

**Priority:** High
**Category:** Observability and Hardening
**Estimated Effort:** Large
**Dependencies:** TASK-008, TASK-014, TASK-015
**Status:** **In Progress** (2026-03-14)

---

## Overview

Turn the feature-complete MVP into an observable and better-validated release candidate.

Business goal:
- expose route decisions, health state, and limiter behavior clearly
- add the metrics and traces needed to understand production behavior
- activate the higher-level Azure-backed validation model already planned in the repository
- finish with the hardening work needed before a broader release

---

## Security Contract

- logs and traces must never include raw secrets, API keys, or bearer tokens
- request-body visibility must remain bounded and intentionally scrubbed
- operator diagnostics must help reconstruct routing decisions without leaking sensitive payload content
- release validation must keep destructive test infrastructure temporary

---

## Sub-Tasks

### TASK-016-01: Decision reason logging, request correlation, and operator diagnostics

**Status:** Done (2026-03-14)

Make route-selection and failover decisions reconstructable for operators.

### TASK-016-02: Metrics, traces, and readiness/health observability expansion

**Status:** Done (2026-03-14)

Expose the runtime signals needed for monitoring and troubleshooting.

### TASK-016-03: `integration-azure` and `e2e-aks` activation

**Status:** To Do

Turn the previously planned higher-level validation model into real executable coverage.

### TASK-016-04: Performance, timeout policy, pool tuning, and release checks

**Status:** To Do

Finish the hardening work needed before treating the router as a stronger release candidate.

---

## Implementation Order

1. Implement decision logging and correlation metadata.
2. Add metrics and traces on top of the decision model.
3. Activate Azure-backed validation using the existing infra planning baseline.
4. Run performance and stability hardening before release tagging.

---

## Testing Requirements

- route decision logs and metric events are covered by tests
- `integration-azure` and `e2e-aks` remain explicitly triggered and bounded
- timeout, pooling, and failure-path tuning are validated under representative load
- `pre-commit --all-files`

---

## Documentation Updates Required

- `docs/operations/observability-and-health.md`
- `docs/reference/decision-reasons.md`
- `docs/operations/testing-levels-and-environments.md`
- `_docs/_TASKS/TASK-016-explainable-routing-observability-and-release-hardening.md`
- `_docs/_TASKS/TASK-016-01-decision-reason-logging-request-correlation-and-operator-diagnostics.md`
- `_docs/_TASKS/TASK-016-01-01-structured-event-schema-for-selection-failover-limiter-and-breaker-updates.md`
- `_docs/_TASKS/TASK-016-01-02-reference-documentation-and-troubleshooting-views.md`
- `_docs/_TASKS/TASK-016-02-metrics-traces-and-readiness-health-observability-expansion.md`
- `_docs/_TASKS/TASK-016-03-integration-azure-and-e2e-aks-activation.md`
- `_docs/_TASKS/TASK-016-04-performance-timeout-policy-pool-tuning-and-release-checks.md`

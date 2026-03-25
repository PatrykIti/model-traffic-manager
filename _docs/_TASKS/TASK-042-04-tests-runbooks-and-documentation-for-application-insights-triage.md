[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-042](./TASK-042-azure-monitor-application-insights-request-flow-telemetry-and-pod-diagnostics.md)

# TASK-042-04: Tests, Runbooks, and Documentation for Application Insights Triage
# FileName: TASK-042-04-tests-runbooks-and-documentation-for-application-insights-triage.md

**Priority:** High
**Category:** Documentation and Validation
**Estimated Effort:** Medium
**Dependencies:** TASK-042-01, TASK-042-02, TASK-042-03, TASK-040-08
**Status:** **Done** (2026-03-25)

---

## Overview

Close the Azure Monitor observability package with validation and operator guidance that turns the emitted telemetry into a repeatable incident workflow.

Detailed work:
1. Add unit and integration coverage for exporter configuration, trace enrichment, startup snapshots, and safe fallback behavior.
2. Document how operators should pivot by `request_id`, `deployment_id`, `upstream_id`, `account`, `region`, and failure classification in Application Insights.
3. Add an operator runbook for diagnosing degraded PTU and PAYG behavior through Application Insights plus pod startup logs.
4. Reconcile the public documentation and implementation-status pages with the final runtime behavior.

---

## Testing Requirements

- `make check`
- local integration coverage proves the request-flow telemetry contract without requiring live Azure Monitor resources
- docs and runbooks must match the actual emitted identifiers and field names

---

## Documentation Updates Required

- `docs/architecture/request-lifecycle.md`
- `docs/operations/observability-and-health.md`
- `docs/getting-started/implementation-status.md`
- `docs/operations/runbooks/README.md`
- `docs/operations/runbooks/application-insights-request-flow-triage.md`
- `_docs/_TASKS/TASK-042-04-tests-runbooks-and-documentation-for-application-insights-triage.md`

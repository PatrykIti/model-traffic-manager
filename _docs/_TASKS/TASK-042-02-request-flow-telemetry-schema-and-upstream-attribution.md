[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-042](./TASK-042-azure-monitor-application-insights-request-flow-telemetry-and-pod-diagnostics.md)

# TASK-042-02: Request-Flow Telemetry Schema and Upstream Attribution
# FileName: TASK-042-02-request-flow-telemetry-schema-and-upstream-attribution.md

**Priority:** High
**Category:** Observability Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-042, TASK-016, TASK-021
**Status:** **Done** (2026-03-25)

---

## Overview

Make every routed request reconstructable in Application Insights from inbound span creation through outbound attempt selection, failover, and final completion.

Detailed work:
1. Enrich inbound and outbound spans with stable routing attributes such as `request_id`, `endpoint_kind`, `deployment_id`, `upstream_id`, `provider`, `account`, `region`, `tier`, `selected_tier`, `decision_reason`, `failover_reason`, `outcome`, and `failure_reason`.
2. Attach the current runtime-event model to spans in a way that keeps route-selection history visible inside one correlated request flow.
3. Ensure the terminal request result records the final upstream that actually served the request or the final failure path that ended it.
4. Define one safe operator-facing field for capacity classification when account, region, and deployment metadata are not enough to distinguish PTU-backed capacity from PAYG-backed capacity.
5. Keep cardinality bounded and explainable so Application Insights remains usable under real traffic volume.

Preferred outcome:
- an operator can start with a request ID, deployment ID, or upstream ID and quickly answer what happened
- a degraded PTU or PAYG upstream can be isolated from the trace timeline without reading pod-local raw logs first

---

## Security Contract

- do not attach prompt text, completion text, embeddings vectors, auth headers, or raw downstream error bodies to spans
- limit upstream metadata to routing and supportability fields that are safe for operator inspection
- any added capacity-classification field must stay semantic and must not leak tenant or secret context

---

## Testing Requirements

- unit and integration tests prove final-upstream attribution on success and on failover
- failure paths preserve correlation while staying scrubbed of secrets and bodies
- bounded-cardinality rules are covered for any new attributes added to spans or events

---

## Documentation Updates Required

- `docs/architecture/request-lifecycle.md`
- `docs/operations/observability-and-health.md`
- `docs/reference/decision-reasons.md`
- `docs/configuration/deployment-and-upstreams.md`
- `_docs/_TASKS/TASK-042-02-request-flow-telemetry-schema-and-upstream-attribution.md`

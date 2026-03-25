[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-042: Azure Monitor Application Insights Request-Flow Telemetry and Pod Diagnostics
# FileName: TASK-042-azure-monitor-application-insights-request-flow-telemetry-and-pod-diagnostics.md

**Priority:** High
**Category:** Production Observability
**Estimated Effort:** Large
**Dependencies:** TASK-016, TASK-021, TASK-040-08
**Status:** **Done** (2026-03-25)

---

## Overview

Add first-class Azure Monitor / Application Insights observability for the router request flow without weakening the repository's explainability or secret-handling rules.

Business goals:
- make every inbound router request reconstructable in Application Insights from request start to final upstream outcome
- let operators answer which upstream served a given `chat/completions` or `embeddings` request and why the router selected or failed over to it
- improve incident triage when PAYG capacity, PTU-backed capacity, regional availability, cooldown, or circuit state causes degraded behavior
- emit one safe startup-time topology snapshot on each pod so operators can quickly confirm the active routing shape and observability mode

Recommended approach:
- keep the router's explicit, owned instrumentation as the source of truth instead of replacing it with opaque auto-instrumentation
- use traces as the canonical request-flow record in Application Insights
- keep stdout structured logs and Prometheus `/metrics` as the baseline local and cluster-native observability surfaces
- treat Azure-backed log export as opt-in and tightly scoped if Python exporter maturity or noise profile remains a concern

Non-goals:
- do not log prompts, completions, embeddings payloads, or raw HTTP bodies
- do not turn the router into a generic debug gateway or packet recorder
- do not hide routing ambiguity behind account-name conventions when explicit upstream metadata is needed

---

## Security Contract

- telemetry must never include raw secrets, API keys, bearer tokens, or secret references
- telemetry must not include request or response bodies beyond minimal safe metadata already allowed by the router contract
- startup snapshots must expose only operator-safe topology fields such as deployment IDs, upstream IDs, provider, account, region, tier, balancing policy, and enabled observability modes
- Azure Monitor / Application Insights export must remain explicitly configured and disabled by default for the zero-dependency local path

---

## Sub-Tasks

### TASK-042-01: Azure Monitor OpenTelemetry export and runtime config surface

**Status:** Done (2026-03-25)

Add repo-owned Azure Monitor exporter wiring, feature flags, and startup lifecycle behavior without breaking the current local-only runtime.

### TASK-042-02: Request-flow telemetry schema and upstream attribution

**Status:** Done (2026-03-25)

Extend the trace and runtime-event model so operators can reconstruct upstream selection, failover, and final outcomes inside Application Insights.

### TASK-042-03: Pod-local startup topology snapshot and operator inspection surface

**Status:** Done (2026-03-25)

Emit one startup-time router topology summary per pod and define the minimum operator workflow for inspecting it through pod logs.

### TASK-042-04: Tests, runbooks, and documentation for Application Insights triage

**Status:** Done (2026-03-25)

Close the package with proof, operator guidance, and incident-response documentation for Azure Monitor backed request-flow debugging.

---

## Implementation Order

1. Add the Azure Monitor exporter and configuration contract behind an explicit runtime switch.
2. Enrich the request-flow trace schema with deterministic upstream attribution and failover metadata.
3. Emit the startup topology snapshot and define the pod-local inspection contract.
4. Finish with tests, official docs, and runbooks for production incident triage.

---

## Testing Requirements

- local startup must still work with no Azure Monitor configuration present
- trace and runtime-event coverage must prove request correlation plus final upstream attribution
- startup topology output must be deterministic, scrubbed, and emitted once per process start
- any Azure-backed verification must stay opt-in and preserve safe artifact capture rules

---

## Documentation Updates Required

- `docs/architecture/request-lifecycle.md`
- `docs/operations/observability-and-health.md`
- `docs/reference/decision-reasons.md`
- `docs/getting-started/implementation-status.md`
- `docs/operations/runbooks/README.md`
- `docs/operations/runbooks/application-insights-request-flow-triage.md`
- `_docs/_TASKS/TASK-042-azure-monitor-application-insights-request-flow-telemetry-and-pod-diagnostics.md`
- `_docs/_TASKS/TASK-042-01-azure-monitor-opentelemetry-export-and-runtime-config-surface.md`
- `_docs/_TASKS/TASK-042-02-request-flow-telemetry-schema-and-upstream-attribution.md`
- `_docs/_TASKS/TASK-042-03-pod-local-startup-topology-snapshot-and-operator-inspection-surface.md`
- `_docs/_TASKS/TASK-042-04-tests-runbooks-and-documentation-for-application-insights-triage.md`
- `_docs/_TASKS/README.md`

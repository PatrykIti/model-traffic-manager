[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-042](./TASK-042-azure-monitor-application-insights-request-flow-telemetry-and-pod-diagnostics.md)

# TASK-042-03: Pod-Local Startup Topology Snapshot and Operator Inspection Surface
# FileName: TASK-042-03-pod-local-startup-topology-snapshot-and-operator-inspection-surface.md

**Priority:** High
**Category:** Runtime Diagnostics
**Estimated Effort:** Medium
**Dependencies:** TASK-042, TASK-042-01, TASK-042-02
**Status:** **Done** (2026-03-25)

---

## Overview

Emit one startup-time topology snapshot per pod so operators can confirm what routing shape and observability mode actually became active after boot.

Detailed work:
1. Record a structured startup event that summarizes active deployments, upstream IDs, provider, account, region, tier, balancing policy, warm-standby or drain state, runtime-state backend, and Azure Monitor enablement.
2. Make the startup output readable in `kubectl logs` while keeping it structured enough for centralized telemetry systems.
3. Define the minimum supported pod-local inspection flow for operators, starting with startup logs before introducing any new debug endpoint.
4. Ensure the snapshot makes it obvious whether Application Insights export is enabled and which request-flow identifiers operators should pivot on first.

Non-goal:
- do not add a permanently noisy per-request console dump on the pod
- do not expose a public debugging API without a strong operational reason

---

## Risks

- startup logs become too verbose if the topology snapshot is not bounded and summarized carefully
- operators may mistake startup topology for live health state unless the event is explicitly labeled as a boot snapshot

---

## Testing Requirements

- startup snapshot is emitted exactly once per application boot
- snapshot payload stays deterministic for a fixed config file
- snapshot omits secrets, tokens, and unsafe endpoint details

---

## Documentation Updates Required

- `docs/operations/observability-and-health.md`
- `docs/operations/runbooks/application-insights-request-flow-triage.md`
- `_docs/_TASKS/TASK-042-03-pod-local-startup-topology-snapshot-and-operator-inspection-surface.md`

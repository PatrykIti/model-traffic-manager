[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-044](./TASK-044-e2e-aks-live-observability-profile-for-azure-monitor-and-consumer-role.md)

# TASK-044-03: Live Suite Assertions for Request Flow, Final Upstream Attribution, and Consumer Role
# FileName: TASK-044-03-live-suite-assertions-for-request-flow-final-upstream-attribution-and-consumer-role.md

**Priority:** High
**Category:** Live Validation
**Estimated Effort:** Medium
**Dependencies:** TASK-044-01, TASK-044-02
**Status:** **Done** (2026-03-25)

---

## Overview

Add `tests/e2e_aks_live_observability/` to prove that real router traffic sent through AKS appears in Azure Monitor / Application Insights with the expected routing metadata.

Minimum assertions:

1. a real chat request through AKS succeeds
2. the emitted telemetry can be found by bounded polling
3. the query result includes `router.final_upstream_id`
4. the query result includes `router.consumer_role`
5. the query result can be correlated by request ID

Recommended query strategy:

- choose one canonical query surface for the suite
- prefer either:
  - Application Insights query by component/app ID, or
  - Log Analytics query by workspace ID
- keep retries explicit because ingestion is eventually consistent

---

## Risks

- live telemetry queries will be slower and more eventually consistent than current `/metrics`-based suites
- the suite will be flaky if it relies on unbounded sleeps instead of structured polling

---

## Testing Requirements

- suite must fail clearly when telemetry is missing versus when the routed request itself fails
- test diagnostics should persist the executed query and the response snippet in the artifact bundle

---

## Documentation Updates Required

- `docs/operations/testing-levels-and-environments.md`
- `docs/operations/runbooks/application-insights-request-flow-triage.md`
- `_docs/_TASKS/TASK-044-03-live-suite-assertions-for-request-flow-final-upstream-attribution-and-consumer-role.md`

[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-044: E2E AKS Live Observability Profile for Azure Monitor and Consumer Role
# FileName: TASK-044-e2e-aks-live-observability-profile-for-azure-monitor-and-consumer-role.md

**Priority:** High
**Category:** Validation and Observability
**Estimated Effort:** Large
**Dependencies:** TASK-042, TASK-043, TASK-029-07
**Status:** To Do

---

## Overview

Add one dedicated `e2e-aks-live-observability` profile that proves the two latest observability features on real Azure and AKS infrastructure:

- Azure Monitor / Application Insights request-flow export
- `consumer_role` propagation through request telemetry

Recommended profile boundary:

- build one combined profile, not two separate profiles
- use the same profile to prove both Application Insights request-flow visibility and `consumer_role` grouping
- keep `consumer_role` validation inside the observability suite because it is telemetry metadata, not a separate infrastructure capability

Business goals:

- prove that the router emits real request-flow telemetry into Azure Monitor / Application Insights from AKS
- prove that operators can identify final upstream attribution and `consumer_role` on real routed requests
- keep the observability proof aligned with the repository's AKS-based live validation model

Required Azure modules:

- `azurerm_kubernetes_cluster` `AKSv2.1.0`
- `azurerm_user_assigned_identity` `UAIv1.0.0`
- `azurerm_cognitive_account` `COGv1.0.0`
- `azurerm_log_analytics_workspace` `LAWv1.1.0`
- `azurerm_application_insights` `APPINSv1.1.0`
- `azurerm_role_assignment` `RAv1.0.0`

Optional module:

- `azurerm_application_insights_workbook` `AIWBv1.0.0`
  only if the suite should also leave behind an operator-facing workbook seed

Non-goals:

- do not create a second dedicated AKS live profile only for `consumer_role`
- do not add workspace- or telemetry-heavy infra to the default smoke AKS suite

---

## Security Contract

- Application Insights connection data must not be committed into YAML, manifests, or artifacts as plain repository content
- the suite must keep request payload visibility bounded to the current router telemetry contract
- artifact capture and query results must not leak secrets, tokens, or raw connection strings
- the observability suite must remain opt-in and must not silently widen default CI cost

---

## Sub-Tasks

### TASK-044-01: Azure observability scope for AKS, Log Analytics, and Application Insights

**Status:** To Do

Create a dedicated Terraform scope for the live observability suite using the repository's existing AKS and Azure module patterns plus the user's Log Analytics and Application Insights modules.

### TASK-044-02: Router runtime wiring and manifest delivery for Azure Monitor mode

**Status:** To Do

Render and deliver router config plus pod environment settings so the AKS deployment runs with `observability_backend=azure_monitor` and a real Application Insights connection string.

### TASK-044-03: Live suite assertions for request flow, final upstream attribution, and consumer role

**Status:** To Do

Add live AKS tests that send real requests through the router, poll Azure Monitor telemetry, and assert final-upstream plus `consumer_role` visibility.

### TASK-044-04: Runner, workflow, runbook, and documentation rollout for the observability suite

**Status:** To Do

Register the new suite in the shared runner/workflow model and document how operators should run and interpret it.

---

## Implementation Order

1. Create the dedicated observability infra scope with Log Analytics and Application Insights.
2. Wire Azure Monitor mode into the rendered router deployment and pod runtime env.
3. Add live tests that query Azure Monitor with bounded retries.
4. Roll the suite into the runner registry, docs, and runbooks.

---

## Testing Requirements

- local quality gate remains green
- the live suite proves at least one real request that appears in Azure Monitor / Application Insights
- the suite verifies `router.final_upstream_id` and `router.consumer_role`
- the suite keeps bounded polling and retry semantics because telemetry ingestion is eventually consistent

---

## Documentation Updates Required

- `docs/operations/testing-levels-and-environments.md`
- `docs/operations/observability-and-health.md`
- `docs/getting-started/local-development.md`
- `docs/operations/runbooks/application-insights-request-flow-triage.md`
- `_docs/_TASKS/TASK-044-e2e-aks-live-observability-profile-for-azure-monitor-and-consumer-role.md`
- `_docs/_TASKS/TASK-044-01-azure-observability-scope-for-aks-log-analytics-and-application-insights.md`
- `_docs/_TASKS/TASK-044-02-router-runtime-wiring-and-manifest-delivery-for-azure-monitor-mode.md`
- `_docs/_TASKS/TASK-044-03-live-suite-assertions-for-request-flow-final-upstream-attribution-and-consumer-role.md`
- `_docs/_TASKS/TASK-044-04-runner-workflow-runbook-and-documentation-rollout-for-the-observability-suite.md`
- `_docs/_TASKS/README.md`

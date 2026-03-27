[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-044](./TASK-044-e2e-aks-live-observability-profile-for-azure-monitor-and-consumer-role.md)

# TASK-044-01: Azure Observability Scope for AKS, Log Analytics, and Application Insights
# FileName: TASK-044-01-azure-observability-scope-for-aks-log-analytics-and-application-insights.md

**Priority:** High
**Category:** Validation Infrastructure
**Estimated Effort:** Medium
**Dependencies:** TASK-044
**Status:** **Done** (2026-03-25)

---

## Overview

Create `infra/e2e-aks-live-observability/` as a dedicated scope for the live observability suite.

Required module usage:

1. `azurerm_kubernetes_cluster` `AKSv2.1.0`
2. `azurerm_user_assigned_identity` `UAIv1.0.0`
3. `azurerm_cognitive_account` `COGv1.0.0`
4. `azurerm_log_analytics_workspace` `LAWv1.1.0`
5. `azurerm_application_insights` `APPINSv1.1.0`
6. `azurerm_role_assignment` `RAv1.0.0`

Scope goals:

- provision AKS and one real Azure OpenAI path for routed requests
- provision one Log Analytics workspace and one Application Insights resource for router telemetry
- expose the minimal outputs needed by the render script and live tests

Preferred outputs:

- AKS cluster name
- user-assigned identity IDs
- Azure OpenAI endpoint
- Application Insights connection string or secure delivery reference
- Application Insights app ID and/or Log Analytics workspace ID for test queries

---

## Risks

- telemetry validation becomes flaky if the scope does not expose one stable query surface
- infra cost grows unnecessarily if the observability suite provisions more than one live model path

---

## Testing Requirements

- `terraform validate` on the new scope
- scope outputs are sufficient for router config rendering and Azure Monitor query tests

---

## Documentation Updates Required

- `docs/operations/testing-levels-and-environments.md`
- `_docs/_TASKS/TASK-044-01-azure-observability-scope-for-aks-log-analytics-and-application-insights.md`

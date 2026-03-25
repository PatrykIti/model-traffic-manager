[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-044](./TASK-044-e2e-aks-live-observability-profile-for-azure-monitor-and-consumer-role.md)

# TASK-044-02: Router Runtime Wiring and Manifest Delivery for Azure Monitor Mode
# FileName: TASK-044-02-router-runtime-wiring-and-manifest-delivery-for-azure-monitor-mode.md

**Priority:** High
**Category:** Runtime Delivery
**Estimated Effort:** Medium
**Dependencies:** TASK-044, TASK-044-01
**Status:** To Do

---

## Overview

Wire the AKS live observability deployment so the router boots in Azure Monitor mode and uses one rendered config that includes `consumer_role`.

Detailed work:

1. Add a render script for the observability suite, based on the existing live-model render pattern.
2. Render deployment configs that include explicit `consumer_role` values.
3. Inject the Azure Monitor connection string and required env vars into the router pod without hard-coding them into repository YAML.
4. Extend the AKS manifest template and suite runner integration for the new env contract.

Required env surface:

- `MODEL_TRAFFIC_MANAGER_OBSERVABILITY_BACKEND=azure_monitor`
- `MODEL_TRAFFIC_MANAGER_AZURE_MONITOR_CONNECTION_STRING` or `APPLICATIONINSIGHTS_CONNECTION_STRING`
- optional sampling/log-export toggles if the suite needs them

---

## Security Contract

- do not store the connection string in committed example router configs
- prefer a delivery path that keeps generated secrets in temporary runner artifacts or Kubernetes secrets only

---

## Testing Requirements

- local render validation for the new script
- manifest wiring and env propagation covered by existing shell/workflow validation paths

---

## Documentation Updates Required

- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-044-02-router-runtime-wiring-and-manifest-delivery-for-azure-monitor-mode.md`

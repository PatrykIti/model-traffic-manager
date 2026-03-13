[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-006: AKS Configuration Delivery Documentation
# FileName: TASK-006-aks-configuration-delivery-documentation.md

**Priority:** High
**Category:** Official Documentation
**Estimated Effort:** Small
**Dependencies:** TASK-005
**Status:** **Done** (2026-03-13)

---

## Overview

Document the supported and recommended approaches for delivering router configuration to AKS workloads.

Business goal:
- explain how the YAML configuration can reach the application in AKS
- clarify which approach already works with the current code
- explain the trade-offs between Kubernetes Secret, env vars, and ConfigMap/Secret split

---

## Sub-Tasks

### TASK-006-01: Official AKS config delivery approaches page

**Status:** Done

Add a dedicated official documentation page that compares the three AKS delivery models and recommends the best one for the current implementation.

---

## Testing Requirements

- official docs page is linked from `docs/operations/README.md`
- guidance is consistent with the current runtime behavior based on `MODEL_TRAFFIC_MANAGER_CONFIG_PATH`
- navigation links and local Markdown links remain valid

---

## Documentation Updates Required

- `docs/operations/README.md`
- `docs/operations/deployment-model.md`
- `docs/configuration/configuration-model.md`
- `docs/operations/aks-configuration-delivery.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
- `_docs/_CHANGELOG/6-2026-03-13-aks-configuration-delivery-approaches.md`

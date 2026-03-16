[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029](./TASK-029-live-azure-validation-expansion-for-router-surfaces.md)

# TASK-029-05: Live Shared-Services Validation on Azure and AKS
# FileName: TASK-029-05-live-shared-services-validation-on-azure-and-aks.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029, TASK-029-01
**Status:** **To Do**

---

## Overview

Add live validation for the shared-service execution model.

Candidate checks:
- `router_proxy + single_endpoint`
- `router_proxy + tiered_failover`
- `direct_backend_access` remains metadata-only and fails closed when executed through router
- live downstream target for shared services is provisioned and observable

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-029-05-live-shared-services-validation-on-azure-and-aks.md`

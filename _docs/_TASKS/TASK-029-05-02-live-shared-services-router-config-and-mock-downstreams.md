[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029-05](./TASK-029-05-live-shared-services-validation-on-azure-and-aks.md)

# TASK-029-05-02: Live Shared-Services Router Config and Mock Downstreams
# FileName: TASK-029-05-02-live-shared-services-router-config-and-mock-downstreams.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029-05-01
**Status:** **Done** (2026-03-18)

---

## Overview

Render a dedicated router config for live shared-services validation and deploy in-cluster mock downstreams for single-endpoint and tiered-failover execution paths.

## Documentation Updates Required

- `scripts/release/render_live_shared_services_router_config.py`
- `infra/e2e-aks-live-shared-services/k8s/`

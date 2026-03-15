[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-025](./TASK-025-shared-service-example-yaml-catalog.md)

# TASK-025-01: Official Shared-Service Example Router Configs
# FileName: TASK-025-01-official-shared-service-example-router-configs.md

**Priority:** High
**Category:** Documentation Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-025
**Status:** **Done** (2026-03-15)

---

## Overview

Publish three example router configs that show the full range of currently supported shared-service execution modes:

1. storage/audio-style `direct_backend_access`
2. internal HTTP API as `router_proxy` with `single_endpoint`
3. shared search/transcript service as `router_proxy` with `tiered_failover`

The examples should be full router configs, not only partial snippets, so they can be copied and adapted directly.

---

## Documentation Updates Required

- `docs/configuration/shared-services.md`
- `configs/examples/shared-services-direct-backend-access.router.yaml`
- `configs/examples/shared-services-router-proxy-single-endpoint.router.yaml`
- `configs/examples/shared-services-router-proxy-tiered-failover.router.yaml`
- `_docs/_TASKS/TASK-025-01-official-shared-service-example-router-configs.md`

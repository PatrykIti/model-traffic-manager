[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-024](./TASK-024-shared-services-execution-model-and-backend-facing-proxy-surface.md)

# TASK-024-02: Backend-Facing Shared-Service Execution Use Case and API Route
# FileName: TASK-024-02-backend-facing-shared-service-execution-use-case-and-api-route.md

**Priority:** High
**Category:** Application and API Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-024, TASK-024-01
**Status:** **Done** (2026-03-15)

---

## Overview

Implement the first shared-service execution surface through the router.

Initial scope:
- backend-facing only
- HTTP/JSON only
- `POST /v1/shared-services/{service_id}`
- registry-only services reject execution
- provider-managed and single-endpoint services execute one downstream call
- tiered-failover services reuse the router failover path

---

## Security Contract

- only JSON execution is supported in the first version
- registry-only services must reject execution explicitly
- execution-mode policy must be visible in runtime events

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-024-02-backend-facing-shared-service-execution-use-case-and-api-route.md`

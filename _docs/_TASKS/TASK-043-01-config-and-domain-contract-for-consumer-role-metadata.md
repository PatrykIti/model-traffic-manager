[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-043](./TASK-043-consumer-role-metadata-for-routed-traffic.md)

# TASK-043-01: Config and Domain Contract for Consumer Role Metadata
# FileName: TASK-043-01-config-and-domain-contract-for-consumer-role-metadata.md

**Priority:** High
**Category:** Configuration Contract
**Estimated Effort:** Medium
**Dependencies:** TASK-043
**Status:** **Done** (2026-03-25)

---

## Overview

Add the optional `consumer_role` field to deployment and shared-service configuration so one router profile can identify the consuming backend it represents.

Detailed work:
1. Extend deployment and shared-service config models with `consumer_role`.
2. Carry the field into domain entities and summary DTOs.
3. Expose the field in operator-facing registry endpoints where appropriate.

---

## Testing Requirements

- unit coverage for config validation and domain construction
- integration coverage for `GET /deployments` and `GET /shared-services`

---

## Documentation Updates Required

- `docs/configuration/deployment-and-upstreams.md`
- `configs/example.router.yaml`
- `configs/full-capabilities.router.yaml`
- `_docs/_TASKS/TASK-043-01-config-and-domain-contract-for-consumer-role-metadata.md`

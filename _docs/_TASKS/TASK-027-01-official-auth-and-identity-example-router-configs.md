[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-027](./TASK-027-auth-and-identity-example-yaml-catalog.md)

# TASK-027-01: Official Auth and Identity Example Router Configs
# FileName: TASK-027-01-official-auth-and-identity-example-router-configs.md

**Priority:** High
**Category:** Documentation Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-027
**Status:** **Done** (2026-03-15)

---

## Overview

Publish example router configs that show:

1. the default process identity with `managed_identity` and no explicit `client_id`
2. explicit user-assigned identity selection with `client_id`
3. mixed auth modes across deployments and shared services

---

## Documentation Updates Required

- `configs/examples/auth-identity-default-managed-identity.router.yaml`
- `configs/examples/auth-identity-explicit-client-ids.router.yaml`
- `configs/examples/auth-identity-mixed-modes.router.yaml`
- `_docs/_TASKS/TASK-027-01-official-auth-and-identity-example-router-configs.md`

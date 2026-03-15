[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-027: Auth and Identity Example YAML Catalog
# FileName: TASK-027-auth-and-identity-example-yaml-catalog.md

**Priority:** High
**Category:** Documentation and Runtime Examples
**Estimated Effort:** Small
**Dependencies:** TASK-012, TASK-024
**Status:** **Done** (2026-03-15)

---

## Overview

Add real example router YAML files and official docs that explain the supported auth and identity patterns clearly.

Business goal:
- show how the router behaves with the default process identity
- show how explicit `client_id` selection works for user-assigned identities
- show how `managed_identity`, `api_key`, and `none` can coexist in one router config

---

## Sub-Tasks

### TASK-027-01: Official auth and identity example router configs

**Status:** Done (2026-03-15)

Add versioned example router YAML files for default managed identity, explicit `client_id`, and mixed auth modes.

### TASK-027-02: Official auth and identity documentation page

**Status:** Done (2026-03-15)

Add a dedicated official docs page that explains the supported identity and auth options and links to the example files.

---

## Testing Requirements

- YAML examples stay valid against the current config contract
- official docs link to the real example files

---

## Documentation Updates Required

- `docs/configuration/README.md`
- `docs/configuration/auth-and-identity.md`
- `docs/configuration/deployment-and-upstreams.md`
- `configs/examples/auth-identity-default-managed-identity.router.yaml`
- `configs/examples/auth-identity-explicit-client-ids.router.yaml`
- `configs/examples/auth-identity-mixed-modes.router.yaml`
- `_docs/_TASKS/TASK-027-auth-and-identity-example-yaml-catalog.md`
- `_docs/_TASKS/TASK-027-01-official-auth-and-identity-example-router-configs.md`
- `_docs/_TASKS/TASK-027-02-official-auth-and-identity-documentation-page.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`

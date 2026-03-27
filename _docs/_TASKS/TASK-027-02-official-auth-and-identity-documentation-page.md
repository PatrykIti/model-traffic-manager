[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-027](./TASK-027-auth-and-identity-example-yaml-catalog.md)

# TASK-027-02: Official Auth and Identity Documentation Page
# FileName: TASK-027-02-official-auth-and-identity-documentation-page.md

**Priority:** High
**Category:** Documentation Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-027
**Status:** **Done** (2026-03-15)

---

## Overview

Add a dedicated official docs page that explains how the router selects identities and how operators should choose between the supported auth modes.

Required topics:
- default process identity
- explicit `client_id`
- `managed_identity`
- `api_key`
- `none`
- mixed-mode configurations across deployments and shared services

---

## Documentation Updates Required

- `docs/configuration/auth-and-identity.md`
- `docs/configuration/README.md`
- `docs/configuration/deployment-and-upstreams.md`
- `_docs/_TASKS/TASK-027-02-official-auth-and-identity-documentation-page.md`

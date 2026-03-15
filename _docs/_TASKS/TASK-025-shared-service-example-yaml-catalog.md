[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-025: Shared-Service Example YAML Catalog
# FileName: TASK-025-shared-service-example-yaml-catalog.md

**Priority:** High
**Category:** Documentation and Runtime Examples
**Estimated Effort:** Small
**Dependencies:** TASK-024
**Status:** **Done** (2026-03-15)

---

## Overview

Add real example router YAML files that demonstrate the main `shared_services` execution patterns implemented in the repository.

Business goal:
- make the shared-services execution model easier to reuse
- provide concrete copyable examples for backend and platform design work
- keep the official docs linked to real versioned config examples, not only inline snippets

---

## Sub-Tasks

### TASK-025-01: Official shared-service example router configs

**Status:** Done (2026-03-15)

Add versioned example router YAML files for direct backend access, router proxy with a single endpoint, and router proxy with tiered failover.

---

## Testing Requirements

- YAML examples stay valid against the current config contract
- official docs link to the real example files

---

## Documentation Updates Required

- `docs/configuration/shared-services.md`
- `configs/examples/shared-services-direct-backend-access.router.yaml`
- `configs/examples/shared-services-router-proxy-single-endpoint.router.yaml`
- `configs/examples/shared-services-router-proxy-tiered-failover.router.yaml`
- `_docs/_TASKS/TASK-025-shared-service-example-yaml-catalog.md`
- `_docs/_TASKS/TASK-025-01-official-shared-service-example-router-configs.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`

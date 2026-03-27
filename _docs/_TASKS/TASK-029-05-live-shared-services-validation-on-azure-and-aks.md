[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029](./TASK-029-live-azure-validation-expansion-for-router-surfaces.md)

# TASK-029-05: Live Shared-Services Validation on Azure and AKS
# FileName: TASK-029-05-live-shared-services-validation-on-azure-and-aks.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029, TASK-029-01
**Status:** **Done** (2026-03-18)

---

## Overview

Add live validation for the shared-service execution model.

Candidate checks:
- `router_proxy + single_endpoint`
- `router_proxy + tiered_failover`
- `direct_backend_access` remains metadata-only and fails closed when executed through router
- live downstream target for shared services is provisioned and observable

## Sub-Tasks

### TASK-029-05-01: Live shared-services AKS scope and Azure direct-access fixture

**Status:** Done (2026-03-18)

Create a dedicated AKS scope and provision a real Azure Storage endpoint for direct backend access.

### TASK-029-05-02: Live shared-services router config and mock downstreams

**Status:** Done (2026-03-18)

Render a dedicated router config and deploy in-cluster mock downstreams for router-proxy scenarios.

### TASK-029-05-03: Live shared-services suite, runner, and docs rollout

**Status:** Done (2026-03-18)

Add the dedicated live suite, its make target, and official docs coverage.

---

## Documentation Updates Required

- `infra/e2e-aks-live-shared-services/`
- `scripts/release/render_live_shared_services_router_config.py`
- `tests/e2e_aks_live_shared_services/`
- `Makefile`
- `scripts/release/run_azure_test_suite.sh`
- `.env.example`
- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
- `docs/getting-started/implementation-status.md`
- `_docs/_TASKS/TASK-029-05-live-shared-services-validation-on-azure-and-aks.md`
- `_docs/_TASKS/TASK-029-05-01-live-shared-services-aks-scope-and-azure-direct-access-fixture.md`
- `_docs/_TASKS/TASK-029-05-02-live-shared-services-router-config-and-mock-downstreams.md`
- `_docs/_TASKS/TASK-029-05-03-live-shared-services-suite-runner-and-docs-rollout.md`

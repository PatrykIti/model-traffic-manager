[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-017-02: Scope Split for `integration-azure` and `e2e-aks`
# FileName: TASK-017-02-scope-split-for-integration-azure-and-e2e-aks.md

**Priority:** High
**Category:** Infrastructure Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-017
**Status:** **Done** (2026-03-14)

---

## Overview

Replace the previous combined wrapper with separate scope roots.

---

## Sub-Tasks

### TASK-017-02-01: `integration-azure` scope root and env tfvars

**Status:** Done (2026-03-14)

Create the Azure-only validation scope with its own `env/dev1.tfvars` and `env/prd1.tfvars`.

### TASK-017-02-02: `e2e-aks` scope root, k8s assets, and env tfvars

**Status:** Done (2026-03-14)

Create the AKS-backed validation scope with its own Kubernetes assets and `env/*.tfvars`.

---

## Testing Requirements

- both scope roots pass `terraform validate`
- the old combined wrapper is removed from active usage

---

## Documentation Updates Required

- `infra/README.md`
- `_docs/_INFRA/terraform-scopes-and-tfvars.md`
- `_docs/_TASKS/TASK-017-02-scope-split-for-integration-azure-and-e2e-aks.md`
- `_docs/_TASKS/TASK-017-02-01-integration-azure-scope-root-and-env-tfvars.md`
- `_docs/_TASKS/TASK-017-02-02-e2e-aks-scope-root-k8s-assets-and-env-tfvars.md`

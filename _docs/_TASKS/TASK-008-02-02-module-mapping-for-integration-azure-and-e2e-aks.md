[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-02-02: Module Mapping for `integration-azure` and `e2e-aks`
# FileName: TASK-008-02-02-module-mapping-for-integration-azure-and-e2e-aks.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008-02
**Status:** **Done** (2026-03-13)

---

## Overview

Define which infrastructure components should be composed for each higher-level test class.

---

## Mapping

### `integration-azure`

Compose only what the feature needs, for example:

- resource group
- user-assigned managed identity
- Azure OpenAI / Azure AI Foundry resource and deployment
- optional Key Vault

Do not create:

- AKS
- ACR unless absolutely required
- Redis unless the tested scenario truly depends on it

### `e2e-aks`

Compose only what in-cluster validation truly needs, for example:

- resource group
- minimal AKS cluster
- workload identity plumbing
- only the Azure dependencies needed by the specific scenario

Prefer:

- the smallest valid node pool
- the smallest valid support resource set

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-02-02-module-mapping-for-integration-azure-and-e2e-aks.md`

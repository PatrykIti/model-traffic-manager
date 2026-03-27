[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-017-01-01: Scope Boundaries for Validation Infrastructure
# FileName: TASK-017-01-01-scope-boundaries-for-validation-infrastructure.md

**Priority:** High
**Category:** Infrastructure Documentation
**Estimated Effort:** Small
**Dependencies:** TASK-017-01
**Status:** **Done** (2026-03-14)

---

## Overview

Define the active Terraform scopes for repository-owned higher-level validation.

Detailed decision:
1. `infra/integration-azure/` owns Azure-backed validation without AKS.
2. `infra/e2e-aks/` owns AKS-backed validation and its scope-local Kubernetes assets.
3. Future scopes such as `idm/` or `states/` stay reserved until the repository genuinely needs them.

---

## Testing Requirements

- workflow and release-check paths align with the documented scope roots

---

## Documentation Updates Required

- `_docs/_INFRA/terraform-scopes-and-tfvars.md`
- `_docs/_TASKS/TASK-017-01-01-scope-boundaries-for-validation-infrastructure.md`

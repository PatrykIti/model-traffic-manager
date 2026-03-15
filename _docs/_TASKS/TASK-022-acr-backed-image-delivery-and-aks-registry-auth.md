[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-022: ACR-Backed Image Delivery and AKS Registry Auth
# FileName: TASK-022-acr-backed-image-delivery-and-aks-registry-auth.md

**Priority:** High
**Category:** Delivery and Security
**Estimated Effort:** Medium
**Dependencies:** TASK-021
**Status:** **To Do**

---

## Overview

Add an Azure-native registry path so AKS validation and later delivery flows can
use ACR and Azure role assignments instead of relying on GHCR pull secrets.

Business goal:
- reduce reliance on personal PAT-backed GHCR access for Azure-backed runs
- align AKS delivery with Azure-native registry auth
- keep the local and CI operator flow deterministic and environment-scoped

## Sub-Tasks

### TASK-022-01: ACR scope and role-assignment contract

**Status:** To Do

Define the Terraform contract for ACR and the required pull permissions.

### TASK-022-02: Local and CI build-push path and naming policy

**Status:** To Do

Define how images are built, tagged, and pushed to ACR for validation suites.

### TASK-022-03: Docs and operator auth guidance

**Status:** To Do

Document the ACR path and the operator prerequisites.

## Testing Requirements

- AKS-backed runs can pull the router image from ACR without long-lived cluster
  secrets
- build and push steps follow a deterministic tagging convention

## Documentation Updates Required

- `docs/getting-started/local-development.md`
- `docs/operations/aks-configuration-delivery.md`
- `docs/operations/testing-levels-and-environments.md`
- `_docs/_INFRA/terraform-scopes-and-tfvars.md`
- `_docs/_TASKS/TASK-022-acr-backed-image-delivery-and-aks-registry-auth.md`
- `_docs/_TASKS/TASK-022-01-acr-scope-and-role-assignment-contract.md`
- `_docs/_TASKS/TASK-022-02-local-and-ci-build-push-path-and-naming-policy.md`
- `_docs/_TASKS/TASK-022-03-docs-and-operator-auth-guidance.md`

## Security Contract

- prefer Azure role assignments and managed access over static registry
  credentials
- keep any temporary fallback secret path explicit, optional, and short-lived

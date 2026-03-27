[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-017-02-02: `e2e-aks` Scope Root, K8s Assets, and Env Tfvars
# FileName: TASK-017-02-02-e2e-aks-scope-root-k8s-assets-and-env-tfvars.md

**Priority:** High
**Category:** Infrastructure Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-017-02
**Status:** **Done** (2026-03-14)

---

## Overview

Create the AKS-backed validation root with scope-local Terraform files, Kubernetes assets, and committed non-secret environment profiles.

---

## Testing Requirements

- `infra/e2e-aks/` validates locally
- AKS workflow paths resolve only against the new scope root and scope-local manifests

---

## Documentation Updates Required

- `infra/README.md`
- `_docs/_TASKS/TASK-017-02-02-e2e-aks-scope-root-k8s-assets-and-env-tfvars.md`

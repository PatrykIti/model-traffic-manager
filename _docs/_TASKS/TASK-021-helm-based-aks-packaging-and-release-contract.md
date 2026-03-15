[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-021: Helm-Based AKS Packaging and Release Contract
# FileName: TASK-021-helm-based-aks-packaging-and-release-contract.md

**Priority:** High
**Category:** Packaging and Release
**Estimated Effort:** Large
**Dependencies:** TASK-020
**Status:** **To Do**

---

## Overview

Replace the current raw AKS manifests used by the repository with a Helm-based
packaging model that can serve both validation suites and future production-like
delivery flows.

Business goal:
- stop duplicating raw manifest edits across AKS validation paths
- define a stable values contract for image, config, identity, and service
- make the AKS deployment path closer to how the router should be released later

## Sub-Tasks

### TASK-021-01: Helm chart structure and values surface

**Status:** To Do

Create the chart skeleton and the first stable values model for router
deployment.

### TASK-021-01-01: Values contract for image, config, identity, service, and probes

**Status:** To Do

Define the minimal values surface that the repository-owned chart must expose.

### TASK-021-02: AKS runner and workflow migration from raw manifests to Helm

**Status:** To Do

Move the AKS-backed runners and workflows from direct manifest application to
`helm upgrade --install`.

### TASK-021-03: Docs and operator release guidance

**Status:** To Do

Document the Helm packaging contract and the expected operator flow.

## Testing Requirements

- `helm lint` and template rendering checks must pass in repository validation
- `e2e-aks` and `e2e-aks-live-model` must deploy through the chart instead of
  raw manifest application
- the chart must support the current Workload Identity and image-pull flows

## Documentation Updates Required

- `docs/operations/aks-configuration-delivery.md`
- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
- `_docs/_INFRA/terraform-scopes-and-tfvars.md`
- `_docs/_TASKS/TASK-021-helm-based-aks-packaging-and-release-contract.md`
- `_docs/_TASKS/TASK-021-01-helm-chart-structure-and-values-surface.md`
- `_docs/_TASKS/TASK-021-01-01-values-contract-for-image-config-identity-service-and-probes.md`
- `_docs/_TASKS/TASK-021-02-aks-runner-and-workflow-migration-from-raw-manifests-to-helm.md`
- `_docs/_TASKS/TASK-021-03-docs-and-operator-release-guidance.md`

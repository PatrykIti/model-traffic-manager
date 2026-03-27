[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008: Cost-Aware Azure Test Infrastructure Orchestration Model
# FileName: TASK-008-cost-aware-azure-test-infrastructure-orchestration-model.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-007
**Status:** **Done** (2026-03-13)

---

## Overview

Define the repository approach for provisioning temporary Azure infrastructure for higher-level tests while explicitly avoiding the cost profile of a long-lived AKS cluster.

Business goal:
- support future `integration-azure` and `e2e-aks` coverage
- keep Azure spend low enough for an individual owner
- avoid standing infrastructure that burns money without active validation value
- keep orchestration close to the application repository and test workflows

Key decision:
- no long-lived AKS cluster
- GitHub Actions remains the orchestrator
- this repository owns the test harness Terraform wrapper
- reusable Terraform modules can still be consumed from the existing module source

---

## Sub-Tasks

### TASK-008-01: Trigger policy and cost guardrails for temporary Azure environments

**Status:** Done

Define when expensive Azure-backed test environments are allowed to run and how they are force-limited.

### TASK-008-02: Terraform wrapper structure and module composition model

**Status:** Done

Define how ephemeral test infrastructure is described in this repository while still reusing existing Terraform modules.

### TASK-008-03: GitHub workflow orchestration for apply, test, and destroy

**Status:** Done

Define the workflow shape that will provision infra, deploy the app, run tests, collect artifacts, and always clean up.

### TASK-008-04: Minimal Azure resource sets by testing level

**Status:** Done

Define the smallest Azure footprint needed for `integration-azure` and for fully ephemeral `e2e-aks`.

---

## Architecture

Planned structure for future implementation:

```text
infra/
|-- integration-azure/
|   |-- providers.tf
|   |-- versions.tf
|   |-- variables.tf
|   |-- locals.tf
|   |-- main.tf
|   |-- outputs.tf
|   `-- env/
|       |-- dev1.tfvars
|       `-- prd1.tfvars
`-- e2e-aks/
    |-- providers.tf
    |-- versions.tf
    |-- variables.tf
    |-- locals.tf
    |-- main.tf
    |-- outputs.tf
    |-- env/
    |   |-- dev1.tfvars
    |   `-- prd1.tfvars
    `-- k8s/

.github/workflows/
|-- integration-azure.yml
|-- e2e-aks.yml
`-- e2e-azure-janitor.yml
```

Current note:

- the repository later adopted the scope-first split above under `TASK-017`, replacing the earlier combined wrapper

---

## Core Decision

Recommended model:

1. Keep GitHub Actions as the primary orchestrator.
2. Keep a thin Terraform wrapper in this repository.
3. Reuse existing Terraform modules from the wrapper.
4. Use only temporary Azure environments for expensive tests.
5. Never rely on a permanently running AKS cluster for day-to-day development as a private owner.

Explicitly not recommended:

- webhooking from GitHub into a private Azure DevOps pipeline as the primary orchestration path
- creating a full AKS environment for every pull request by default
- leaving higher-cost Azure resources running between test windows

---

## Implementation Order

1. Finalize trigger matrix and budget guardrails.
2. Finalize Terraform wrapper boundaries and state model.
3. Finalize workflow contract for `apply -> deploy -> test -> destroy`.
4. Finalize minimal resource sets for each testing level.
5. Implement only after a feature genuinely needs the higher-level environment.

---

## Testing Requirements

- the planned model must explicitly prevent full AKS creation on every normal PR
- the planned model must include forced cleanup
- the planned model must separate `integration-azure` from `e2e-aks`
- the planned model must keep GitHub Actions as the single visible orchestration layer

---

## Documentation Updates Required

- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
- `_docs/_TASKS/TASK-008-cost-aware-azure-test-infrastructure-orchestration-model.md`
- `_docs/_TASKS/TASK-008-01-trigger-policy-and-cost-guardrails-for-temporary-azure-environments.md`
- `_docs/_TASKS/TASK-008-01-01-trigger-matrix-and-approval-rules.md`
- `_docs/_TASKS/TASK-008-01-02-cost-ttl-budget-and-cleanup-guardrails.md`
- `_docs/_TASKS/TASK-008-02-terraform-wrapper-structure-and-module-composition-model.md`
- `_docs/_TASKS/TASK-008-02-01-repo-local-wrapper-structure-and-state-boundaries.md`
- `_docs/_TASKS/TASK-008-02-02-module-mapping-for-integration-azure-and-e2e-aks.md`
- `_docs/_TASKS/TASK-008-03-github-workflow-orchestration-for-apply-test-and-destroy.md`
- `_docs/_TASKS/TASK-008-03-01-integration-azure-workflow-shape.md`
- `_docs/_TASKS/TASK-008-03-02-e2e-aks-workflow-shape-with-always-destroy.md`
- `_docs/_TASKS/TASK-008-04-minimal-azure-resource-sets-by-testing-level.md`
- `_docs/_TASKS/TASK-008-04-01-minimal-resources-for-integration-azure.md`
- `_docs/_TASKS/TASK-008-04-02-minimal-resources-for-fully-ephemeral-e2e-aks.md`
- `_docs/_CHANGELOG/8-2026-03-13-cost-aware-azure-test-infrastructure-orchestration-model.md`

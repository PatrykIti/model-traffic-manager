[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-02: Terraform Wrapper Structure and Module Composition Model
# FileName: TASK-008-02-terraform-wrapper-structure-and-module-composition-model.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008
**Status:** **Done** (2026-03-13)

---

## Overview

Define how this repository should describe temporary Azure test environments while still reusing existing Terraform modules.

---

## Sub-Tasks

### TASK-008-02-01: Repo-local wrapper structure and state boundaries

**Status:** Done

Define the Terraform wrapper footprint that belongs in this repository.

### TASK-008-02-02: Module mapping for `integration-azure` and `e2e-aks`

**Status:** Done

Define which reusable modules are invoked for which test level.

---

## Recommendation

- keep the Terraform wrapper in this repository
- keep it thin and test-harness-specific
- consume reusable modules from the existing module source
- keep state separated by test level and run context

---

## Target Structure

```text
infra/e2e/terraform/
|-- versions.tf
|-- providers.tf
|-- variables.tf
|-- locals.tf
|-- main.tf
|-- outputs.tf
|-- integration-azure.tfvars.example
`-- e2e-aks.tfvars.example
```

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-02-terraform-wrapper-structure-and-module-composition-model.md`
- `_docs/_TASKS/TASK-008-02-01-repo-local-wrapper-structure-and-state-boundaries.md`
- `_docs/_TASKS/TASK-008-02-02-module-mapping-for-integration-azure-and-e2e-aks.md`

[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-017: Terraform Scope Model and Tfvars Alignment
# FileName: TASK-017-terraform-scope-model-and-tfvars-alignment.md

**Priority:** High
**Category:** Infrastructure Structure
**Estimated Effort:** Medium
**Dependencies:** TASK-016
**Status:** **Done** (2026-03-14)

---

## Overview

Align the repository-owned Terraform layout with the scope-first and per-scope `tfvars` approach used in `genai-infrastructure`, while keeping the router repository intentionally smaller.

Business goal:
- make higher-level test infrastructure easier to edit and reason about
- avoid one mixed Terraform root for unrelated validation concerns
- keep workflow wiring, `tfvars`, and future infrastructure changes consistent with a scope-first model

---

## Sub-Tasks

### TASK-017-01: Terraform scope and tfvars guidance

**Status:** Done (2026-03-14)

Document the scope-first model, `tfvars` rules, and boundary decisions for this repository.

### TASK-017-02: Scope split for `integration-azure` and `e2e-aks`

**Status:** Done (2026-03-14)

Replace the shared wrapper with separate Terraform roots for Azure-only and AKS-backed validation.

### TASK-017-03: Workflow and release-check alignment

**Status:** Done (2026-03-14)

Update workflows and validation commands to target the new scope layout and per-scope `tfvars`.

---

## Testing Requirements

- both scope roots validate independently
- workflow YAML stays valid after path and input changes
- release validation uses the new scope paths rather than the old combined wrapper

---

## Documentation Updates Required

- `_docs/README.md`
- `_docs/_INFRA/README.md`
- `_docs/_INFRA/terraform-scopes-and-tfvars.md`
- `infra/README.md`
- `docs/operations/testing-levels-and-environments.md`
- `_docs/_TASKS/TASK-017-terraform-scope-model-and-tfvars-alignment.md`
- `_docs/_TASKS/TASK-017-01-terraform-scope-and-tfvars-guidance.md`
- `_docs/_TASKS/TASK-017-01-01-scope-boundaries-for-validation-infrastructure.md`
- `_docs/_TASKS/TASK-017-01-02-tfvars-environment-profile-rules.md`
- `_docs/_TASKS/TASK-017-02-scope-split-for-integration-azure-and-e2e-aks.md`
- `_docs/_TASKS/TASK-017-02-01-integration-azure-scope-root-and-env-tfvars.md`
- `_docs/_TASKS/TASK-017-02-02-e2e-aks-scope-root-k8s-assets-and-env-tfvars.md`
- `_docs/_TASKS/TASK-017-03-workflow-and-release-check-alignment.md`
- `_docs/_CHANGELOG/README.md`
- `_docs/_CHANGELOG/19-2026-03-14-terraform-scope-model-and-tfvars-alignment.md`

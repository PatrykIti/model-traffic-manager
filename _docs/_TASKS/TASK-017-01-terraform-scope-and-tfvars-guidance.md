[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-017-01: Terraform Scope and Tfvars Guidance
# FileName: TASK-017-01-terraform-scope-and-tfvars-guidance.md

**Priority:** High
**Category:** Infrastructure Documentation
**Estimated Effort:** Small
**Dependencies:** TASK-017
**Status:** **Done** (2026-03-14)

---

## Overview

Document the repository rules for Terraform scope boundaries and per-scope `tfvars`.

---

## Sub-Tasks

### TASK-017-01-01: Scope boundaries for validation infrastructure

**Status:** Done (2026-03-14)

Define which concerns belong in `integration-azure` and which belong in `e2e-aks`.

### TASK-017-01-02: Tfvars environment-profile rules

**Status:** Done (2026-03-14)

Define how `env/dev1.tfvars` and `env/prd1.tfvars` should be used in this smaller repository.

---

## Testing Requirements

- the written rules match the implemented layout
- the guidance stays small enough for this repository and does not copy the full external matrix

---

## Documentation Updates Required

- `_docs/_INFRA/README.md`
- `_docs/_INFRA/terraform-scopes-and-tfvars.md`
- `_docs/_TASKS/TASK-017-01-terraform-scope-and-tfvars-guidance.md`
- `_docs/_TASKS/TASK-017-01-01-scope-boundaries-for-validation-infrastructure.md`
- `_docs/_TASKS/TASK-017-01-02-tfvars-environment-profile-rules.md`

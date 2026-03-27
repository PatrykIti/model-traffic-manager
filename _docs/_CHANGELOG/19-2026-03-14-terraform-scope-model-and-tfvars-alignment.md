[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 19-2026-03-14-terraform-scope-model-and-tfvars-alignment.md

# 19. Terraform Scope Model and Tfvars Alignment

**Date:** 2026-03-14
**Version:** 0.1.0
**Tasks:** TASK-017, TASK-017-01, TASK-017-01-01, TASK-017-01-02, TASK-017-02, TASK-017-02-01, TASK-017-02-02, TASK-017-03

## Key Changes

### Scope model
- Replaced the previous combined higher-level Terraform wrapper with a scope-first layout.
- Added dedicated roots for `infra/integration-azure/` and `infra/e2e-aks/`.
- Kept the repository intentionally smaller than `genai-infrastructure` while adopting the same editing model.

### Tfvars model
- Added per-scope `env/dev1.tfvars` and `env/prd1.tfvars` files.
- Kept secrets and run-specific values out of committed `tfvars`.
- Aligned workflows and release validation to the new per-scope `tfvars` model.

### Documentation
- Added internal guidance for Terraform scopes and tfvars under `_docs/_INFRA/`.
- Added `infra/README.md` as the entry point for repository-owned infrastructure scopes.
- Updated testing and workflow documentation to reference the new scope layout.

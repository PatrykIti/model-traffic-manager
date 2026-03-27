[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 20-2026-03-14-shared-tfvars-baseline-and-scope-aware-naming.md

# 20. Shared Tfvars Baseline and Scope-Aware Naming

**Date:** 2026-03-14
**Version:** 0.1.0
**Tasks:** TASK-018, TASK-018-01, TASK-018-02

## Key Changes

### Shared tfvars model
- Added `infra/_shared/env/dev1.tfvars` and `infra/_shared/env/prd1.tfvars` as the common non-secret baseline for validation scopes.
- Removed duplicated common values from the `integration-azure` scope-local environment files.
- Reduced `e2e-aks` scope-local `tfvars` to AKS-specific override values only.

### Scope-aware naming
- Updated both active Terraform scopes so resource names include the scope identity.
- Prevented collisions between `integration-azure` and `e2e-aks` when the same environment profile and run ID are used.
- Updated workflows so they combine the shared baseline with scope-specific overrides where needed.

### Documentation
- Updated the internal Terraform guidance to describe the shared-baseline model explicitly.
- Kept the repository aligned with the genai-infrastructure style while avoiding unnecessary duplication.

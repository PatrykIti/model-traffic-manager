[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 17-2026-03-14-azure-backed-validation-activation-and-test-harness-scaffolding.md

# 17. Azure-Backed Validation Activation and Test Harness Scaffolding

**Date:** 2026-03-14
**Version:** 0.1.0
**Tasks:** TASK-016-03

## Key Changes

### Higher-level validation activation
- Added opt-in `integration-azure` and `e2e-aks` GitHub Actions workflows.
- Added a repo-local Terraform wrapper for temporary Azure-backed validation environments.
- Added a janitor workflow for expired temporary resource groups.

### Test harness
- Added `tests/integration_azure/` for Azure-backed auth validation.
- Added `tests/e2e_aks/` for AKS runtime smoke validation.
- Added AKS deployment templates for the router e2e path and validated the Terraform wrapper locally with `terraform validate`.

### Documentation
- Updated testing-level documentation to reflect the now-active higher-level validation paths.
- Kept these workflows opt-in and outside the default PR quality gate.

[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-019: Local One-Command Azure-Backed Test Runners
# FileName: TASK-019-local-one-command-azure-backed-test-runners.md

**Priority:** High
**Category:** Developer Workflow
**Estimated Effort:** Medium
**Dependencies:** TASK-016, TASK-017, TASK-018
**Status:** **Done** (2026-03-14)

---

## Overview

Add local one-command runners for `integration-azure` and `e2e-aks` that automatically read the active Azure CLI context, provision temporary infrastructure, run the selected test suite, and always destroy resources afterwards.

Business goal:
- let the operator run higher-level validation locally without manually exporting Terraform inputs
- guarantee `destroy` even when tests fail
- keep the local operator flow as close as possible to the GitHub workflow orchestration

---

## Sub-Tasks

### TASK-019-01: Local `integration-azure` runner

**Status:** Done (2026-03-14)

Provide a one-command local runner for Azure-backed integration validation.

### TASK-019-02: Local `e2e-aks` runner with guaranteed cleanup

**Status:** Done (2026-03-14)

Provide a one-command local AKS-backed runner with apply-test-destroy orchestration and cleanup traps.

### TASK-019-03: Documentation, Makefile, and operator contract

**Status:** Done (2026-03-14)

Document the local runner commands, prerequisites, and cleanup guarantees.

---

## Testing Requirements

- both local runners use the active Azure CLI context for Terraform input resolution
- `destroy` runs even when the test suite fails
- new Makefile targets and release scripts pass repository validation

---

## Documentation Updates Required

- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
- `_docs/_INFRA/terraform-scopes-and-tfvars.md`
- `_docs/_TASKS/TASK-019-local-one-command-azure-backed-test-runners.md`
- `_docs/_TASKS/TASK-019-01-local-integration-azure-runner.md`
- `_docs/_TASKS/TASK-019-01-01-azure-cli-context-and-shared-tfvars-resolution.md`
- `_docs/_TASKS/TASK-019-01-02-apply-test-destroy-wrapper-for-integration-azure.md`
- `_docs/_TASKS/TASK-019-02-local-e2e-aks-runner-with-guaranteed-cleanup.md`
- `_docs/_TASKS/TASK-019-02-01-ghcr-image-build-and-aks-deploy-contract.md`
- `_docs/_TASKS/TASK-019-02-02-trap-based-cleanup-and-diagnostics-collection.md`
- `_docs/_TASKS/TASK-019-03-documentation-makefile-and-operator-contract.md`

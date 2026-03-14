[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-019-01: Local `integration-azure` Runner
# FileName: TASK-019-01-local-integration-azure-runner.md

**Priority:** High
**Category:** Developer Workflow
**Estimated Effort:** Small
**Dependencies:** TASK-019
**Status:** **Done** (2026-03-14)

---

## Overview

Add a local runner for `integration-azure` that resolves Terraform inputs from the active Azure CLI context and executes `apply -> test -> destroy`.

---

## Sub-Tasks

### TASK-019-01-01: Azure CLI context and shared tfvars resolution

**Status:** Done (2026-03-14)

Resolve subscription and related inputs automatically from `az account show`.

### TASK-019-01-02: Apply-test-destroy wrapper for `integration-azure`

**Status:** Done (2026-03-14)

Wrap Terraform apply, test execution, and destroy in one local script with cleanup guarantees.

---

## Testing Requirements

- the runner works without manually exporting Terraform subscription variables
- `destroy` still runs when the integration test exits non-zero

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-019-01-local-integration-azure-runner.md`
- `_docs/_TASKS/TASK-019-01-01-azure-cli-context-and-shared-tfvars-resolution.md`
- `_docs/_TASKS/TASK-019-01-02-apply-test-destroy-wrapper-for-integration-azure.md`

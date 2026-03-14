[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-019-01-01: Azure CLI Context and Shared Tfvars Resolution
# FileName: TASK-019-01-01-azure-cli-context-and-shared-tfvars-resolution.md

**Priority:** High
**Category:** Developer Workflow
**Estimated Effort:** Small
**Dependencies:** TASK-019-01
**Status:** **Done** (2026-03-14)

---

## Overview

Resolve the shared Terraform inputs for local Azure-backed tests from the active Azure CLI account and the committed shared `tfvars` baseline.

---

## Testing Requirements

- the local runner reads the active Azure subscription from `az account show`
- the shared baseline `tfvars` is always included automatically

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-019-01-01-azure-cli-context-and-shared-tfvars-resolution.md`

[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-022-01: ACR Scope and Role-Assignment Contract
# FileName: TASK-022-01-acr-scope-and-role-assignment-contract.md

**Priority:** High
**Category:** Infrastructure and Security
**Estimated Effort:** Medium
**Dependencies:** TASK-022
**Status:** **To Do**

---

## Overview

Define the infrastructure shape for ACR and the pull permissions required by
the AKS-backed validation paths.

## Testing Requirements

- Terraform validation proves the ACR scope contract
- AKS can authenticate to the registry using the intended Azure-native access
  model

## Documentation Updates Required

- `_docs/_TASKS/TASK-022-01-acr-scope-and-role-assignment-contract.md`

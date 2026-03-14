[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-017-02-01: `integration-azure` Scope Root and Env Tfvars
# FileName: TASK-017-02-01-integration-azure-scope-root-and-env-tfvars.md

**Priority:** High
**Category:** Infrastructure Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-017-02
**Status:** **Done** (2026-03-14)

---

## Overview

Create the Azure-backed validation root with scope-local Terraform files and committed non-secret environment profiles.

---

## Testing Requirements

- `infra/integration-azure/` validates locally
- workflows can target `env/dev1.tfvars` or `env/prd1.tfvars`

---

## Documentation Updates Required

- `infra/README.md`
- `_docs/_TASKS/TASK-017-02-01-integration-azure-scope-root-and-env-tfvars.md`

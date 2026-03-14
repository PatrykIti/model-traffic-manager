[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-017-03: Workflow and Release-Check Alignment
# FileName: TASK-017-03-workflow-and-release-check-alignment.md

**Priority:** High
**Category:** Infrastructure Automation
**Estimated Effort:** Small
**Dependencies:** TASK-017
**Status:** **Done** (2026-03-14)

---

## Overview

Update workflows and release validation so they use the new scope roots and `env/*.tfvars` model.

Detailed work:
1. Point GitHub workflows at `infra/integration-azure/` and `infra/e2e-aks/`.
2. Use committed scope-local `env/dev1.tfvars` or `env/prd1.tfvars` instead of one mixed wrapper file.
3. Update `make release-check` to validate both active scopes independently.

---

## Testing Requirements

- workflow YAML remains valid
- release-check validates both new scope roots

---

## Documentation Updates Required

- `docs/operations/testing-levels-and-environments.md`
- `_docs/_TASKS/TASK-017-03-workflow-and-release-check-alignment.md`

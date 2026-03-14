[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-017-01-02: Tfvars Environment-Profile Rules
# FileName: TASK-017-01-02-tfvars-environment-profile-rules.md

**Priority:** High
**Category:** Infrastructure Documentation
**Estimated Effort:** Small
**Dependencies:** TASK-017-01
**Status:** **Done** (2026-03-14)

---

## Overview

Define the per-scope `env/*.tfvars` model used in this repository.

Detailed decision:
1. Keep committed, non-secret `env/dev1.tfvars` and `env/prd1.tfvars` inside each active scope.
2. Pass secrets and ephemeral identifiers such as subscription IDs and run IDs from workflows, not from committed `tfvars`.
3. Reuse the same slim shared variable contract across scopes instead of copying the full external platform model.

---

## Testing Requirements

- workflow inputs align with the new `env/*.tfvars` model
- committed `tfvars` remain non-secret

---

## Documentation Updates Required

- `_docs/_INFRA/terraform-scopes-and-tfvars.md`
- `_docs/_TASKS/TASK-017-01-02-tfvars-environment-profile-rules.md`

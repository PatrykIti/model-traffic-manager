[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-018: Shared Tfvars Baseline and Scope-Aware Naming
# FileName: TASK-018-shared-tfvars-baseline-and-scope-aware-naming.md

**Priority:** High
**Category:** Infrastructure Refinement
**Estimated Effort:** Small
**Dependencies:** TASK-017
**Status:** **Done** (2026-03-14)

---

## Overview

Refine the scope-first Terraform model so common environment values are not duplicated across validation scopes.

Business goal:
- keep one shared non-secret environment baseline for all test types
- preserve scope-specific override files only where a scope truly needs extra knobs
- make resource names explicit about the scope so parallel test levels do not collide

---

## Sub-Tasks

### TASK-018-01: Shared tfvars baseline for validation scopes

**Status:** Done (2026-03-14)

Move repeated environment values into `infra/_shared/env/*.tfvars`.

### TASK-018-02: Scope-aware naming and workflow alignment

**Status:** Done (2026-03-14)

Include scope identity in resource naming and update workflows to consume the shared baseline plus optional scope-specific overrides.

---

## Testing Requirements

- `make release-check` passes with the shared baseline model
- both scope roots validate independently
- workflow YAML remains valid after the tfvars path changes

---

## Documentation Updates Required

- `infra/README.md`
- `_docs/_INFRA/terraform-scopes-and-tfvars.md`
- `docs/operations/testing-levels-and-environments.md`
- `_docs/_TASKS/TASK-018-shared-tfvars-baseline-and-scope-aware-naming.md`
- `_docs/_CHANGELOG/README.md`
- `_docs/_CHANGELOG/20-2026-03-14-shared-tfvars-baseline-and-scope-aware-naming.md`

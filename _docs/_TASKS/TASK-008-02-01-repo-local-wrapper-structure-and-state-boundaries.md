[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-02-01: Repo-Local Wrapper Structure and State Boundaries
# FileName: TASK-008-02-01-repo-local-wrapper-structure-and-state-boundaries.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008-02
**Status:** **Done** (2026-03-13)

---

## Overview

Define the Terraform boundary that belongs in this repository.

---

## State Rules

- use a dedicated backend namespace/workspace/prefix for test infrastructure
- isolate state for:
  - `integration-azure`
  - `e2e-aks`
- do not mix application delivery state with test harness infra state
- include run-aware identifiers so failed cleanup can be traced

---

## Repository Rule

The wrapper here should describe:

- test-specific resource composition
- naming
- tagging
- lifecycle behavior

It should not duplicate the internals of the reusable modules.

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-02-01-repo-local-wrapper-structure-and-state-boundaries.md`

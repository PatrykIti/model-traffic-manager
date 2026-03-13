[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-04: Minimal Azure Resource Sets by Testing Level
# FileName: TASK-008-04-minimal-azure-resource-sets-by-testing-level.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008
**Status:** **Done** (2026-03-13)

---

## Overview

Define the smallest resource sets that honestly support each higher-level test class.

---

## Sub-Tasks

### TASK-008-04-01: Minimal resources for `integration-azure`

**Status:** Done

Define the smallest Azure footprint for provider/auth integration without AKS.

### TASK-008-04-02: Minimal resources for fully ephemeral `e2e-aks`

**Status:** Done

Define the smallest Azure footprint for cluster runtime validation.

---

## Rule

Provision only what the specific scenario proves.

Do not create:

- AKS for tests that only need provider auth behavior
- Redis for tests that do not exercise shared state
- ACR if a cheaper registry path is acceptable for the test

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-04-minimal-azure-resource-sets-by-testing-level.md`
- `_docs/_TASKS/TASK-008-04-01-minimal-resources-for-integration-azure.md`
- `_docs/_TASKS/TASK-008-04-02-minimal-resources-for-fully-ephemeral-e2e-aks.md`

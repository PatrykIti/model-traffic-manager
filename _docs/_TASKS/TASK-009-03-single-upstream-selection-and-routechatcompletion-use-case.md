[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009-03: Single-Upstream Selection and `RouteChatCompletion` Use Case
# FileName: TASK-009-03-single-upstream-selection-and-routechatcompletion-use-case.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-009-02
**Status:** **Done** (2026-03-13)

---

## Overview

Implement the first real request orchestration path in the application layer.

Scope:
- deployment lookup
- single-upstream selection
- auth header build
- outbound invocation
- response handoff

---

## Sub-Tasks

### TASK-009-03-01: Single-upstream candidate selection from the deployment registry

**Status:** Done (2026-03-13)

Define the minimal selection rule before multi-upstream routing exists.

### TASK-009-03-02: `RouteChatCompletion` orchestration and response handling

**Status:** Done (2026-03-13)

Implement the first routing use case end-to-end in the application layer.

---

## Testing Requirements

- deployment lookup failure is covered
- upstream selection is deterministic for the single-upstream case
- orchestration does not leak infrastructure details into the use case contract

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-009-03-single-upstream-selection-and-routechatcompletion-use-case.md`
- `_docs/_TASKS/TASK-009-03-01-single-upstream-candidate-selection-from-the-deployment-registry.md`
- `_docs/_TASKS/TASK-009-03-02-routechatcompletion-orchestration-and-response-handling.md`

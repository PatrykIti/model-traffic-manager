[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009-02: Outbound Invocation and Auth Header Preparation
# FileName: TASK-009-02-outbound-invocation-and-auth-header-preparation.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-009-01
**Status:** To Do

---

## Overview

Implement the reusable plumbing required to call one upstream safely.

Scope:
- outbound invoker port and implementation
- secret provider contract for `api_key`
- auth header builder for `none` and `api_key`

---

## Sub-Tasks

### TASK-009-02-01: Outbound invoker contract and `httpx` implementation

**Status:** To Do

Create the outbound call abstraction and the first `httpx`-based implementation.

### TASK-009-02-02: Secret provider contract and env-backed bootstrap implementation

**Status:** To Do

Create the minimal secret resolution path for `api_key` auth.

### TASK-009-02-03: Auth header builder for `none` and `api_key`

**Status:** To Do

Create the reusable auth-header path used by the route use case.

---

## Testing Requirements

- outbound invoker is unit-testable without a real upstream
- auth headers for `none` and `api_key` are covered by unit tests
- secret resolution failure paths are covered

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-009-02-outbound-invocation-and-auth-header-preparation.md`
- `_docs/_TASKS/TASK-009-02-01-outbound-invoker-contract-and-httpx-implementation.md`
- `_docs/_TASKS/TASK-009-02-02-secret-provider-contract-and-env-backed-bootstrap-implementation.md`
- `_docs/_TASKS/TASK-009-02-03-auth-header-builder-for-none-and-api-key.md`

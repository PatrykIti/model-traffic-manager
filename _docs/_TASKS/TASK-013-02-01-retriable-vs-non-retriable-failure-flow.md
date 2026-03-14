[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-013-02-01: Retriable vs Non-Retriable Failure Flow
# FileName: TASK-013-02-01-retriable-vs-non-retriable-failure-flow.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-013-02
**Status:** **To Do**

---

## Overview

Define the attempt-loop behavior around retriable and non-retriable failures.

Detailed work:
1. Retry only for timeout, connection error, `429`, `500`, `502`, `503`, `504`, and recognized quota exhaustion.
2. Do not fail over on `400`, `401`, `403`, `404`, or request validation errors.
3. Keep the failure mapping explicit so API behavior stays predictable.

---

## Testing Requirements

- status-code and exception handling stay aligned with the documented retry rules
- the attempt loop does not exceed the configured maximum
- the final error surface remains deterministic when no candidate can succeed

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-013-02-01-retriable-vs-non-retriable-failure-flow.md`

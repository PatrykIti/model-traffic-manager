[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-015-01: Deployment-Level Limit Contracts and Rejection Model
# FileName: TASK-015-01-deployment-level-limit-contracts-and-rejection-model.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-015
**Status:** **To Do**

---

## Overview

Define the application-facing limiter contracts for the MVP.

Detailed work:
1. Keep rate limiting and concurrency limiting explicit in the application layer.
2. Return a repository-owned rejection outcome instead of adapter-specific errors.
3. Preserve enough metadata for future logs and metrics without over-designing the API.

---

## Testing Requirements

- the limiter contracts stay independent from Redis or FastAPI details
- rejection outcomes can be mapped cleanly to HTTP behavior
- accepted and rejected cases remain deterministic in unit tests

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-015-01-deployment-level-limit-contracts-and-rejection-model.md`

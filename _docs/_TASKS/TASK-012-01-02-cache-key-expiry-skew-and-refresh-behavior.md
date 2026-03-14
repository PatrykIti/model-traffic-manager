[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-012-01-02: Cache Key, Expiry Skew, and Refresh Behavior
# FileName: TASK-012-01-02-cache-key-expiry-skew-and-refresh-behavior.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-012-01
**Status:** **To Do**

---

## Overview

Define the in-memory caching rules for Managed Identity tokens.

Detailed work:
1. Use `(auth_mode, client_id, scope)` as the cache key.
2. Add an expiry skew so nearly expired tokens are refreshed before dispatch.
3. Keep the cache per-process and explicit instead of adding shared state in this phase.

---

## Testing Requirements

- cached tokens are reused only while safely valid
- refresh behavior is deterministic near expiry boundaries
- cache misses and refreshes do not change the application-layer contract

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-012-01-02-cache-key-expiry-skew-and-refresh-behavior.md`

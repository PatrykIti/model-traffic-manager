[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-014-02-02: Redis-Backed Repository Adapter and Persistence Behavior
# FileName: TASK-014-02-02-redis-backed-repository-adapter-and-persistence-behavior.md

**Priority:** High
**Category:** Infrastructure Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-014-02
**Status:** **To Do**

---

## Overview

Add the Redis-backed adapter for shared health state across router instances.

Recommended approach:
- keep Redis details inside infrastructure only
- store a compact repository-owned representation of health state
- make TTL and cleanup rules explicit instead of implicit adapter side effects

---

## Testing Requirements

- adapter tests cover serialization, expiration behavior, and absent-state loading
- Redis failures surface through repository-owned exceptions or fallback rules
- the application layer stays isolated from Redis client details

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-014-02-02-redis-backed-repository-adapter-and-persistence-behavior.md`

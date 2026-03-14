[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-014-02-01: In-Memory Bootstrap Repository and Transition Tests
# FileName: TASK-014-02-01-in-memory-bootstrap-repository-and-transition-tests.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-014-02
**Status:** **To Do**

---

## Overview

Add an in-memory health repository so the new behavior remains cheap and deterministic locally.

Detailed work:
1. Support per-upstream load and save operations.
2. Apply success and failure transition rules in a repository-owned form.
3. Keep the implementation small and explicit for unit and local integration tests.

---

## Testing Requirements

- unseen upstreams load as healthy by default
- success clears consecutive failure state as designed
- cooldown and circuit-open transitions can be asserted without Redis

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-014-02-01-in-memory-bootstrap-repository-and-transition-tests.md`

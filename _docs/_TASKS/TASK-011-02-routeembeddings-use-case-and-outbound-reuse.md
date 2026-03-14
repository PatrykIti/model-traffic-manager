[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-011-02: `RouteEmbeddings` Use Case and Outbound Reuse
# FileName: TASK-011-02-routeembeddings-use-case-and-outbound-reuse.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-011
**Status:** **To Do**

---

## Overview

Implement the embeddings use case with the same deterministic single-upstream bootstrap model used by chat completions.

Recommended approach:
- add a dedicated `RouteEmbeddings` use case instead of overloading the chat use case
- reuse the existing auth header builder and outbound invoker ports
- keep shared code explicit and small instead of introducing a generic abstraction too early

---

## Testing Requirements

- the use case resolves deployments from the same registry as the chat path
- the first configured upstream is selected deterministically in Phase 2
- outbound invocation reuses the existing adapter contracts without endpoint-specific regressions

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-011-02-routeembeddings-use-case-and-outbound-reuse.md`

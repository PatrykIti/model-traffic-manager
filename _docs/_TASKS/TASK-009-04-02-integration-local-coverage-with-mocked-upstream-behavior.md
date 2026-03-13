[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009-04-02: `integration-local` Coverage with Mocked Upstream Behavior
# FileName: TASK-009-04-02-integration-local-coverage-with-mocked-upstream-behavior.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-009-04
**Status:** To Do

---

## Overview

Prove the first proxy path with local integration tests and mocked upstream behavior.

Recommended approach:
- use `respx` for outbound HTTP mocking
- keep tests inside the repository process
- do not introduce Azure yet

---

## Detailed Work Items

1. Add success-path integration test.
2. Add deployment-not-found integration test.
3. Add upstream failure integration test.
4. Assert response passthrough behavior and HTTP mapping.

---

## Testing Requirements

- mocked upstream responses drive the route end-to-end
- no real network dependency is required
- tests remain deterministic and cheap enough for default PR execution

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-009-04-02-integration-local-coverage-with-mocked-upstream-behavior.md`

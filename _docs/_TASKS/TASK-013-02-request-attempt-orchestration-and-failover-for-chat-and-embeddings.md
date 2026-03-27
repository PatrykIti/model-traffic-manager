[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-013-02: Request-Attempt Orchestration and Failover for Chat and Embeddings
# FileName: TASK-013-02-request-attempt-orchestration-and-failover-for-chat-and-embeddings.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-013
**Status:** **Done** (2026-03-14)

---

## Overview

Extend the proxy use cases so retriable failures can move across candidates without hiding non-retriable failures.

---

## Sub-Tasks

### TASK-013-02-01: Retriable vs non-retriable failure flow

**Status:** Done (2026-03-14)

Define when the router attempts another upstream and when it returns immediately.

### TASK-013-02-02: Decision reasons and next-candidate transitions

**Status:** Done (2026-03-14)

Preserve enough decision context to explain why the router moved to the next candidate.

---

## Testing Requirements

- non-retriable failures stop the attempt loop immediately
- retriable failures can move to another candidate in the selected policy order
- chat and embeddings use cases stay behaviorally aligned

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-013-02-request-attempt-orchestration-and-failover-for-chat-and-embeddings.md`
- `_docs/_TASKS/TASK-013-02-01-retriable-vs-non-retriable-failure-flow.md`
- `_docs/_TASKS/TASK-013-02-02-decision-reasons-and-next-candidate-transitions.md`

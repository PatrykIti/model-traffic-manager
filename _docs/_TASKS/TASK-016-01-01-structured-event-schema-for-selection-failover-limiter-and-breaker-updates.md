[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-016-01-01: Structured Event Schema for Selection, Failover, Limiter, and Breaker Updates
# FileName: TASK-016-01-01-structured-event-schema-for-selection-failover-limiter-and-breaker-updates.md

**Priority:** High
**Category:** Observability Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-016-01
**Status:** **Done** (2026-03-14)

---

## Overview

Define the structured event shapes emitted by the router's core decision paths.

Detailed work:
1. Capture selection, failover, limiter rejection, cooldown, and circuit-breaker changes.
2. Include deployment ID, upstream ID, tier, reason, and correlation metadata where relevant.
3. Keep secrets, raw tokens, and unnecessary prompt payload data out of the emitted events.

---

## Testing Requirements

- event payloads are serializable and stable under test
- sensitive fields are absent or explicitly redacted
- event names and reason values remain consistent with reference docs

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-016-01-01-structured-event-schema-for-selection-failover-limiter-and-breaker-updates.md`

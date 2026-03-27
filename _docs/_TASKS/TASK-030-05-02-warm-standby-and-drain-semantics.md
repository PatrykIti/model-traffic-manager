[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-030-05](./TASK-030-05-advanced-balancing-controls-examples-and-documentation.md)

# TASK-030-05-02: Warm-Standby and Drain Semantics
# FileName: TASK-030-05-02-warm-standby-and-drain-semantics.md

**Priority:** High
**Category:** Routing Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-030-05
**Status:** **Done** (2026-03-17)

---

## Overview

Define operator-controlled states that are not failures:

- `warm_standby`
  upstream is healthy and ready, but should not take normal traffic
- `drain`
  upstream should stop receiving new traffic without being marked unhealthy

The goal is to support graceful operational control without abusing health states.

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-030-05-02-warm-standby-and-drain-semantics.md`

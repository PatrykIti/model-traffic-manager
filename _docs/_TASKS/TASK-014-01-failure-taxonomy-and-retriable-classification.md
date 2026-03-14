[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-014-01: Failure Taxonomy and Retriable Classification
# FileName: TASK-014-01-failure-taxonomy-and-retriable-classification.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-014
**Status:** **To Do**

---

## Overview

Define the failure model that drives retries, cooldown, and circuit breaker updates.

---

## Sub-Tasks

### TASK-014-01-01: HTTP, network, and quota signatures and mapping rules

**Status:** To Do

Define how transport, HTTP, and quota-related failures map into router-owned classifications.

### TASK-014-01-02: `Retry-After` parsing and cooldown semantics

**Status:** To Do

Define how `429` responses influence cooldown state and retry timing.

---

## Testing Requirements

- failure classes remain explicit and repository-owned
- retriable and non-retriable outcomes stay aligned with the routing contract
- quota exhaustion recognition stays testable and documented

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-014-01-failure-taxonomy-and-retriable-classification.md`
- `_docs/_TASKS/TASK-014-01-01-http-network-and-quota-signatures-and-mapping-rules.md`
- `_docs/_TASKS/TASK-014-01-02-retry-after-parsing-and-cooldown-semantics.md`

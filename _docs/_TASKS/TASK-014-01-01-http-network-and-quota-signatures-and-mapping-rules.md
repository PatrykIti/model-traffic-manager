[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-014-01-01: HTTP, Network, and Quota Signatures and Mapping Rules
# FileName: TASK-014-01-01-http-network-and-quota-signatures-and-mapping-rules.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-014-01
**Status:** **To Do**

---

## Overview

Define the canonical mapping from outbound failures to router-owned failure reasons.

Detailed work:
1. Classify timeout and connection errors separately from HTTP status failures.
2. Recognize `429`, `5xx`, and known quota exhaustion signatures as retriable in the right cases.
3. Preserve non-retriable handling for request and authorization errors.

---

## Testing Requirements

- the classifier treats transport failures and HTTP failures consistently
- recognized quota exhaustion remains explicit rather than heuristic-by-accident
- mapping rules can be exercised with unit tests only

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-014-01-01-http-network-and-quota-signatures-and-mapping-rules.md`

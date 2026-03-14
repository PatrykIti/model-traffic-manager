[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-016-01-02: Reference Documentation and Troubleshooting Views
# FileName: TASK-016-01-02-reference-documentation-and-troubleshooting-views.md

**Priority:** High
**Category:** Documentation
**Estimated Effort:** Small
**Dependencies:** TASK-016-01
**Status:** **Done** (2026-03-14)

---

## Overview

Explain how operators should interpret the router's decision data and troubleshooting outputs.

Detailed work:
1. Expand the decision reasons reference page.
2. Add troubleshooting-oriented examples for selection, failover, limiting, and breaker state changes.
3. Keep the reference pages aligned with the real emitted field names.

---

## Testing Requirements

- operator-facing examples stay aligned with the real event schema
- troubleshooting flows remain understandable without internal code knowledge
- documentation does not expose secrets or unsafe logging guidance

---

## Documentation Updates Required

- `docs/reference/decision-reasons.md`
- `_docs/_TASKS/TASK-016-01-02-reference-documentation-and-troubleshooting-views.md`

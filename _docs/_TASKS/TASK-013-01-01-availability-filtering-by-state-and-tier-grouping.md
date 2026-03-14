[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-013-01-01: Availability Filtering by State and Tier Grouping
# FileName: TASK-013-01-01-availability-filtering-by-state-and-tier-grouping.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-013-01
**Status:** **To Do**

---

## Overview

Define how the router narrows the candidate set before balancing.

Detailed work:
1. Read the current health state for each upstream.
2. Filter out `unhealthy`, `cooldown`, and `circuit_open` candidates.
3. Group the remaining candidates by tier and pick the lowest available tier.

---

## Testing Requirements

- the default state for an unseen upstream is still treated as available
- tier grouping happens only after availability filtering
- an empty candidate set returns the repository-owned no-healthy-upstream outcome

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-013-01-01-availability-filtering-by-state-and-tier-grouping.md`

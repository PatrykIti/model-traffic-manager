[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-030](./TASK-030-model-aware-load-balancing-within-tier.md)

# TASK-030-02: Selector Behavior for Compatible Pools Within a Tier
# FileName: TASK-030-02-selector-behavior-for-compatible-pools-within-a-tier.md

**Priority:** High
**Category:** Routing Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-030, TASK-030-01
**Status:** **To Do**

---

## Overview

Extend the same-tier selector so it balances only within a compatibility pool instead of across every same-tier upstream blindly.

Recommended behavior:
- filter unavailable upstreams first
- choose the lowest available tier
- within that tier, choose the active compatibility pool
- apply weighted round robin only inside that pool

Open design point:
- whether pool choice should be deterministic or configurable when multiple compatible pools coexist in the same tier

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-030-02-selector-behavior-for-compatible-pools-within-a-tier.md`

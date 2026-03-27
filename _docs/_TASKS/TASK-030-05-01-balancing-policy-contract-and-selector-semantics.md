[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-030-05](./TASK-030-05-advanced-balancing-controls-examples-and-documentation.md)

# TASK-030-05-01: Balancing Policy Contract and Selector Semantics
# FileName: TASK-030-05-01-balancing-policy-contract-and-selector-semantics.md

**Priority:** High
**Category:** Routing Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-030-05
**Status:** **Done** (2026-03-17)

---

## Overview

Define whether the router should support explicit balancing policies such as:

- `weighted_round_robin`
- `active_standby`

Questions to settle:
- where the policy lives in config
- whether policy is per deployment, per compatibility pool, or per upstream
- how the selector explains policy decisions to operators

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-030-05-01-balancing-policy-contract-and-selector-semantics.md`

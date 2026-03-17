[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-030](./TASK-030-model-aware-load-balancing-within-tier.md)

# TASK-030-06: Commented Example YAML Catalog for Load-Balancing Scenarios
# FileName: TASK-030-06-commented-example-yaml-catalog-for-load-balancing-scenarios.md

**Priority:** High
**Category:** Documentation Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-030, TASK-030-03, TASK-030-04
**Status:** **To Do**

---

## Overview

Publish commented example router configs that show how to use load balancing safely.

Required example families:
- chat active-active across the same model in multiple regions
- chat with active-active primary pool plus model fallback tiers
- embeddings balancing only inside a safe compatibility group
- mixed pool examples that demonstrate why incompatible upstreams must not share a compatibility group

Rule:
- comments in the YAML must explain the operator intent, not only the field meaning

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-030-06-commented-example-yaml-catalog-for-load-balancing-scenarios.md`

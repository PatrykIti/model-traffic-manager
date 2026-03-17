[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-030](./TASK-030-model-aware-load-balancing-within-tier.md)

# TASK-030-04: Embeddings-Specific Safety Rules
# FileName: TASK-030-04-embeddings-specific-safety-rules.md

**Priority:** High
**Category:** Routing Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-030, TASK-030-01, TASK-030-02
**Status:** **Done** (2026-03-17)

---

## Overview

Define stricter rules for embeddings pools than for chat pools.

Recommended default:
- only balance embeddings upstreams when the embedding model and vector-space contract are equivalent
- do not mix `text-embedding-3-small` and `text-embedding-3-large` in one balanced pool
- treat different embeddings models as different compatibility groups unless explicitly proven safe

Reason:
- unsafe embeddings mixing can break vector-store consistency and retrieval quality

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-030-04-embeddings-specific-safety-rules.md`

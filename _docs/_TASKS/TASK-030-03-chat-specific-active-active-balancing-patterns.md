[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-030](./TASK-030-model-aware-load-balancing-within-tier.md)

# TASK-030-03: Chat-Specific Active-Active Balancing Patterns
# FileName: TASK-030-03-chat-specific-active-active-balancing-patterns.md

**Priority:** High
**Category:** Routing Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-030, TASK-030-01, TASK-030-02
**Status:** **Done** (2026-03-17)

---

## Overview

Define safe active-active balancing patterns for chat deployments.

Recommended supported patterns:
- same model, same version, different region
- same model, same version, different account
- same model, same version, different deployment copy on the same account

Recommended default:
- different model families should not be balanced in the same tier by default
- different model families may still be used as higher-tier fallback

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-030-03-chat-specific-active-active-balancing-patterns.md`

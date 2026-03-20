[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040-04](./TASK-040-04-retry-and-resilience-policy-for-runner-side-external-operations.md)

# TASK-040-04-01: Retry Policy Catalog and Matchers
# FileName: TASK-040-04-01-retry-policy-catalog-and-matchers.md

**Priority:** High
**Category:** Reliability Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-040-04
**Status:** **Done** (2026-03-20)

---

## Overview

Define retry policy classes and the transient-error matcher used by the Azure-backed and AKS-backed runner.

## Documentation Updates Required

- `scripts/release/retry_policy.py`
- `tests/unit/release/test_retry_policy.py`

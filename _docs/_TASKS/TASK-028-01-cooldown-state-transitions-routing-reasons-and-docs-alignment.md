[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-028](./TASK-028-explicit-cooldown-state-semantics-and-observability.md)

# TASK-028-01: Cooldown State Transitions, Routing Reasons, and Docs Alignment
# FileName: TASK-028-01-cooldown-state-transitions-routing-reasons-and-docs-alignment.md

**Priority:** High
**Category:** Domain Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-028
**Status:** **Done** (2026-03-16)

---

## Overview

Use `HealthStatus.COOLDOWN` as the actual temporary exclusion state while keeping `last_failure_reason` as the explanation for why the cooldown was applied.

Target behavior:
- `429` enters `cooldown` with `last_failure_reason=rate_limited`
- `quota_exhausted` enters `cooldown` with `last_failure_reason=quota_exhausted`
- retryable health failures below the circuit threshold enter `cooldown` with `last_failure_reason=unhealthy` or transport reason
- selector rejection reasons expose `cooldown_*` variants for clearer operator diagnostics

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-028-01-cooldown-state-transitions-routing-reasons-and-docs-alignment.md`

[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 30: Explicit Cooldown State Semantics and Observability

**Date:** 2026-03-16
**Version:** 0.1.0
**Tasks:**
- TASK-028
- TASK-028-01

---

## Key Changes

### Domain behavior

- made `cooldown` the real temporary exclusion state for retriable but not-yet-circuit-open upstream failures
- kept `last_failure_reason` as the explanation for why the cooldown was applied
- preserved half-open and circuit-open behavior on top of the new cooldown semantics

### Routing and diagnostics

- selector rejection reasons now distinguish cooldown causes such as `cooldown_rate_limited` and `cooldown_unhealthy`
- improved operator visibility without changing the overall failover model
- retained normalization support for older persisted temporary states

### Validation and docs

- updated unit coverage for cooldown transitions and rejection reasons
- updated routing and implementation-status docs to describe explicit cooldown semantics

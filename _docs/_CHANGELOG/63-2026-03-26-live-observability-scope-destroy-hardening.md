[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 63: Live Observability Scope Destroy Hardening

**Date:** 2026-03-26
**Version:** 0.1.0
**Tasks:**
- TASK-046

---

## Key Changes

### Temporary Scope Cleanup

- updated the `e2e-aks-live-observability` AzureRM provider features block to allow RG deletion even when Application Insights leaves nested Smart Detection resources behind
- kept the override limited to this ephemeral validation scope so repository-wide destroy safety is unchanged

[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 33: E2E AKS Live Chat Failover Scenarios

**Date:** 2026-03-16
**Version:** 0.1.0
**Tasks:**
- TASK-029-04

---

## Key Changes

### Live validation profile

- extended the existing `e2e-aks-live-model` suite with controlled failover scenarios
- added an in-cluster mock primary that returns `429` and `503` for deterministic routing tests
- proved live router failover into a real Azure OpenAI secondary

### Health-state validation

- added live checks for `cooldown` and `circuit_open` behavior through router metrics
- kept the scenario operator-visible by asserting route-attempt and health-update counters

### Workflow and docs

- updated docs and env examples for the live failover profile overrides
- kept the implementation inside the existing live-model area instead of introducing another redundant top-level runner

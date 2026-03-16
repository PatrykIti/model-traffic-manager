[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-029](./TASK-029-live-azure-validation-expansion-for-router-surfaces.md)

# TASK-029-04: `e2e-aks-live-model` Chat Failover and Health-State Scenarios
# FileName: TASK-029-04-e2e-aks-live-model-chat-failover-and-health-state-scenarios.md

**Priority:** High
**Category:** Validation Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-029, TASK-029-01
**Status:** **To Do**

---

## Overview

Add live chat scenarios that prove more than a happy-path model response.

Candidate checks:
- regional/account failover from a degraded primary to a healthy secondary
- model fallback across tiers
- live observation of cooldown and circuit-open transitions under controlled failure conditions

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-029-04-e2e-aks-live-model-chat-failover-and-health-state-scenarios.md`

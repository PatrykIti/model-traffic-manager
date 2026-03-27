[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 31: Live Azure Validation Expansion Planning

**Date:** 2026-03-16
**Version:** 0.1.0
**Tasks:**
- TASK-029
- TASK-029-01

---

## Key Changes

### Validation planning

- defined the next live Azure validation matrix across `integration-azure`, `e2e-aks`, and `e2e-aks-live-model`
- split future work into dedicated profiles for embeddings, chat failover, shared services, and Redis-backed multi-replica validation
- kept the plan intentionally profile-based so failures stay attributable and suite cost remains controllable

### Workflow alignment

- added formal task files for the upcoming live validation expansion
- updated the task board so the next Azure-backed validation work has explicit, reviewable scope

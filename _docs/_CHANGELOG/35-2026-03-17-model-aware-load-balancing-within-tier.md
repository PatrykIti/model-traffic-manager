[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 35: Model-Aware Load Balancing Within Tier

**Date:** 2026-03-17
**Version:** 0.1.0
**Tasks:**
- TASK-030
- TASK-030-01
- TASK-030-02
- TASK-030-03
- TASK-030-04
- TASK-030-05
- TASK-030-05-01
- TASK-030-05-02
- TASK-030-05-03
- TASK-030-05-04
- TASK-030-05-05
- TASK-030-06
- TASK-030-07

---

## Key Changes

### Routing and config contract

- added model-aware same-tier balancing metadata to upstreams
- introduced compatibility-aware selection instead of blindly treating every same-tier upstream as one interchangeable pool
- added operational controls for `active_standby`, `warm_standby`, `drain`, `target_share_percent`, and `max_share_percent`

### Validation and safety

- added config validation that blocks unsafe embeddings pools and mixed compatibility groups
- added selector tests for standby, drain, and target-share behavior
- kept the first iteration explainable by grounding load-balancing controls in simple, explicit fields

### Examples, docs, and live validation

- added commented YAML catalogs for load-balancing scenarios
- added official configuration and routing documentation for the new balancing model
- added a dedicated AKS live validation package and local `make` runner for load-balancing behavior

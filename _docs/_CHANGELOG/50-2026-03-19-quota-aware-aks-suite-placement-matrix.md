[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 50: Quota-Aware AKS Suite Placement Matrix

**Date:** 2026-03-19
**Version:** 0.1.0
**Tasks:**
- TASK-040-05
- TASK-040-05-01
- TASK-040-05-02

---

## Key Changes

### AKS Validation Placement

- encoded a per-suite AKS placement matrix in scope-specific `env/*.tfvars`
- split the active validation profiles across `westeurope` and `northeurope`
- used `Standard_D2s_v4` and `Standard_D2ds_v4` as the active VM families for quota-aware placement

### Operator Guidance

- documented the current suite-to-region and suite-to-VM-family mapping
- clarified that quota-driven placement changes should be made in per-suite tfvars rather than shared defaults

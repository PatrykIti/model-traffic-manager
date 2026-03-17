[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 37: Live Load-Balancing Rendered Config Scalar Typing Fix

**Date:** 2026-03-17
**Version:** 0.1.0
**Tasks:**
- TASK-032

---

## Key Changes

### Validation runner fix

- quoted date-like `model_version` values in the rendered live load-balancing router config so YAML keeps them as strings
- removed the startup crash seen in the dedicated AKS load-balancing validation profile

### Regression coverage

- added config-loader coverage for the rendered live load-balancing config path
- asserted string preservation for both chat and embeddings `model_version` values

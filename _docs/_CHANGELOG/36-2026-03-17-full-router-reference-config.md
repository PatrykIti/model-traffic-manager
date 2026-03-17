[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 36: Full Router Reference Config

**Date:** 2026-03-17
**Version:** 0.1.0
**Tasks:**
- TASK-031
- TASK-031-01

---

## Key Changes

### Reference config

- added `configs/full-capabilities.router.yaml` as a commented full reference config
- kept `configs/example.router.yaml` small and runnable for bootstrap use
- consolidated the major router capabilities into one readable file without replacing the scenario-specific example catalog

### Official documentation

- clarified the difference between the minimal bootstrap config and the full reference config
- linked the new file from official configuration and local-development docs

### Validation

- extended config-loader coverage so the new full reference file stays valid against the current contract

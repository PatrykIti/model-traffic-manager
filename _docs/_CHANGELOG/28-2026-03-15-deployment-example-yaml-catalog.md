[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 28: Deployment Example YAML Catalog

**Date:** 2026-03-15
**Version:** 0.1.0
**Tasks:**
- TASK-026
- TASK-026-01

---

## Key Changes

### Example config catalog

- added three real example router YAML files under `configs/examples/` for model traffic
- covered regional chat failover, model-level fallback, and embeddings regional failover
- kept each example as a full router config so it can be copied and adapted directly

### Official documentation

- linked the new deployment examples from the official deployment and upstreams documentation
- clarified what each example demonstrates so future backend and platform work can choose the right pattern quickly

### Validation

- extended loader coverage so the new deployment example YAML files are validated against the current config contract

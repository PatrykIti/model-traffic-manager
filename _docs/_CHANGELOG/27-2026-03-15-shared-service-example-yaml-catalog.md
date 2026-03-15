[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 27: Shared-Service Example YAML Catalog

**Date:** 2026-03-15
**Version:** 0.1.0
**Tasks:**
- TASK-025
- TASK-025-01

---

## Key Changes

### Example config catalog

- added three real example router YAML files under `configs/examples/`
- covered direct backend access, router proxy with a single endpoint, and router proxy with tiered failover
- kept each example as a full router config so it can be copied and adapted directly

### Official documentation

- linked the new example files from the official shared-services documentation
- kept the inline snippets while adding versioned file-based examples for practical reuse

### Validation

- added loader coverage to prove that the new example YAML files stay valid against the current config contract

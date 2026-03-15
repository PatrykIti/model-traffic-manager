[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 29: Auth and Identity Example YAML Catalog

**Date:** 2026-03-15
**Version:** 0.1.0
**Tasks:**
- TASK-027
- TASK-027-01
- TASK-027-02

---

## Key Changes

### Example config catalog

- added three real example router YAML files under `configs/examples/` for auth and identity patterns
- covered default process identity, explicit `client_id` selection, and mixed auth modes
- kept each example as a full router config so it can be copied and adapted directly

### Official documentation

- added a dedicated official docs page for auth and identity behavior
- linked the new examples from the configuration docs
- clarified how the router chooses the default process identity versus an explicit user-assigned identity

### Validation

- extended loader coverage so the new auth and identity example YAML files are validated against the current config contract

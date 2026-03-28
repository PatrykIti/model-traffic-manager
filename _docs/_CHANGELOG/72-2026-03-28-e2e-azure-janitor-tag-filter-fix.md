[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 72: E2E Azure Janitor Tag Filter Fix

**Date:** 2026-03-28
**Version:** 0.1.0
**Tasks:**
- TASK-055

---

## Key Changes

### Janitor Workflow

- fixed the Azure janitor resource-group filter so it no longer passes two tag filters to `az group list --tag`
- moved the two-tag selection into the JMESPath query so the cleanup workflow can correctly target repository-owned temporary resource groups

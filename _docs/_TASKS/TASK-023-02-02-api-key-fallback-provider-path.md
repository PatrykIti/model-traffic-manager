[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-023-02-02: API-Key Fallback Provider Path
# FileName: TASK-023-02-02-api-key-fallback-provider-path.md

**Priority:** High
**Category:** Higher-Level Validation
**Estimated Effort:** Small
**Dependencies:** TASK-023-02
**Status:** **To Do**

---

## Overview

Add an explicit opt-in Azure-backed validation path for provider calls that use
`api_key` fallback instead of Managed Identity.

## Testing Requirements

- the path is explicit and does not silently consume API-key configuration
- provider responses and auth failures are observable and attributable

## Documentation Updates Required

- `_docs/_TASKS/TASK-023-02-02-api-key-fallback-provider-path.md`

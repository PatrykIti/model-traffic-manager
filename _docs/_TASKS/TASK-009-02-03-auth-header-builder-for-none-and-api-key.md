[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009-02-03: Auth Header Builder for `none` and `api_key`
# FileName: TASK-009-02-03-auth-header-builder-for-none-and-api-key.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-009-02
**Status:** **Done** (2026-03-13)

---

## Overview

Create the first reusable auth header builder.

This work item owns:
- no-auth path
- API key header construction path
- failure behavior for missing secret material

---

## Pseudocode

```text
if auth.mode == none:
    return {}

if auth.mode == api_key:
    secret = secret_provider.get(secret_ref)
    return {header_name: secret}
```

---

## Testing Requirements

- `none` returns empty headers
- `api_key` returns one correctly named header
- missing secret raises a deterministic application error

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-009-02-03-auth-header-builder-for-none-and-api-key.md`

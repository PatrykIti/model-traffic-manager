[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-011-01: Embeddings Request/Response Contract and API Surface
# FileName: TASK-011-01-embeddings-request-response-contract-and-api-surface.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-011
**Status:** **Done** (2026-03-14)

---

## Overview

Define the first embeddings proxy contract and expose it through the API.

Detailed work:
1. Add the application DTO for the inbound embeddings request.
2. Define the route behavior for raw request passthrough and response passthrough.
3. Keep the error mapping and response style aligned with the chat proxy path.

---

## Testing Requirements

- the route preserves the caller payload without adding router-specific shape changes
- the HTTP contract matches the same baseline behavior as the chat proxy route
- non-existent deployments map cleanly to the existing repository error surface

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-011-01-embeddings-request-response-contract-and-api-surface.md`

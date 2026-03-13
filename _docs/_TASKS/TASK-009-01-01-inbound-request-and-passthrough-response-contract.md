[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009-01-01: Inbound Request and Passthrough Response Contract
# FileName: TASK-009-01-01-inbound-request-and-passthrough-response-contract.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Small
**Dependencies:** TASK-009-01
**Status:** To Do

---

## Overview

Define the route contract for the first proxy implementation.

Decision target:
- accept the request body as provider-oriented JSON payload
- keep request validation intentionally thin in this phase
- return upstream JSON body and status code transparently when the upstream call succeeds

---

## Detailed Work Items

1. Decide whether the API route accepts a raw JSON body or a thin DTO wrapper.
2. Preserve the path shape `POST /v1/chat/completions/{deployment_id}`.
3. Preserve upstream response payload shape rather than inventing a custom response DTO.
4. Reserve extension points for future metadata/logging without changing the HTTP contract.

---

## Pseudocode

```text
POST /v1/chat/completions/{deployment_id}
    parse incoming JSON
    call RouteChatCompletion
    return upstream status + upstream JSON
```

---

## Testing Requirements

- local integration tests can assert on the raw upstream payload
- the route contract does not require provider-specific schema modeling in Phase 2

---

## Documentation Updates Required

- `docs/architecture/request-lifecycle.md`
- `_docs/_TASKS/TASK-009-01-01-inbound-request-and-passthrough-response-contract.md`

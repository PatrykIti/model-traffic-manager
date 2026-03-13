[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009-03-02: `RouteChatCompletion` Orchestration and Response Handling
# FileName: TASK-009-03-02-routechatcompletion-orchestration-and-response-handling.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-009-03
**Status:** **Done** (2026-03-13)

---

## Overview

Implement the first routing use case in the application layer.

This work item owns:
- request DTO or contract
- `RouteChatCompletion`
- error handling between repository, auth, and outbound boundaries

---

## Pseudocode

```text
RouteChatCompletion(request):
    deployment = deployment_repository.get(request.deployment_id)
    if missing:
        raise DeploymentNotFound

    upstream = select single upstream
    auth_headers = auth_header_builder.build(upstream.auth)
    response = outbound_invoker.send(...)
    return response
```

---

## Testing Requirements

- repository miss raises the expected error
- auth path is invoked only after deployment selection
- outbound call receives expected endpoint, headers, and body

---

## Documentation Updates Required

- `docs/architecture/request-lifecycle.md`
- `_docs/_TASKS/TASK-009-03-02-routechatcompletion-orchestration-and-response-handling.md`

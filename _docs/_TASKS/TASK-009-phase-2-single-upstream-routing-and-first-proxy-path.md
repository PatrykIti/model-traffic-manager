[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-009: Phase 2 Single-Upstream Routing and First Proxy Path
# FileName: TASK-009-phase-2-single-upstream-routing-and-first-proxy-path.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Large
**Dependencies:** TASK-005
**Status:** To Do

---

## Overview

Implement the first real request-routing path for the router by supporting a single upstream per deployment for chat completions.

Business goal:
- move from "deployment registry exists" to "the router can proxy a real request"
- prove the end-to-end request path before introducing failover, cooldown, circuit breaker, or Managed Identity
- establish the reusable application contracts for outbound invocation and auth header building

In scope:
- `POST /v1/chat/completions/{deployment_id}`
- single-upstream routing
- auth modes `none` and `api_key`
- outbound invocation through `httpx`
- basic error mapping and response passthrough
- unit and `integration-local` coverage

Out of scope:
- multi-upstream failover
- `managed_identity`
- embeddings
- Redis-backed state
- retry loops across multiple candidates

---

## Security Contract

- visibility: `internal`
- client auth path: not implemented in this phase; the route is assumed to run inside a trusted boundary until a later auth task formalizes client authentication
- rate-limit bucket: not implemented in this phase; route design must keep room for future per-deployment limiting
- nonce / signature / HMAC: not used in this phase
- reCAPTCHA: not applicable
- internal mode: the route is intended for internal platform use, not direct public exposure

---

## Architecture

Target additions for Phase 2:

```text
app/application/
|-- dto/
|   |-- chat_completion_request.py
|   `-- outbound_response.py
|-- ports/
|   |-- outbound_invoker.py
|   `-- secret_provider.py
`-- use_cases/
    `-- route_chat_completion.py

app/infrastructure/
|-- auth/
|   |-- auth_header_builder.py
|   `-- env_secret_provider.py
`-- http/
    `-- httpx_outbound_invoker.py

app/entrypoints/api/
`-- routes_chat.py

tests/
|-- unit/application/use_cases/test_route_chat_completion.py
|-- unit/infrastructure/auth/test_auth_header_builder.py
|-- unit/infrastructure/http/test_httpx_outbound_invoker.py
`-- integration/api/test_chat_proxy.py
```

---

## Sub-Tasks

### TASK-009-01: Chat proxy contract and error model

**Status:** To Do

Define the request/response contract and the error behavior of the first proxy path.

### TASK-009-02: Outbound invocation and auth header preparation

**Status:** To Do

Implement the reusable outbound and auth plumbing needed by the first proxy path.

### TASK-009-03: Single-upstream selection and `RouteChatCompletion` use case

**Status:** To Do

Implement the first routing use case with a single upstream and deployment lookup.

### TASK-009-04: API route and local integration proof

**Status:** To Do

Expose the proxy path through FastAPI and prove it through local integration tests.

### TASK-009-05: Documentation, task tracking, and validation alignment

**Status:** To Do

Update official docs, internal task tracking, and changelog after the implementation is complete.

---

## Implementation Order

1. Finalize the inbound/outbound contract and basic error model.
2. Implement outbound invocation and auth header preparation.
3. Implement the single-upstream use case.
4. Expose the API route and prove it through `integration-local`.
5. Update docs and tracking once implementation is complete.

---

## Testing Requirements

- unit tests for auth header building
- unit tests for outbound invoker behavior and error translation
- unit tests for `RouteChatCompletion`
- local integration test proving `/v1/chat/completions/{deployment_id}` against a mocked upstream
- `pre-commit --all-files`

---

## Documentation Updates Required

- `docs/architecture/request-lifecycle.md`
- `docs/getting-started/implementation-status.md`
- `docs/configuration/deployment-and-upstreams.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
- all TASK-009 work item files
- future changelog entry for TASK-009

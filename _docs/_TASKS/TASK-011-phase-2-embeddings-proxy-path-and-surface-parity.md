[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-011: Phase 2 Embeddings Proxy Path and Surface Parity
# FileName: TASK-011-phase-2-embeddings-proxy-path-and-surface-parity.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-009, TASK-010
**Status:** **To Do**

---

## Overview

Complete the remaining single-upstream API surface from Phase 2 by adding embeddings proxy support.

Business goal:
- support `embeddings` in addition to chat completions
- reuse the existing outbound invocation and auth plumbing
- keep the public API shape and internal architecture consistent across both MVP endpoints

In scope:
- `POST /v1/embeddings/{deployment_id}`
- `RouteEmbeddings`
- response passthrough and baseline error mapping parity
- unit and `integration-local` coverage

Out of scope:
- multi-upstream failover
- `managed_identity`
- rate limiting and concurrency limiting
- Redis-backed state

---

## Security Contract

- visibility: `internal`
- client auth path: not implemented yet; the route remains intended for trusted platform boundaries
- router outbound auth: reuse `none` and `api_key` behavior without forwarding client tokens
- rate-limit bucket: deferred to the limiting task
- internal mode: yes

---

## Sub-Tasks

### TASK-011-01: Embeddings request/response contract and API surface

**Status:** To Do

Define the embeddings route contract and its parity with the existing chat proxy surface.

### TASK-011-02: `RouteEmbeddings` use case and outbound reuse

**Status:** To Do

Implement the embeddings use case by reusing the existing outbound and auth plumbing.

### TASK-011-03: `integration-local` coverage, docs, and example config alignment

**Status:** To Do

Prove the new path locally and update the relevant docs and examples.

---

## Implementation Order

1. Finalize the embeddings route contract and DTO shape.
2. Implement `RouteEmbeddings` with deterministic single-upstream selection.
3. Expose the route and prove it through local integration coverage.
4. Update official docs, examples, and tracking.

---

## Testing Requirements

- unit tests for the embeddings use case
- route-level integration test for success, not-found, and representative upstream failure
- parity checks for auth header reuse and passthrough behavior
- `pre-commit --all-files`

---

## Documentation Updates Required

- `docs/getting-started/implementation-status.md`
- `docs/architecture/request-lifecycle.md`
- `docs/configuration/deployment-and-upstreams.md`
- `_docs/_TASKS/TASK-011-phase-2-embeddings-proxy-path-and-surface-parity.md`
- `_docs/_TASKS/TASK-011-01-embeddings-request-response-contract-and-api-surface.md`
- `_docs/_TASKS/TASK-011-02-routeembeddings-use-case-and-outbound-reuse.md`
- `_docs/_TASKS/TASK-011-03-integration-local-coverage-docs-and-example-config-alignment.md`

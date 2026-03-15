[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-024: Shared Services Execution Model and Backend-Facing Proxy Surface
# FileName: TASK-024-shared-services-execution-model-and-backend-facing-proxy-surface.md

**Priority:** High
**Category:** Core Feature Implementation
**Estimated Effort:** Large
**Dependencies:** TASK-023
**Status:** **Done** (2026-03-15)

---

## Overview

Implement the first real shared-services execution model so backend callers can use selected shared services through the router while other services remain metadata-only or provider-managed.

Business goal:
- keep `shared_services` useful to the future chatbot backend
- support multiple execution modes without collapsing into a generic gateway
- allow router-mediated HTTP/JSON execution where it adds value
- preserve metadata-only and provider-managed options for services that should not use router failover

---

## Security Contract

- shared-service execution must remain explicit and opt-in per service
- router-proxied shared services must not become an unbounded arbitrary-method or arbitrary-content gateway
- registry-only services must fail closed if a backend tries to execute them through the router
- service auth remains router-owned; no client credential forwarding

---

## Sub-Tasks

### TASK-024-01: Shared-service config and domain contract for execution modes

**Status:** Done (2026-03-15)

Add typed execution modes and routing policies for shared services.

### TASK-024-02: Backend-facing shared-service execution use case and API route

**Status:** Done (2026-03-15)

Implement the first router-owned execution path for eligible shared services.

### TASK-024-03: Tests, official docs, and changelog alignment for shared-service execution

**Status:** Done (2026-03-15)

Prove the new behavior and document it clearly.

---

## Testing Requirements

- config validation for execution-mode combinations
- unit tests for registry-only rejection, single-endpoint execution, and tiered-failover execution
- local integration tests for `POST /v1/shared-services/{service_id}`
- `uv run ruff check .`
- `uv run mypy app`
- `PYTHONPATH=. uv run pytest tests/unit tests/integration/api -q`

---

## Documentation Updates Required

- `docs/configuration/configuration-model.md`
- `docs/configuration/deployment-and-upstreams.md`
- `docs/configuration/shared-services.md`
- `docs/architecture/request-lifecycle.md`
- `docs/getting-started/implementation-status.md`
- `docs/getting-started/local-development.md`
- `docs/operations/deployment-model.md`
- `docs/operations/observability-and-health.md`
- `docs/reference/glossary.md`
- `_docs/_TASKS/TASK-024-shared-services-execution-model-and-backend-facing-proxy-surface.md`
- `_docs/_TASKS/TASK-024-01-shared-service-config-and-domain-contract-for-execution-modes.md`
- `_docs/_TASKS/TASK-024-02-backend-facing-shared-service-execution-use-case-and-api-route.md`
- `_docs/_TASKS/TASK-024-03-tests-official-docs-and-changelog-alignment-for-shared-service-execution.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`

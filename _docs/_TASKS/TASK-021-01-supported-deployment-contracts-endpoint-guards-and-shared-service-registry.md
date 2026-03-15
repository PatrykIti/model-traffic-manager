[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-021](./TASK-021-mvp-closure-runtime-state-activation-and-contract-hardening.md)

# TASK-021-01: Supported Deployment Contracts, Endpoint Guards, and Shared-Service Registry
# FileName: TASK-021-01-supported-deployment-contracts-endpoint-guards-and-shared-service-registry.md

**Priority:** High
**Category:** Core and Application Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-021
**Status:** **Done** (2026-03-15)

---

## Overview

The MVP supports only `chat/completions` and `embeddings`, so the application must reject unsupported deployment contracts instead of accepting arbitrary `kind` and `protocol` strings.

Detailed work:
1. Convert deployment `kind` and `protocol` into explicit MVP enums or equivalent constrained types.
2. Reject unsupported contracts during YAML validation and domain construction.
3. Guard request execution so chat routes only target chat deployments and embeddings routes only target embeddings deployments.
4. Introduce a real application-side registry for `shared_services`.
5. Expose a minimal runtime surface that proves `shared_services` are loaded and queryable instead of dead configuration.

---

## Security Contract

- incompatible deployment contracts must never be routed accidentally
- error messages may explain contract mismatch but must not leak secret material from config
- shared-service summaries must not surface raw secret values

---

## Testing Requirements

- config tests for unsupported deployment `kind`
- config tests for unsupported deployment `protocol`
- use-case or route tests for deployment/endpoint mismatch handling
- unit tests for shared-service registry loading
- local integration proof for the shared-service runtime surface

---

## Documentation Updates Required

- `docs/configuration/configuration-model.md`
- `docs/configuration/deployment-and-upstreams.md`
- `docs/getting-started/implementation-status.md`
- `_docs/_TASKS/TASK-021-01-supported-deployment-contracts-endpoint-guards-and-shared-service-registry.md`

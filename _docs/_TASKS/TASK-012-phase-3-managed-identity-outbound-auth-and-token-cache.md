[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-012: Phase 3 Managed Identity Outbound Auth and Token Cache
# FileName: TASK-012-phase-3-managed-identity-outbound-auth-and-token-cache.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Large
**Dependencies:** TASK-009, TASK-010
**Status:** **To Do**

---

## Overview

Implement the secretless outbound authentication path for Azure-native upstreams.

Business goal:
- make `managed_identity` the real default outbound auth mode instead of only a validated config option
- keep token acquisition explicit, cached, and testable
- preserve the separation between router outbound auth and future client auth

In scope:
- Azure token provider contract and adapter
- in-memory token cache keyed by auth mode, client ID, and scope
- auth header builder support for `managed_identity`
- unit and `integration-local` coverage with stubs

Out of scope:
- Redis-backed token cache
- AKS workload identity rollout proof
- multi-upstream failover behavior

---

## Security Contract

- visibility: `internal`
- outbound identity: router-managed only; do not forward client bearer tokens as the default model
- token storage: in-memory only for this phase
- cache key: `(auth_mode, client_id, scope)`
- logging: never log raw bearer tokens

---

## Sub-Tasks

### TASK-012-01: Azure token provider contract and in-memory cache

**Status:** To Do

Define the token acquisition contract and implement the local in-memory cache behavior.

### TASK-012-02: Managed Identity auth header integration and bootstrap wiring

**Status:** To Do

Wire Managed Identity into the auth header builder, container, and runtime validation path.

### TASK-012-03: Documentation, security contract, and operations guidance

**Status:** To Do

Explain how the new auth mode works operationally and how it stays separate from client auth.

---

## Implementation Order

1. Implement token acquisition and cache semantics.
2. Integrate `managed_identity` into auth header building and runtime wiring.
3. Add unit and local integration coverage with Azure credential stubs.
4. Update docs and security notes.

---

## Testing Requirements

- token acquisition is stub-friendly and deterministic in unit tests
- cached tokens are reused until refresh rules require a new acquisition
- `managed_identity` auth works for both chat and future embeddings use cases
- `pre-commit --all-files`

---

## Documentation Updates Required

- `docs/configuration/deployment-and-upstreams.md`
- `docs/operations/deployment-model.md`
- `docs/getting-started/implementation-status.md`
- `_docs/_TASKS/TASK-012-phase-3-managed-identity-outbound-auth-and-token-cache.md`
- `_docs/_TASKS/TASK-012-01-azure-token-provider-contract-and-in-memory-cache.md`
- `_docs/_TASKS/TASK-012-01-01-credential-selection-and-token-acquisition-semantics.md`
- `_docs/_TASKS/TASK-012-01-02-cache-key-expiry-skew-and-refresh-behavior.md`
- `_docs/_TASKS/TASK-012-02-managed-identity-auth-header-integration-and-bootstrap-wiring.md`
- `_docs/_TASKS/TASK-012-02-01-container-wiring-and-config-runtime-validation-alignment.md`
- `_docs/_TASKS/TASK-012-02-02-unit-and-local-integration-coverage-with-credential-stubs.md`
- `_docs/_TASKS/TASK-012-03-documentation-security-contract-and-operations-guidance.md`

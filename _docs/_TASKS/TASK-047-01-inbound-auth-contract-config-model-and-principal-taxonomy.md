[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-047](./TASK-047-inbound-client-auth-with-api-bearer-tokens-and-microsoft-entra-id.md)

# TASK-047-01: Inbound Auth Contract, Config Model, and Principal Taxonomy
# FileName: TASK-047-01-inbound-auth-contract-config-model-and-principal-taxonomy.md

**Priority:** High
**Category:** Security Contract
**Estimated Effort:** Medium
**Dependencies:** TASK-047
**Status:** **In Progress** (2026-03-27)

---

## Overview

Define the configuration and domain contract for inbound caller authentication.

Recommended contract split:

1. one router-level or endpoint-surface-level inbound auth policy section
2. explicit auth modes:
   - `none`
   - `api_bearer_token`
   - `entra_id`
3. a normalized request principal object emitted after successful authentication

Principal taxonomy should capture at least:

- `auth_mode`
- `principal_type`
- `principal_id`
- `display_name`
- `consumer_role` if mapped
- `entra_app_id` / `azp` when Entra ID is used

---

## Sub-Tasks

### TASK-047-01-01: API bearer token contract, generation, and storage semantics

**Status:** In Progress (2026-03-27)

Define how operators generate, store, rotate, and identify router-owned bearer tokens.

### TASK-047-01-02: Entra ID token contract, audience, issuer, and principal claims

**Status:** In Progress (2026-03-27)

Define how the router validates Entra access-token shape and which claims are required for app-only service tokens.

---

## Testing Requirements

- config validation rejects ambiguous or incomplete inbound auth definitions
- principal taxonomy stays stable across both auth modes

---

## Documentation Updates Required

- `docs/configuration/configuration-model.md`
- `docs/configuration/auth-and-identity.md`
- `_docs/_TASKS/TASK-047-01-inbound-auth-contract-config-model-and-principal-taxonomy.md`
- `_docs/_TASKS/TASK-047-01-01-api-bearer-token-contract-generation-and-storage-semantics.md`
- `_docs/_TASKS/TASK-047-01-02-entra-id-token-contract-audience-issuer-and-principal-claims.md`

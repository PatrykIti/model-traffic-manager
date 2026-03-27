[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-047-01](./TASK-047-01-inbound-auth-contract-config-model-and-principal-taxonomy.md)

# TASK-047-01-01: API Bearer Token Contract, Generation, and Storage Semantics
# FileName: TASK-047-01-01-api-bearer-token-contract-generation-and-storage-semantics.md

**Priority:** High
**Category:** Security Contract
**Estimated Effort:** Small
**Dependencies:** TASK-047-01
**Status:** To Do

---

## Overview

Define the router-owned bearer-token path.

Recommended approach:

- clients send `Authorization: Bearer <opaque-token>`
- the router stores only hashed token material or resolves it from `secret_ref`
- the repository may provide an operator helper script to generate tokens offline, but not an in-app issuance endpoint
- config should support token metadata such as `token_id`, `display_name`, `consumer_role`, `expires_at`, and `secret_ref`

Security details:

- compare token hashes in constant time
- support explicit token disable or rotation windows
- never emit the raw token in logs, traces, or config rendering output

---

## Documentation Updates Required

- `docs/configuration/auth-and-identity.md`
- `_docs/_TASKS/TASK-047-01-01-api-bearer-token-contract-generation-and-storage-semantics.md`

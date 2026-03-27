[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-047-01](./TASK-047-01-inbound-auth-contract-config-model-and-principal-taxonomy.md)

# TASK-047-01-02: Entra ID Token Contract, Audience, Issuer, and Principal Claims
# FileName: TASK-047-01-02-entra-id-token-contract-audience-issuer-and-principal-claims.md

**Priority:** High
**Category:** Security Contract
**Estimated Effort:** Small
**Dependencies:** TASK-047-01
**Status:** **In Progress** (2026-03-27)

---

## Overview

Define the Entra ID inbound token contract for service-to-service callers.

Recommended token assumptions:

- the router is a protected web API
- the access token `aud` identifies the router API app registration or its Application ID URI
- app-only callers use client-credentials style tokens acquired through a client app or managed identity with federated credentials
- authorization should use `roles` claims from API app roles for daemon/service callers

Validation contract:

- validate issuer
- validate tenant
- validate audience
- validate signature and key material from the Entra signing keys endpoint
- validate token lifetime
- validate expected `roles` or explicit caller allow-list semantics
- optionally capture `azp`, `appid`, `tid`, and `oid/sub` into the normalized principal context

---

## Documentation Updates Required

- `docs/configuration/auth-and-identity.md`
- `_docs/_TASKS/TASK-047-01-02-entra-id-token-contract-audience-issuer-and-principal-claims.md`

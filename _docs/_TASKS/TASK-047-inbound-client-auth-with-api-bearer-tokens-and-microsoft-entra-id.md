[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-047: Inbound Client Auth with API Bearer Tokens and Microsoft Entra ID
# FileName: TASK-047-inbound-client-auth-with-api-bearer-tokens-and-microsoft-entra-id.md

**Priority:** High
**Category:** Security and Access Control
**Estimated Effort:** Large
**Dependencies:** TASK-005, TASK-016, TASK-042, TASK-043
**Status:** **In Progress** (2026-03-27)

---

## Overview

Add inbound client authentication to `model-traffic-manager` so router callers can authenticate through one of two optional modes:

- repository-owned API bearer tokens
- Microsoft Entra ID access tokens

Business goals:

- let backend callers protect `chat/completions`, `embeddings`, and router-callable shared-service endpoints with explicit inbound auth
- support a simple operator-managed bearer-token path for non-Entra or lower-friction consumers
- support a first-class Microsoft Entra ID path for service-to-service authentication without client secrets by using federated identity credentials on the calling workload side
- keep router observability and explainability aligned by exposing authenticated caller identity metadata in a safe, low-cardinality way

Recommended product direction:

- API bearer tokens should be opaque router-owned bearer tokens carried in `Authorization: Bearer <token>` per RFC 6750
- Microsoft Entra ID should treat `model-traffic-manager` as a protected web API
- the token `aud` should identify the router API application, not the calling service
- each calling service should use its own client app registration or managed identity with federated credentials
- application authorization for app-only Entra tokens should rely on API app roles and `roles` claims rather than delegated scopes

Important Entra design clarification:

- for app-to-app service authentication, the "resource" or audience should normally be the router API app registration
- the "second app" per external service is the client/caller app registration, not the audience
- if you want per-service authorization, add app roles on the router API app and assign those roles to each client app or service principal

Non-goals:

- do not add a user-facing token issuance UI, portal, or tenant control-plane workflow in this repository
- do not turn the router into a general OAuth authorization server
- do not require Entra ID for every caller if bearer tokens are sufficient for a supported integration

---

## Security Contract

- API bearer tokens must never be logged in raw form and should be stored as hashes or operator-provided secret refs, not as committed plaintext
- bearer-token comparison must use constant-time verification
- inbound Entra validation must check signature, issuer, tenant, audience, token lifetime, and expected app roles or caller allow-list semantics
- the router must distinguish authentication from authorization failures and return explicit `401` versus `403` behavior
- no inbound-auth task is complete without documentation for token rotation, app registration ownership, and federated credential lifecycle

---

## Sub-Tasks

### TASK-047-01: Inbound auth contract, config model, and principal taxonomy

**Status:** In Progress (2026-03-27)

Define the repository-owned auth model for API bearer tokens and Entra ID, including config shape, caller identity metadata, and HTTP error semantics.

### TASK-047-02: Runtime authentication middleware and request principal propagation

**Status:** In Progress (2026-03-27)

Implement FastAPI-side authentication, principal resolution, and authorization checks without leaking auth material into logs or traces.

### TASK-047-03: Microsoft Entra ID protected-API model, app roles, and federated caller guidance

**Status:** In Progress (2026-03-27)

Define and document the Azure app-registration model for protecting the router as an Entra web API and onboarding calling services through federated credentials.

### TASK-047-04: Tests, examples, observability alignment, and documentation rollout

**Status:** To Do

Close the feature with examples, tests, docs, and operator guidance for token rotation, claim validation, and troubleshooting.

---

## Implementation Order

1. Define the inbound auth config contract and principal model.
2. Implement runtime token extraction, validation, and request principal propagation.
3. Publish the Entra app-registration and federated-credential model with app-role guidance.
4. Finish with tests, examples, and operator docs.

---

## Testing Requirements

- local and unit coverage must prove `401` versus `403` behavior for both auth modes
- JWT validation tests must cover issuer, audience, role, expiration, and malformed-token paths
- API token tests must cover constant-time validation and secret-lookup semantics
- observability must expose safe caller metadata without leaking tokens or raw JWTs

---

## Documentation Updates Required

- `docs/configuration/configuration-model.md`
- `docs/configuration/auth-and-identity.md`
- `docs/architecture/request-lifecycle.md`
- `docs/operations/observability-and-health.md`
- `docs/reference/glossary.md`
- `docs/getting-started/implementation-status.md`
- `_docs/_TASKS/TASK-047-inbound-client-auth-with-api-bearer-tokens-and-microsoft-entra-id.md`
- `_docs/_TASKS/TASK-047-01-inbound-auth-contract-config-model-and-principal-taxonomy.md`
- `_docs/_TASKS/TASK-047-01-01-api-bearer-token-contract-generation-and-storage-semantics.md`
- `_docs/_TASKS/TASK-047-01-02-entra-id-token-contract-audience-issuer-and-principal-claims.md`
- `_docs/_TASKS/TASK-047-02-runtime-authentication-middleware-and-request-principal-propagation.md`
- `_docs/_TASKS/TASK-047-02-01-api-token-extraction-validation-and-constant-time-verification.md`
- `_docs/_TASKS/TASK-047-02-02-entra-jwt-validation-jwks-refresh-and-authorization-decision-flow.md`
- `_docs/_TASKS/TASK-047-02-03-request-principal-context-and-audit-safe-observability-fields.md`
- `_docs/_TASKS/TASK-047-03-microsoft-entra-id-protected-api-model-app-roles-and-federated-caller-guidance.md`
- `_docs/_TASKS/TASK-047-03-01-router-api-app-registration-application-id-uri-and-app-role-design.md`
- `_docs/_TASKS/TASK-047-03-02-caller-app-registration-federated-credential-pattern-and-role-assignment-flow.md`
- `_docs/_TASKS/TASK-047-04-tests-examples-observability-alignment-and-documentation-rollout.md`
- `_docs/_TASKS/README.md`

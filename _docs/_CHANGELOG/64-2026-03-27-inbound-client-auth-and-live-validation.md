[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 64: Inbound Client Auth and Live Validation

**Date:** 2026-03-27
**Version:** 0.1.0
**Tasks:**
- TASK-047
- TASK-047-01
- TASK-047-01-01
- TASK-047-01-02
- TASK-047-02
- TASK-047-02-01
- TASK-047-02-02
- TASK-047-02-03
- TASK-047-03
- TASK-047-03-01
- TASK-047-03-02
- TASK-047-04

---

## Key Changes

### Inbound Authentication

- added router-side inbound authentication for opaque API bearer tokens and Microsoft Entra ID access tokens
- introduced a normalized request-principal model so caller identity can flow through the request context safely
- split authentication from authorization with explicit `401` versus `403` behavior

### Microsoft Entra ID

- implemented protected-API validation for Entra access tokens, including signature, tenant, issuer, audience, and app-role checks
- documented and automated the live test model where a federated workload identity obtains a token for the router API app
- wired temporary app-registration and app-role assignment scaffolding into the AKS validation runner

### Validation and Documentation

- added unit, integration, and live AKS coverage for inbound auth behavior
- added example router configs and official docs for bearer-token and Entra-based caller auth
- finished the dedicated `e2e-aks-live-inbound-auth` suite and validated it successfully end to end

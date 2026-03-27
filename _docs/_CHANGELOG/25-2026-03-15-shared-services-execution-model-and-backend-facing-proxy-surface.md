[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 25: Shared Services Execution Model and Backend-Facing Proxy Surface

**Date:** 2026-03-15
**Version:** 0.1.0
**Tasks:**
- TASK-024
- TASK-024-01
- TASK-024-02
- TASK-024-03

---

## Key Changes

### Shared-service execution model

- implemented explicit shared-service execution modes for direct backend access and router-mediated execution
- distinguished single-endpoint router proxy behavior from full tiered failover
- kept provider-managed availability separate from router-controlled failover semantics

### Backend-facing API surface

- added `POST /v1/shared-services/{service_id}` for router-callable shared services
- kept metadata-only services fail-closed when execution is attempted through the router
- reused outbound auth, request correlation, rate/concurrency limiting, and failover behavior where applicable

### Validation and documentation

- added unit and local integration coverage for direct-access rejection, single-endpoint execution, and tiered-failover execution
- updated official docs to explain shared-service execution modes, boundaries, and runtime behavior
- synchronized task tracking and changelog metadata with the completed implementation

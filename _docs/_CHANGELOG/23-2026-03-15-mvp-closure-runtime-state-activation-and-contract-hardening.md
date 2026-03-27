[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 23: MVP Closure, Runtime State Activation, and Contract Hardening

**Date:** 2026-03-15
**Version:** 0.1.0
**Tasks:**
- TASK-021
- TASK-021-01
- TASK-021-02
- TASK-021-03
- TASK-021-04

---

## Key Changes

### Contract enforcement

- restricted deployment contracts to the MVP-supported combinations only
- added request-path guards so chat and embeddings routes reject incompatible deployment contracts explicitly
- turned `shared_services` into a real runtime registry with `GET /shared-services`

### Health, failover, and explainability

- implemented half-open circuit recovery with a single probe request
- extended route-selection diagnostics with rejected-candidate metadata and explicit failover reasons
- updated routing docs to describe the real recovery and observability behavior

### Shared runtime state

- added runtime settings for `in_memory` versus `redis` state backends
- wired Redis-backed health and limiter adapters into the active bootstrap container
- closed Redis resources during application shutdown

### Validation and repository tracking

- added unit and local integration coverage for the new contract, shared-service, health, and bootstrap behavior
- extended AKS smoke coverage to include `GET /shared-services`
- updated official documentation, the task board, and the changelog index to reflect the completed MVP closure work

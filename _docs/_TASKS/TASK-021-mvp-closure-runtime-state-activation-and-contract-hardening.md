[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-021: MVP Closure, Runtime State Activation, and Contract Hardening
# FileName: TASK-021-mvp-closure-runtime-state-activation-and-contract-hardening.md

**Priority:** High
**Category:** MVP Completion and Hardening
**Estimated Effort:** Large
**Dependencies:** TASK-014, TASK-015, TASK-016
**Status:** **Done** (2026-03-15)

---

## Overview

Close the remaining application-side gaps between the implemented router and the MVP contract defined in `_docs/_MVP/`.

Business goal:
- make the MVP contract enforceable at startup and request time
- finish the health/failover behavior with real half-open recovery
- activate shared runtime state for multi-instance execution instead of local-only defaults
- turn explainable routing into a reconstructable operator signal rather than a partial event stream
- remove dead MVP configuration by turning `shared_services` into a real application-side runtime registry

---

## Security Contract

- endpoint and protocol guardrails must fail closed and must not route traffic to an incompatible deployment contract
- runtime diagnostics must never log raw secrets, API keys, or bearer tokens
- Redis-backed state must store only operational metadata needed for routing, health, and limit coordination
- shared-service registry visibility must expose only semantic config metadata already present in router configuration

---

## Sub-Tasks

### TASK-021-01: Supported deployment contracts, endpoint guards, and shared-service registry

**Status:** Done (2026-03-15)

Enforce the MVP deployment contract in config, domain, and request execution, and turn `shared_services` into a real runtime registry.

### TASK-021-02: Half-open circuit recovery and health-state transition hardening

**Status:** Done (2026-03-15)

Implement a real half-open recovery phase with a single probe request and correct state transitions after probe success or failure.

### TASK-021-03: Redis-backed runtime state activation and shared coordination

**Status:** Done (2026-03-15)

Allow the active runtime to switch from local in-memory state to Redis-backed health and limiter coordination for multi-instance deployments.

### TASK-021-04: Explainable routing rejection diagnostics and status reconciliation

**Status:** Done (2026-03-15)

Record why candidates were rejected, surface failover reasons explicitly, and align public/internal status documentation with the actual runtime behavior.

---

## Implementation Order

1. Lock down deployment contract validation and request-path guards.
2. Implement half-open health recovery and selector behavior.
3. Activate Redis-backed runtime state through settings and bootstrap wiring.
4. Expand explainability signals, update docs, and reconcile repository status pages.

---

## Testing Requirements

- config validation rejects unsupported deployment kinds and protocols
- request paths reject incompatible deployment contracts explicitly
- half-open recovery allows one probe and re-opens or closes correctly
- Redis-backed runtime wiring is covered without requiring a live Redis instance in unit tests
- explainability fields are covered by unit and local integration tests
- `PYTHONPATH=. uv run pytest tests/unit tests/integration/api -q`

---

## Documentation Updates Required

- `docs/getting-started/implementation-status.md`
- `docs/configuration/configuration-model.md`
- `docs/configuration/deployment-and-upstreams.md`
- `docs/routing/failover-and-health.md`
- `docs/reference/decision-reasons.md`
- `docs/operations/deployment-model.md`
- `_docs/_TASKS/TASK-021-mvp-closure-runtime-state-activation-and-contract-hardening.md`
- `_docs/_TASKS/TASK-021-01-supported-deployment-contracts-endpoint-guards-and-shared-service-registry.md`
- `_docs/_TASKS/TASK-021-02-half-open-circuit-recovery-and-health-state-transition-hardening.md`
- `_docs/_TASKS/TASK-021-03-redis-backed-runtime-state-activation-and-shared-coordination.md`
- `_docs/_TASKS/TASK-021-04-explainable-routing-rejection-diagnostics-and-status-reconciliation.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`

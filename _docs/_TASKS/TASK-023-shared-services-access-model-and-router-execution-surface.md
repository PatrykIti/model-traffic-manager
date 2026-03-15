[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-023: Shared Services Access Model and Router Execution Surface
# FileName: TASK-023-shared-services-access-model-and-router-execution-surface.md

**Priority:** High
**Category:** Architecture and Feature Planning
**Estimated Effort:** Large
**Dependencies:** TASK-021
**Status:** **Done** (2026-03-15)

---

## Overview

Design and implement a safe, explicit way for backend services to consume `shared_services` through or alongside the router without turning the router into a generic integration gateway.

Business goal:
- make `shared_services` useful to the future chatbot backend
- keep auth, observability, and service metadata centralized where that adds value
- avoid forcing LLM-style failover semantics onto services that already have provider-managed availability
- preserve the repository boundary: this service remains a traffic router, not a general-purpose backend platform

Key architectural direction:
- not every shared service should behave like an LLM deployment
- some services should use router-managed HTTP proxying
- some services should use a single semantic endpoint with no router failover
- some services, such as Azure Storage with provider-managed redundancy, may be better consumed directly by the backend via SDK and Managed Identity instead of being proxied through the router

---

## Security Contract

- backend-to-router shared-service access must stay explicit and controlled
- generic credential forwarding is forbidden; router outbound auth remains service-owned
- binary/object payload paths must not silently expand the router into an unbounded file gateway
- failover policy must be opt-in per shared-service class, not assumed by default

---

## Sub-Tasks

### TASK-023-01: Shared-service taxonomy, routing profiles, and failover policy split

**Status:** Done (2026-03-15)

Define which shared-service classes should support router-managed failover, which should use a single provider-managed endpoint, and which should stay direct-access from the backend.

### TASK-023-02: Configuration and domain model for shared-service execution policies

**Status:** Done (2026-03-15)

Extend the config/domain contract so shared services can declare access mode, transport shape, and routing policy explicitly.

### TASK-023-03: First backend-facing shared-service proxy path for HTTP/JSON services

**Status:** Done (2026-03-15)

Implement the first narrow shared-service execution path through the router for backend callers where router-managed auth, observability, and optional failover are valuable.

### TASK-023-04: Direct-access model for provider-managed storage and large object workloads

**Status:** Done (2026-03-15)

Document and implement the boundary where services such as Azure Storage remain backend-direct with Managed Identity instead of becoming generic router-proxied traffic.

### TASK-023-05: Validation, observability, and official documentation for shared-service execution

**Status:** Done (2026-03-15)

Implementation note:
- this planning task tree was realized by the executable implementation captured under `TASK-024*`
- the planning conclusions remain useful as the architectural rationale for the implemented shared-service execution model

Add tests, diagnostics, and official docs for the final shared-service execution model.

---

## Implementation Order

1. Lock the taxonomy and failover policy split.
2. Encode the policy in config and domain types.
3. Implement the first narrow proxy path for backend-friendly HTTP/JSON shared services.
4. Keep storage-style services direct-access unless a specific use case justifies a dedicated router path.
5. Prove the model with tests and publish the operator/developer contract.

---

## Testing Requirements

- config validation for shared-service execution policies
- unit tests for routing-policy selection per shared-service class
- local integration tests for the first shared-service proxy path
- explicit tests proving that provider-managed storage-style services do not accidentally inherit LLM failover behavior

---

## Documentation Updates Required

- `docs/configuration/configuration-model.md`
- `docs/configuration/deployment-and-upstreams.md`
- `docs/architecture/request-lifecycle.md`
- `docs/operations/deployment-model.md`
- `docs/reference/glossary.md`
- `_docs/_TASKS/TASK-023-shared-services-access-model-and-router-execution-surface.md`
- `_docs/_TASKS/TASK-023-01-shared-service-taxonomy-routing-profiles-and-failover-policy-split.md`
- `_docs/_TASKS/TASK-023-02-configuration-and-domain-model-for-shared-service-execution-policies.md`
- `_docs/_TASKS/TASK-023-03-first-backend-facing-shared-service-proxy-path-for-http-json-services.md`
- `_docs/_TASKS/TASK-023-04-direct-access-model-for-provider-managed-storage-and-large-object-workloads.md`
- `_docs/_TASKS/TASK-023-05-validation-observability-and-official-documentation-for-shared-service-execution.md`
- `_docs/_TASKS/README.md`

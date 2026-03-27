[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-005: Phase 1 Domain, Config, and Deployment Registry Bootstrap
# FileName: TASK-005-phase-1-domain-config-and-deployment-registry-bootstrap.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Large
**Dependencies:** TASK-004
**Status:** **Done** (2026-03-13)

---

## Overview

Implement the first real application behavior on top of the Phase 0 scaffold.

Business goal:
- establish the first domain model for deployments, upstreams, auth, and health-related state
- load and validate the semantic YAML configuration at startup
- expose the first useful application capability: listing deployments from validated config

Expected outcome:
- startup fails fast on invalid config
- the service has a typed deployment registry loaded from YAML
- clients can inspect the current deployment registry through the API

---

## Sub-Tasks

### TASK-005-01: Domain and configuration model foundation

**Status:** Done (2026-03-13)

Create the domain entities/value objects and the Pydantic configuration contract that maps YAML into typed runtime structures.

### TASK-005-02: YAML loader and config-backed deployment repository

**Status:** Done (2026-03-13)

Create the infrastructure layer that loads, validates, and exposes deployments through a repository contract.

### TASK-005-03: Deployment listing use case and API surface

**Status:** Done (2026-03-13)

Implement the first application use case and expose it through the HTTP API.

### TASK-005-04: Documentation, task tracking, and validation alignment

**Status:** Done (2026-03-13)

Update official docs, internal task tracking, and changelog/history after the implementation is complete.

---

## Architecture

Target additions for Phase 1:

```text
app/domain/
|-- entities/
|   |-- deployment.py
|   `-- upstream.py
|-- value_objects/
|   |-- auth_policy.py
|   `-- health_state.py
`-- errors.py

app/application/
|-- dto/
|   `-- deployment_summary.py
|-- ports/
|   `-- deployment_repository.py
`-- use_cases/
    `-- list_deployments.py

app/infrastructure/config/
|-- models.py
|-- yaml_loader.py
`-- deployment_repository.py

app/entrypoints/api/
`-- routes_deployments.py
```

---

## Implementation Order

1. Build the domain/value object layer.
2. Build the config models and validation rules.
3. Load YAML into typed config and expose a deployment repository.
4. Add the deployment listing use case and API endpoint.
5. Add tests and documentation updates.

---

## Testing Requirements

- invalid config is rejected deterministically
- domain/value object invariants are covered by unit tests
- the deployment listing use case is covered by unit tests
- API integration confirms deployments are exposed from validated config

---

## Documentation Updates Required

- `docs/architecture/system-overview.md`
- `docs/configuration/configuration-model.md`
- `docs/configuration/deployment-and-upstreams.md`
- `docs/reference/glossary.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`
- all TASK-005 work item files
- future changelog entry for TASK-005

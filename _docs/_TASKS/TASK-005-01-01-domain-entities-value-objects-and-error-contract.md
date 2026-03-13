[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-005-01-01: Domain Entities, Value Objects, and Error Contract
# FileName: TASK-005-01-01-domain-entities-value-objects-and-error-contract.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-005-01
**Status:** **Done** (2026-03-13)

---

## Overview

Define the pure domain model for Phase 1.

This work item owns:
- `Deployment`
- `Upstream`
- `AuthPolicy`
- `HealthState`
- base domain error classes needed for config loading and deployment lookup

---

## Target Files

```text
app/domain/entities/deployment.py
app/domain/entities/upstream.py
app/domain/value_objects/auth_policy.py
app/domain/value_objects/health_state.py
app/domain/errors.py
```

---

## Pseudocode

```text
Deployment:
    requires at least one upstream
    exposes provider/region summaries

Upstream:
    requires tier >= 0
    requires weight > 0

AuthPolicy:
    managed_identity -> requires scope
    api_key -> requires header_name and secret_ref
    none -> requires no external auth material
```

---

## Testing Requirements

- valid domain objects can be created
- invalid auth policy combinations raise domain errors
- invalid tier/weight/upstream combinations raise domain errors

---

## Documentation Updates Required

- `docs/reference/glossary.md`
- `_docs/_TASKS/TASK-005-01-01-domain-entities-value-objects-and-error-contract.md`

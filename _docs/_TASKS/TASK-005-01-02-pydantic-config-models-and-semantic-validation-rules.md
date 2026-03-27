[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-005-01-02: Pydantic Config Models and Semantic Validation Rules
# FileName: TASK-005-01-02-pydantic-config-models-and-semantic-validation-rules.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-005-01
**Status:** **Done** (2026-03-13)

---

## Overview

Create the typed YAML contract and enforce semantic validation before runtime startup continues.

This work item owns:
- top-level router config model
- nested deployment/upstream/auth models
- duplicate ID checks
- auth-specific validation rules

---

## Target Files

```text
app/infrastructure/config/models.py
```

---

## Validation Rules

- deployment IDs are unique
- upstream IDs are unique within a deployment
- `managed_identity` requires `scope`
- `api_key` requires `header_name` and `secret_ref`
- `tier >= 0`
- `weight > 0`
- endpoints must be valid URLs

---

## Testing Requirements

- valid example YAML structure passes validation
- duplicate deployment IDs fail
- duplicate upstream IDs fail
- missing `scope` for `managed_identity` fails
- missing API key fields fails

---

## Documentation Updates Required

- `docs/configuration/configuration-model.md`
- `docs/configuration/deployment-and-upstreams.md`
- `_docs/_TASKS/TASK-005-01-02-pydantic-config-models-and-semantic-validation-rules.md`

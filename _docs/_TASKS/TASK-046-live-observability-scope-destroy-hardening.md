[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-046: Live Observability Scope Destroy Hardening
# FileName: TASK-046-live-observability-scope-destroy-hardening.md

**Priority:** High
**Category:** Validation Reliability
**Estimated Effort:** Small
**Dependencies:** TASK-044
**Status:** **Done** (2026-03-26)

---

## Overview

Harden the `e2e-aks-live-observability` scope so temporary resource-group cleanup does not fail when Application Insights leaves nested Smart Detection resources behind.

Result:

- the AzureRM provider for this temporary scope now skips nested-resource protection during RG deletion
- the change is intentionally limited to this ephemeral validation scope

---

## Testing Requirements

- `terraform -chdir=infra/e2e-aks-live-observability validate`

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-046-live-observability-scope-destroy-hardening.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/63-2026-03-26-live-observability-scope-destroy-hardening.md`
- `_docs/_CHANGELOG/README.md`

[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-055: E2E Azure Janitor Tag Filter Fix
# FileName: TASK-055-e2e-azure-janitor-tag-filter-fix.md

**Priority:** Medium
**Category:** Workflow Reliability
**Estimated Effort:** Small
**Dependencies:** TASK-040
**Status:** **Done** (2026-03-28)

---

## Overview

Fix the Azure janitor workflow so it filters temporary resource groups correctly.

The previous implementation attempted to pass two tag filters to `az group list --tag`, but the Azure CLI only accepts a single tag filter argument there. The workflow now filters for both repository ownership and temporary-resource markers in the JMESPath query instead.

---

## Testing Requirements

- the janitor workflow remains shell- and docs-guardrail compliant
- the resource-group list command accepts the filter syntax used in the workflow

---

## Documentation Updates Required

- `.github/workflows/e2e-azure-janitor.yml`
- `_docs/_TASKS/TASK-055-e2e-azure-janitor-tag-filter-fix.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/README.md`

[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-020-01: Live-Model AKS Scope and Azure OpenAI Infrastructure
# FileName: TASK-020-01-live-model-aks-scope-and-azure-openai-infrastructure.md

**Priority:** High
**Category:** Infrastructure Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-020
**Status:** **Done** (2026-03-15)

---

## Overview

Create a dedicated AKS-backed scope that also provisions Azure OpenAI resources and grants the router identity inference access.

---

## Testing Requirements

- the new scope validates independently
- the router identity receives the required Azure OpenAI RBAC

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-020-01-live-model-aks-scope-and-azure-openai-infrastructure.md`

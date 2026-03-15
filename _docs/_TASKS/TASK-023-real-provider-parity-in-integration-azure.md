[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-023: Real Provider Parity in `integration-azure`
# FileName: TASK-023-real-provider-parity-in-integration-azure.md

**Priority:** High
**Category:** Higher-Level Validation
**Estimated Effort:** Medium
**Dependencies:** TASK-011, TASK-012, TASK-020
**Status:** **To Do**

---

## Overview

Expand `integration-azure` from identity-only proof into a faster real-provider
validation layer for chat completions and embeddings without requiring AKS.

Business goal:
- keep a cheaper Azure-backed validation path than the full AKS suites
- prove real upstream behavior for both main inference endpoints
- make auth-mode behavior explicit in the Azure-backed integration layer

## Sub-Tasks

### TASK-023-01: Chat completions live provider request path

**Status:** To Do

Add real Azure OpenAI chat validation to `integration-azure`.

### TASK-023-02: Embeddings live provider request path and auth matrix

**Status:** To Do

Add real embeddings validation and split the auth expectations explicitly.

### TASK-023-02-01: Managed Identity provider path

**Status:** To Do

Prove the real provider path using Managed Identity.

### TASK-023-02-02: API-key fallback provider path

**Status:** To Do

Add an explicit opt-in path for API-key-based provider validation.

### TASK-023-03: Cost guardrails, docs, and operator contract

**Status:** To Do

Document the faster Azure-backed live-provider path and its expected limits.

## Testing Requirements

- `integration-azure` proves real provider calls for chat completions and
  embeddings
- the auth-mode split stays explicit instead of silently mixing credentials
- cost and quota guardrails remain documented and opt-in

## Documentation Updates Required

- `docs/operations/testing-levels-and-environments.md`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-023-real-provider-parity-in-integration-azure.md`
- `_docs/_TASKS/TASK-023-01-chat-completions-live-provider-request-path.md`
- `_docs/_TASKS/TASK-023-02-embeddings-live-provider-request-path-and-auth-matrix.md`
- `_docs/_TASKS/TASK-023-02-01-managed-identity-provider-path.md`
- `_docs/_TASKS/TASK-023-02-02-api-key-fallback-provider-path.md`
- `_docs/_TASKS/TASK-023-03-cost-guardrails-docs-and-operator-contract.md`

## Security Contract

- keep Managed Identity and API-key validation paths separate in configuration
  and operator instructions
- never hide API-key requirements behind implicit environment discovery

[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-015: Basic Rate Limiting and Concurrency Limiting
# FileName: TASK-015-basic-rate-limiting-and-concurrency-limiting.md

**Priority:** High
**Category:** Core Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-013, TASK-014
**Status:** **To Do**

---

## Overview

Implement the remaining MVP limit controls at the deployment level.

Business goal:
- prevent one deployment from exceeding its configured concurrency and request-rate guardrails
- keep the limit logic small, explicit, and explainable
- preserve room for both local and Redis-backed enforcement

In scope:
- deployment-level rejection model
- concurrency guard
- request-rate limiting
- local and Redis-backed adapters

Out of scope:
- tenant-aware limits
- cost-aware or adaptive shaping
- global distributed quota planning

---

## Security Contract

- visibility: `internal`
- enforcement key: deployment-level in MVP, not end-user identity aware
- rejection behavior: explicit and observable
- secret handling: none required beyond existing router config

---

## Sub-Tasks

### TASK-015-01: Deployment-level limit contracts and rejection model

**Status:** To Do

Define the application-facing limiter behavior and error surface.

### TASK-015-02: Local and Redis-backed limiter adapters

**Status:** To Do

Implement the MVP storage and coordination layer for limits.

### TASK-015-03: Entrypoint integration, tests, and docs

**Status:** To Do

Apply the limiters to the HTTP entrypoint and prove the behavior.

---

## Implementation Order

1. Define the limiter ports and rejection model.
2. Implement local and Redis-backed adapters.
3. Integrate enforcement into the API path.
4. Add tests and update docs.

---

## Testing Requirements

- unit tests cover accepted and rejected cases for both rate and concurrency limits
- local integration tests prove HTTP rejection behavior
- Redis-backed coordination stays adapter-scoped and testable
- `pre-commit --all-files`

---

## Documentation Updates Required

- `docs/configuration/configuration-model.md`
- `docs/operations/observability-and-health.md`
- `docs/getting-started/implementation-status.md`
- `_docs/_TASKS/TASK-015-basic-rate-limiting-and-concurrency-limiting.md`
- `_docs/_TASKS/TASK-015-01-deployment-level-limit-contracts-and-rejection-model.md`
- `_docs/_TASKS/TASK-015-02-local-and-redis-backed-limiter-adapters.md`
- `_docs/_TASKS/TASK-015-03-entrypoint-integration-tests-and-docs.md`

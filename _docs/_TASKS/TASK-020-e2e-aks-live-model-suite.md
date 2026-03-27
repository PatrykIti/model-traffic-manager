[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-020: E2E AKS Live-Model Suite
# FileName: TASK-020-e2e-aks-live-model-suite.md

**Priority:** High
**Category:** Higher-Level Validation
**Estimated Effort:** Medium
**Dependencies:** TASK-019
**Status:** **Done** (2026-03-15)

---

## Overview

Add a second AKS-backed suite that provisions real Azure OpenAI infrastructure and validates a live model response through the router.

Business goal:
- keep the current `e2e-aks` command as a cheap runtime smoke path
- add a separate, opt-in live-model suite with broader infrastructure
- validate a real request path through AKS, Workload Identity, router config, and Azure OpenAI

---

## Sub-Tasks

### TASK-020-01: Live-model AKS scope and Azure OpenAI infrastructure

**Status:** Done (2026-03-15)

Provision AKS plus Azure OpenAI account, deployments, and RBAC for the router identity.

### TASK-020-02: Live-model runner and router configuration generation

**Status:** Done (2026-03-15)

Add a dedicated local runner and generate runtime router config from Terraform outputs.

### TASK-020-03: Live-model e2e test suite and operator docs

**Status:** Done (2026-03-15)

Add the test suite, Makefile command, and documentation for the new live-model path.

---

## Testing Requirements

- the current smoke suite remains unchanged
- the live-model suite provisions extra infra and validates a real model response
- cleanup still runs even when the live-model request fails

---

## Documentation Updates Required

- `docs/getting-started/local-development.md`
- `docs/operations/testing-levels-and-environments.md`
- `_docs/_INFRA/terraform-scopes-and-tfvars.md`
- `_docs/_TASKS/TASK-020-e2e-aks-live-model-suite.md`
- `_docs/_TASKS/TASK-020-01-live-model-aks-scope-and-azure-openai-infrastructure.md`
- `_docs/_TASKS/TASK-020-02-live-model-runner-and-router-configuration-generation.md`
- `_docs/_TASKS/TASK-020-03-live-model-e2e-test-suite-and-operator-docs.md`

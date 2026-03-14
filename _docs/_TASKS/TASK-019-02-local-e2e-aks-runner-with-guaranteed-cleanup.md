[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-019-02: Local `e2e-aks` Runner with Guaranteed Cleanup
# FileName: TASK-019-02-local-e2e-aks-runner-with-guaranteed-cleanup.md

**Priority:** High
**Category:** Developer Workflow
**Estimated Effort:** Medium
**Dependencies:** TASK-019
**Status:** **Done** (2026-03-14)

---

## Overview

Add a local one-command AKS runner that can provision the cluster, deploy the router, run smoke checks, and always destroy the environment afterwards.

---

## Sub-Tasks

### TASK-019-02-01: GHCR image build and AKS deploy contract

**Status:** Done (2026-03-14)

Define how the local runner builds or reuses an image and deploys it to AKS.

### TASK-019-02-02: Trap-based cleanup and diagnostics collection

**Status:** Done (2026-03-14)

Guarantee `destroy` and collect diagnostics even when the AKS-backed suite fails.

---

## Testing Requirements

- the runner provisions AKS, deploys the router, runs smoke tests, and tears everything down
- local failure still triggers cleanup and diagnostic capture

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-019-02-local-e2e-aks-runner-with-guaranteed-cleanup.md`
- `_docs/_TASKS/TASK-019-02-01-ghcr-image-build-and-aks-deploy-contract.md`
- `_docs/_TASKS/TASK-019-02-02-trap-based-cleanup-and-diagnostics-collection.md`

[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-019-02-01: GHCR Image Build and AKS Deploy Contract
# FileName: TASK-019-02-01-ghcr-image-build-and-aks-deploy-contract.md

**Priority:** High
**Category:** Developer Workflow
**Estimated Effort:** Small
**Dependencies:** TASK-019-02
**Status:** **Done** (2026-03-14)

---

## Overview

Define the local AKS runner contract around image publishing and in-cluster deployment.

---

## Testing Requirements

- the runner can build and push an image or accept a prebuilt one
- the router deployment consumes that image deterministically

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-019-02-01-ghcr-image-build-and-aks-deploy-contract.md`

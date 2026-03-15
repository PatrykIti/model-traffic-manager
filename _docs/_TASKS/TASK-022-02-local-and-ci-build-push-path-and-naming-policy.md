[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-022-02: Local and CI Build-Push Path and Naming Policy
# FileName: TASK-022-02-local-and-ci-build-push-path-and-naming-policy.md

**Priority:** High
**Category:** Workflow and Delivery
**Estimated Effort:** Medium
**Dependencies:** TASK-022
**Status:** **To Do**

---

## Overview

Define the local and CI build-push flow for ACR, including image naming,
tagging, and scope-aware isolation.

## Testing Requirements

- the local runners and CI path can push an image to ACR with stable naming
- the resulting image reference is consumable by AKS-backed suites

## Documentation Updates Required

- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-022-02-local-and-ci-build-push-path-and-naming-policy.md`

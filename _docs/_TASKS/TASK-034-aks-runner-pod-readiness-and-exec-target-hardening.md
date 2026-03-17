[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-034: AKS Runner Pod Readiness and Exec Target Hardening
# FileName: TASK-034-aks-runner-pod-readiness-and-exec-target-hardening.md

**Priority:** High
**Category:** Validation and Runner Hardening
**Estimated Effort:** Small
**Dependencies:** TASK-019, TASK-020, TASK-029, TASK-030
**Status:** **Done** (2026-03-17)

---

## Overview

Harden the Azure/AKS validation runner against startup races that can happen immediately after deployment rollout.

Business goal:
- stop false negatives where `kubectl exec deployment/router-app ...` runs before the container is actually ready for exec
- use explicit pod readiness checks before Workload Identity token validation
- execute against the resolved running router pod and container, not an abstract deployment target

---

## Sub-Tasks

- add a helper that resolves the active running router pod by label
- wait for pod readiness after deployment rollout for router and mock pods
- run identity smoke checks against `pod/<name> -c router` instead of `deployment/router-app`

---

## Testing Requirements

- `bash -n scripts/release/run_azure_test_suite.sh` stays valid
- the runner includes explicit readiness waits before `kubectl exec`

---

## Documentation Updates Required

- `scripts/release/run_azure_test_suite.sh`
- `_docs/_TASKS/TASK-034-aks-runner-pod-readiness-and-exec-target-hardening.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/39-2026-03-17-aks-runner-pod-readiness-and-exec-target-hardening.md`
- `_docs/_CHANGELOG/README.md`

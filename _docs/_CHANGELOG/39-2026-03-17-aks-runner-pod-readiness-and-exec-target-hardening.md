[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 39: AKS Runner Pod Readiness and Exec Target Hardening

**Date:** 2026-03-17
**Version:** 0.1.0
**Tasks:**
- TASK-034

---

## Key Changes

### Runner startup synchronization

- added explicit pod readiness waits after deployment rollout in the Azure/AKS test runner
- hardened both router and mock deployment startup checks before follow-up validation steps

### Exec target selection

- switched Workload Identity smoke checks from `deployment/router-app` to the resolved running router pod and `router` container
- removed a race where rollout completion could still be followed by `container not found` on immediate `kubectl exec`

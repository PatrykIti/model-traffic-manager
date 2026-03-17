[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 34: Live Chat Failover Mock Image Pull Fix

**Date:** 2026-03-17
**Version:** 0.1.0
**Tasks:**
- TASK-029-04

---

## Key Changes

### AKS failover helper fix

- updated the failover mock deployment to use the same `router-app` service account as the main router pod
- ensured the mock helper inherits the patched image-pull secret when GHCR images are used
- fixed the `ImagePullBackOff` failure that blocked the live chat failover suite before the test logic could run

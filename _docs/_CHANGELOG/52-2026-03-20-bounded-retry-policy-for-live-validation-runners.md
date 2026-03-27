[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 52: Bounded Retry Policy for Live Validation Runners

**Date:** 2026-03-20
**Version:** 0.1.0
**Tasks:**
- TASK-040-04
- TASK-040-04-01
- TASK-040-04-02
- TASK-040-04-03

---

## Key Changes

### Retry Policy

- added a central retry-policy matcher for transient runner-side failures
- classified retry policies for Azure control-plane, GHCR auth/build, Terraform apply/destroy, Kubernetes watches, and port-forward startup

### Runner Integration

- added bounded retries with explicit backoff to the shared Azure/AKS runner
- hardened transient operations such as GHCR auth, image build/push, Terraform apply, AKS credential acquisition, rollout waits, and port-forward startup

### Validation

- added unit coverage for retry-policy matching
- validated the updated runner and documented the new bounded retry behavior

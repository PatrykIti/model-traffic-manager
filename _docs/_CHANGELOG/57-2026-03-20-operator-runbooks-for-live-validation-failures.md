[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 57: Operator Runbooks for Live Validation Failures

**Date:** 2026-03-20
**Version:** 0.1.0
**Tasks:**
- TASK-040-08
- TASK-040-08-01
- TASK-040-08-02
- TASK-040-08-03

---

## Key Changes

### Runbook Set

- added an operations runbook index and focused runbooks for Azure OpenAI permission failures, GHCR/image-pull failures, AKS rollout and port-forward failures, quota placement issues, and storage/cleanup failures

### Documentation Integration

- linked the runbook set from operations/testing docs
- aligned the runbooks with real failure signatures already observed in the live validation matrix

[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 32: E2E AKS Live Embeddings Profile

**Date:** 2026-03-16
**Version:** 0.1.0
**Tasks:**
- TASK-029-03

---

## Key Changes

### Live validation profile

- added a dedicated `e2e-aks-live-embeddings` Terraform scope
- added a dedicated router-config renderer for live embeddings validation
- added a dedicated AKS end-to-end embeddings suite and local `make` target

### Workflow and operator surface

- extended the local runner to support the new live embeddings suite
- added the required environment markers and outputs-path contract
- updated official docs so the new profile is discoverable next to the existing live chat suite

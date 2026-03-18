[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 45: Live Shared-Services Validation on Azure and AKS

**Date:** 2026-03-18
**Version:** 0.1.0
**Tasks:**
- TASK-029-05
- TASK-029-05-01
- TASK-029-05-02
- TASK-029-05-03

---

## Key Changes

### Live Shared-Services Profile

- added a dedicated `e2e-aks-live-shared-services` scope and suite
- provisioned a real Azure Storage account endpoint for the direct-backend-access shared-service contract
- added in-cluster mock downstreams for `router_proxy + single_endpoint` and `router_proxy + tiered_failover`

### Runner and Test Surface

- added `make e2e-aks-live-shared-services-local`
- extended the shared Azure/AKS runner to render and execute the dedicated shared-services profile
- added a live suite that validates registry exposure, fail-closed direct access, single-endpoint execution, and tiered failover behavior

### Documentation

- documented the new profile in testing-level and local-development docs
- updated implementation status to include live shared-services validation

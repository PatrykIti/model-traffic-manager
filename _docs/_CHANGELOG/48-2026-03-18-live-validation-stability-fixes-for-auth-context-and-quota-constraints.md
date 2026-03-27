[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 48: Live Validation Stability Fixes for Auth, Context, and Quota Constraints

**Date:** 2026-03-18
**Version:** 0.1.0
**Tasks:**
- TASK-039

---

## Key Changes

### Auth and Role Assignment

- granted Azure OpenAI user access to the current executing principal for the split integration-azure provider-probe profiles
- preserved the existing user-assigned identity role assignments while allowing local and workflow execution identities to call the live Azure OpenAI APIs

### Runner Isolation

- switched the AKS runner to an isolated temporary kubeconfig per run
- reduced cross-suite context stomping when multiple AKS profiles are executed close together

### Quota and Fixture Hardening

- moved AKS validation profile defaults away from the constrained B-series family to a D-series size aligned with the broader infrastructure
- adjusted the live shared-services storage fixture so the storage module can provision and tear down cleanly

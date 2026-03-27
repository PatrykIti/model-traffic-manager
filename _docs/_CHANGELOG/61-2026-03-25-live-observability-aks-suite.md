[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 61: Live Observability AKS Suite

**Date:** 2026-03-25
**Version:** 0.1.0
**Tasks:**
- TASK-044
- TASK-044-01
- TASK-044-02
- TASK-044-03
- TASK-044-04

---

## Key Changes

### New AKS Live Observability Scope

- added `infra/e2e-aks-live-observability/` as a dedicated live AKS scope for Azure Monitor request-flow validation
- used the user's Terraform modules for Log Analytics Workspace and Application Insights alongside the existing AKS, UAI, Cognitive Account, and role-assignment modules
- validated the new Terraform scope successfully after module initialization

### Runtime Delivery and Runner Wiring

- added a dedicated observability router config renderer with explicit `consumer_role` values
- extended the shared Azure/AKS runner to fetch the Application Insights connection string at runtime and deliver it to the router pod through a Kubernetes secret
- registered `e2e-aks-live-observability` in the suite registry and added a local make target

### Live Assertions and Documentation

- added `tests/e2e_aks_live_observability/` with live checks for Application Insights request-flow visibility, final-upstream attribution, and `consumer_role`
- added startup-log validation for the structured topology snapshot
- updated local-development, testing-levels, observability, and runbook documentation for the new suite

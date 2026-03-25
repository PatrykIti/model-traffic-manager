[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 59: Azure Monitor Request-Flow Observability

**Date:** 2026-03-25
**Version:** 0.1.0
**Tasks:**
- TASK-042
- TASK-042-01
- TASK-042-02
- TASK-042-03
- TASK-042-04

---

## Key Changes

### Azure Monitor Runtime Export

- added an opt-in Azure Monitor / Application Insights backend for the router observability path
- aligned the OpenTelemetry dependency set with the Azure Monitor Python compatibility window and refreshed `uv.lock`
- extended runtime settings and `.env.example` with explicit Azure Monitor exporter controls, sampling, and log-export toggles

### Request-Flow Telemetry

- enriched runtime events and request spans with final-upstream attribution fields including provider, account, region, model metadata, auth mode, and optional `capacity_mode`
- added final-upstream span attributes so operators can query which upstream served a request without reconstructing the answer from raw pod logs
- preserved existing router-owned selection and failover instrumentation instead of switching to opaque automatic instrumentation

### Startup Diagnostics and Docs

- added a structured startup topology snapshot per pod plus a lightweight startup trace for boot visibility
- updated official docs and added an Application Insights request-flow triage runbook for PTU versus PAYG style investigations
- added unit and integration coverage for settings validation, runtime event enrichment, startup snapshots, and startup wiring

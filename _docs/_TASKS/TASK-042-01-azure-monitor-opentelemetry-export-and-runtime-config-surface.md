[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-042](./TASK-042-azure-monitor-application-insights-request-flow-telemetry-and-pod-diagnostics.md)

# TASK-042-01: Azure Monitor OpenTelemetry Export and Runtime Config Surface
# FileName: TASK-042-01-azure-monitor-opentelemetry-export-and-runtime-config-surface.md

**Priority:** High
**Category:** Observability Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-042
**Status:** **Done** (2026-03-25)

---

## Overview

Add an explicit Azure Monitor / Application Insights export path that fits the router's current manual instrumentation model.

Detailed work:
1. Add the exact-pinned Azure Monitor OpenTelemetry package set required for trace export and any optional log export.
2. Extend the runtime settings model with explicit observability controls such as backend mode, connection-string source, service version, and log-export enablement.
3. Initialize resource attributes consistently at startup so Application Insights can group traces by service identity and environment.
4. Preserve the current stdout-only and Prometheus-first baseline when Azure Monitor is not configured.
5. Fail safely when exporter configuration is absent or invalid so local bootstrap remains zero-dependency.

Implementation note:
- prefer exporter wiring that preserves the repository's explicit instrumentation and avoids duplicate spans
- keep trace export as the required signal when Azure Monitor mode is enabled
- treat Azure-backed log export as optional behind a feature flag if exporter maturity or data volume makes it risky

---

## Risks

- duplicate or conflicting instrumentation if exporter bootstrap is layered carelessly on top of existing tracing
- startup regressions if the zero-dependency path starts requiring Azure-specific environment variables
- noisy or unstable production behavior if logs are mirrored to Azure Monitor without clear filtering rules

---

## Testing Requirements

- settings validation covers both disabled and enabled Azure Monitor modes
- startup wiring remains functional with and without a connection string
- exporter bootstrap is unit-tested with stubs so no live Azure dependency is required

---

## Documentation Updates Required

- `docs/operations/observability-and-health.md`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-042-01-azure-monitor-opentelemetry-export-and-runtime-config-surface.md`

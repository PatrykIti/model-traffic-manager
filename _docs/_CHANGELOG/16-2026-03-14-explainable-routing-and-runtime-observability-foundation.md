[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 16-2026-03-14-explainable-routing-and-runtime-observability-foundation.md

# 16. Explainable Routing and Runtime Observability Foundation

**Date:** 2026-03-14
**Version:** 0.1.0
**Tasks:** TASK-016-01, TASK-016-01-01, TASK-016-01-02, TASK-016-02

## Key Changes

### Decision events and request correlation
- Added request correlation through `x-request-id` and request-scoped middleware state.
- Added structured runtime events for route selection, health-state updates, limiter rejections, and request completion.
- Wired runtime event recording into routing and limiting flows without leaking secrets or payload content.

### Metrics and traces
- Added a Prometheus `/metrics` endpoint and runtime counters/histograms for route attempts, limiter rejections, health-state updates, and request duration.
- Added trace foundations for inbound requests and outbound model attempts.
- Expanded startup wiring so observability components are available through the bootstrap container.

### Documentation
- Updated official docs to reflect runtime decision events, request correlation, and the current observability surface.
- Left `TASK-016` itself in progress because Azure-backed activation and release hardening remain ahead.

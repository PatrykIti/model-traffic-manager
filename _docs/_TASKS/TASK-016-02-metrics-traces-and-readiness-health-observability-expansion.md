[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-016-02: Metrics, Traces, and Readiness/Health Observability Expansion
# FileName: TASK-016-02-metrics-traces-and-readiness-health-observability-expansion.md

**Priority:** High
**Category:** Observability Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-016
**Status:** **To Do**

---

## Overview

Add the metrics and traces that make the router operationally visible.

Detailed work:
1. Emit Prometheus metrics for route attempts, upstream outcomes, limiter rejections, and breaker changes.
2. Add OpenTelemetry traces around inbound request handling and outbound attempts.
3. Extend readiness and health signaling with richer operational detail where appropriate.

---

## Testing Requirements

- metric events are emitted on the core success and failure paths
- traces preserve request and attempt correlation without logging secrets
- readiness behavior stays aligned with actual dependency expectations

---

## Documentation Updates Required

- `docs/operations/observability-and-health.md`
- `_docs/_TASKS/TASK-016-02-metrics-traces-and-readiness-health-observability-expansion.md`

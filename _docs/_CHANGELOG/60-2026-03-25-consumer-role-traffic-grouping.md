[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 60: Consumer Role Traffic Grouping

**Date:** 2026-03-25
**Version:** 0.1.0
**Tasks:**
- TASK-043
- TASK-043-01
- TASK-043-02
- TASK-043-03

---

## Key Changes

### Config and Registry Contract

- added optional `consumer_role` metadata to deployment and shared-service configs
- carried the field into domain entities, API summaries, and the example router configs
- documented recommended low-cardinality values such as backend or worker profile names

### Request-Flow Telemetry

- added `consumer_role` to runtime events, request-flow trace attributes, and limiter rejection diagnostics
- included the field in the startup topology snapshot so pod-local inspection reflects the active role mapping
- kept the field off Prometheus metric labels to avoid unnecessary cardinality growth

### Tests and Documentation

- updated unit and integration coverage for config validation, registry endpoints, request-flow events, limiter rejections, and startup diagnostics
- updated official docs and Application Insights triage guidance so operators can filter by consuming backend profile

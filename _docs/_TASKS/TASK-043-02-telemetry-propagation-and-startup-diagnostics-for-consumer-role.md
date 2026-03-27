[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-043](./TASK-043-consumer-role-metadata-for-routed-traffic.md)

# TASK-043-02: Telemetry Propagation and Startup Diagnostics for Consumer Role
# FileName: TASK-043-02-telemetry-propagation-and-startup-diagnostics-for-consumer-role.md

**Priority:** High
**Category:** Observability Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-043, TASK-042
**Status:** **Done** (2026-03-25)

---

## Overview

Propagate `consumer_role` through the router-owned observability path so request-flow telemetry can be filtered by consuming service profile.

Detailed work:
1. Add `consumer_role` to runtime events and request-flow trace attributes.
2. Include it in limiter rejections and other request-path diagnostics that do not yet have upstream context.
3. Add it to the startup topology snapshot so pod-local inspection shows the active role mapping.

---

## Testing Requirements

- request-flow tests cover `consumer_role` on successful and degraded paths
- startup snapshot tests prove the field is emitted when configured

---

## Documentation Updates Required

- `docs/architecture/request-lifecycle.md`
- `docs/operations/observability-and-health.md`
- `docs/reference/decision-reasons.md`
- `_docs/_TASKS/TASK-043-02-telemetry-propagation-and-startup-diagnostics-for-consumer-role.md`

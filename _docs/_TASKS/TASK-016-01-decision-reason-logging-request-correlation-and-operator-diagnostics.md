[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-016-01: Decision Reason Logging, Request Correlation, and Operator Diagnostics
# FileName: TASK-016-01-decision-reason-logging-request-correlation-and-operator-diagnostics.md

**Priority:** High
**Category:** Observability Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-016
**Status:** **Done** (2026-03-14)

---

## Overview

Add the decision-level logging and correlation data needed to explain router behavior.

---

## Sub-Tasks

### TASK-016-01-01: Structured event schema for selection, failover, limiter, and breaker updates

**Status:** Done (2026-03-14)

Define the event payloads emitted by the router for core control-path decisions.

### TASK-016-01-02: Reference documentation and troubleshooting views

**Status:** Done (2026-03-14)

Explain how operators should read the emitted decision data during incident response.

---

## Testing Requirements

- emitted events are structured, consistent, and scrubbed of sensitive values
- correlation metadata links request attempts across selection and failover transitions
- operator-facing reference docs stay aligned with the emitted event schema

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-016-01-decision-reason-logging-request-correlation-and-operator-diagnostics.md`
- `_docs/_TASKS/TASK-016-01-01-structured-event-schema-for-selection-failover-limiter-and-breaker-updates.md`
- `_docs/_TASKS/TASK-016-01-02-reference-documentation-and-troubleshooting-views.md`

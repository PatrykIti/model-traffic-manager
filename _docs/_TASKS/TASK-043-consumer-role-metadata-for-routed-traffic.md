[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-043: Consumer Role Metadata for Routed Traffic
# FileName: TASK-043-consumer-role-metadata-for-routed-traffic.md

**Priority:** High
**Category:** Traffic Observability
**Estimated Effort:** Medium
**Dependencies:** TASK-042
**Status:** **Done** (2026-03-25)

---

## Overview

Add one operator-owned `consumer_role` field to deployment and shared-service configs so routed traffic can be grouped by the consuming backend or service profile instead of relying only on deployment IDs and upstream metadata.

Business goals:
- let operators filter request-flow telemetry by the backend or service profile that owns a routing configuration
- make it easier to compare response time and failure behavior across the same upstream fleet when several external services use different router profiles
- keep the field semantic and low-cardinality enough for logs, traces, and operator-facing summaries

Recommended usage:
- prefer stable values such as `bot-system-be`, `chatbot-api`, or `document-worker`
- avoid personal email addresses or other high-cardinality identifiers

Non-goals:
- do not turn `consumer_role` into an RBAC or identity primitive
- do not add it as a default label on every Prometheus metric if that would create avoidable cardinality growth

---

## Security Contract

- `consumer_role` must stay operator-defined metadata and must not contain secrets, tokens, or auth material
- documentation should explicitly discourage personal identifiers and high-cardinality values
- request payloads remain out of scope; this task is about configuration-owned routing metadata only

---

## Sub-Tasks

### TASK-043-01: Config and domain contract for consumer role metadata

**Status:** Done (2026-03-25)

Add the optional `consumer_role` field to deployment and shared-service configuration plus the corresponding domain entities and summaries.

### TASK-043-02: Telemetry propagation and startup diagnostics for consumer role

**Status:** Done (2026-03-25)

Emit `consumer_role` through runtime events, request-flow traces, limiter rejections, and startup topology snapshots.

### TASK-043-03: Tests, docs, and operator guidance for consumer role usage

**Status:** Done (2026-03-25)

Close the feature with proof, official docs, and task/changelog reconciliation.

---

## Implementation Order

1. Add the `consumer_role` field to config, domain, and API summary surfaces.
2. Propagate the field through runtime telemetry and startup diagnostics.
3. Update tests, docs, task tracking, and changelog entries.

---

## Testing Requirements

- config validation covers the optional `consumer_role` field for deployments and shared services
- runtime events and startup snapshots include `consumer_role` when configured
- API summaries remain stable and backward-compatible apart from the new field

---

## Documentation Updates Required

- `docs/configuration/deployment-and-upstreams.md`
- `docs/architecture/request-lifecycle.md`
- `docs/operations/observability-and-health.md`
- `docs/reference/decision-reasons.md`
- `docs/getting-started/implementation-status.md`
- `configs/example.router.yaml`
- `configs/full-capabilities.router.yaml`
- `_docs/_TASKS/TASK-043-consumer-role-metadata-for-routed-traffic.md`
- `_docs/_TASKS/TASK-043-01-config-and-domain-contract-for-consumer-role-metadata.md`
- `_docs/_TASKS/TASK-043-02-telemetry-propagation-and-startup-diagnostics-for-consumer-role.md`
- `_docs/_TASKS/TASK-043-03-tests-docs-and-operator-guidance-for-consumer-role-usage.md`
- `_docs/_TASKS/README.md`

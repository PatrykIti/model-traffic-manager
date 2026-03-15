[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-023](./TASK-023-shared-services-access-model-and-router-execution-surface.md)

# TASK-023-02: Configuration and Domain Model for Shared-Service Execution Policies
# FileName: TASK-023-02-configuration-and-domain-model-for-shared-service-execution-policies.md

**Priority:** High
**Category:** Domain and Configuration Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-023, TASK-023-01
**Status:** **Done** (2026-03-15)

---

## Overview

Extend `shared_services` so each service explicitly describes:
- service kind
- transport contract
- execution mode
- routing/failover policy
- auth policy

Suggested direction:
- keep `shared_services` separate from `deployments`
- do not overload LLM-specific terms like `kind=llm` or `protocol=openai_chat`
- allow one or more upstreams only where the execution profile genuinely needs them
- make policy validation reject impossible combinations such as `provider_managed` plus router-side tiered failover

Potential fields:
- `service_type`
- `transport`
- `execution_mode`
- `routing`
- `upstreams` or `endpoint`, depending on the chosen profile

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-023-02-configuration-and-domain-model-for-shared-service-execution-policies.md`

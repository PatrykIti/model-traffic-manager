[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-023](./TASK-023-shared-services-access-model-and-router-execution-surface.md)

# TASK-023-04: Direct-Access Model for Provider-Managed Storage and Large Object Workloads
# FileName: TASK-023-04-direct-access-model-for-provider-managed-storage-and-large-object-workloads.md

**Priority:** High
**Category:** Architecture and Operations Planning
**Estimated Effort:** Medium
**Dependencies:** TASK-023, TASK-023-01
**Status:** **To Do**

---

## Overview

Document and encode the rule that not every shared service should be proxied through the router.

Primary use case:
- backend writes voice-conversation artifacts, transcripts, or recordings to Azure Storage

Recommended default:
- backend uses Azure SDK plus Managed Identity directly against the storage account
- router may expose service metadata and policy registry, but does not become a generic blob ingress/egress gateway by default

Reasoning:
- storage accounts with RA-GRS or equivalent provider-managed availability should not require router-managed tier failover
- large object upload/download, range requests, and blob semantics would push the router toward a generic data-plane gateway
- this is operationally and architecturally different from LLM traffic routing

Optional future direction:
- if a concrete product need appears, add dedicated router-owned storage endpoints for narrowly defined operations instead of a generic catch-all proxy

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-023-04-direct-access-model-for-provider-managed-storage-and-large-object-workloads.md`

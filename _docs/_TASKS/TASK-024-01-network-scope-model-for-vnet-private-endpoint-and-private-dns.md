[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-024-01: Network Scope Model for VNet, Private Endpoint, and Private DNS
# FileName: TASK-024-01-network-scope-model-for-vnet-private-endpoint-and-private-dns.md

**Priority:** High
**Category:** Infrastructure and Networking
**Estimated Effort:** Medium
**Dependencies:** TASK-024
**Status:** **To Do**

---

## Overview

Define the Terraform scope shape required to provision the VNet, the Azure
OpenAI Private Endpoint, and the Private DNS integration needed by the live
suite.

## Sub-Tasks

### TASK-024-01-01: Public-network-disable and name-resolution invariants

**Status:** To Do

Define the security and DNS invariants for the private path.

## Testing Requirements

- the scope shape stays explicit and test-oriented rather than turning into a
  generic network platform wrapper
- DNS integration is represented clearly enough to troubleshoot from AKS

## Documentation Updates Required

- `_docs/_TASKS/TASK-024-01-network-scope-model-for-vnet-private-endpoint-and-private-dns.md`
- `_docs/_TASKS/TASK-024-01-01-public-network-disable-and-name-resolution-invariants.md`

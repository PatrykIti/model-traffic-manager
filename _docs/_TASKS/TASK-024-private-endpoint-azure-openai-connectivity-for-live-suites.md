[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-024: Private-Endpoint Azure OpenAI Connectivity for Live Suites
# FileName: TASK-024-private-endpoint-azure-openai-connectivity-for-live-suites.md

**Priority:** High
**Category:** Networking and Security
**Estimated Effort:** Large
**Dependencies:** TASK-020, TASK-021
**Status:** **To Do**

---

## Overview

Add a private-network validation path for Azure OpenAI so the repository can
prove router connectivity over Private Endpoint and Private DNS instead of only
over public access.

Business goal:
- validate the router against a more production-like private connectivity model
- prove DNS resolution and private routing from AKS to Azure OpenAI
- keep the public-path live suite as the cheaper baseline while adding a
  hardened option

## Sub-Tasks

### TASK-024-01: Network scope model for VNet, Private Endpoint, and Private DNS

**Status:** To Do

Define the infrastructure contract for private connectivity.

### TASK-024-01-01: Public-network-disable and name-resolution invariants

**Status:** To Do

Define the invariants that must hold once the private path is enabled.

### TASK-024-02: AKS live-suite private-path deployment and validation

**Status:** To Do

Run the live suite through the private path from AKS to Azure OpenAI.

### TASK-024-03: Docs and troubleshooting runbook

**Status:** To Do

Document the private path and the expected operator diagnostics.

## Testing Requirements

- Azure OpenAI can be reached from AKS through Private Endpoint and Private DNS
- the suite proves name resolution, auth, and a real model response on the
  private path
- operator diagnostics clearly distinguish public-path vs private-path failures

## Documentation Updates Required

- `docs/operations/aks-configuration-delivery.md`
- `docs/operations/testing-levels-and-environments.md`
- `_docs/_INFRA/terraform-scopes-and-tfvars.md`
- `_docs/_TASKS/TASK-024-private-endpoint-azure-openai-connectivity-for-live-suites.md`
- `_docs/_TASKS/TASK-024-01-network-scope-model-for-vnet-private-endpoint-and-private-dns.md`
- `_docs/_TASKS/TASK-024-01-01-public-network-disable-and-name-resolution-invariants.md`
- `_docs/_TASKS/TASK-024-02-aks-live-suite-private-path-deployment-and-validation.md`
- `_docs/_TASKS/TASK-024-03-docs-and-troubleshooting-runbook.md`

## Security Contract

- private connectivity must not silently fall back to public access
- once public access is disabled, docs and diagnostics must make that invariant
  explicit

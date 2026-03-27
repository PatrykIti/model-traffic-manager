[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-008-04-01: Minimal Resources for `integration-azure`
# FileName: TASK-008-04-01-minimal-resources-for-integration-azure.md

**Priority:** High
**Category:** Testing Infrastructure Planning
**Estimated Effort:** Small
**Dependencies:** TASK-008-04
**Status:** **Done** (2026-03-13)

---

## Overview

Define the smallest Azure resource set for cloud-backed integration without AKS.

---

## Minimal Resource Set

- resource group
- user-assigned managed identity
- Azure OpenAI / Azure AI Foundry resource with one test deployment
- optional Key Vault if the feature under test needs secret retrieval

Add later only if needed:

- Redis
- storage account
- other Azure-native dependencies

---

## Recommendation

This is the preferred first cloud-backed layer because it gives real Azure confidence at much lower cost than AKS.

---

## Documentation Updates Required

- `_docs/_TASKS/TASK-008-04-01-minimal-resources-for-integration-azure.md`

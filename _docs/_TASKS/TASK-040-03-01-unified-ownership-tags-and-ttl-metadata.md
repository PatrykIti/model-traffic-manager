[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md) | [TASK-040-03](./TASK-040-03-resource-lifecycle-ttl-and-cleanup-hardening.md)

# TASK-040-03-01: Unified Ownership Tags and TTL Metadata
# FileName: TASK-040-03-01-unified-ownership-tags-and-ttl-metadata.md

**Priority:** High
**Category:** Infrastructure Implementation
**Estimated Effort:** Medium
**Dependencies:** TASK-040-03
**Status:** **Done** (2026-03-20)

---

## Overview

Bring the Azure-backed scopes to one consistent ownership and TTL tag contract.

## Documentation Updates Required

- `infra/*/locals.tf`
- `.github/workflows/e2e-azure-janitor.yml`

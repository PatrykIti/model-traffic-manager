[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 8-2026-03-13-cost-aware-azure-test-infrastructure-orchestration-model.md

# 8. Cost-Aware Azure Test Infrastructure Orchestration Model

**Date:** 2026-03-13
**Version:** 0.1.0
**Tasks:** TASK-008, TASK-008-01, TASK-008-01-01, TASK-008-01-02, TASK-008-02, TASK-008-02-01, TASK-008-02-02, TASK-008-03, TASK-008-03-01, TASK-008-03-02, TASK-008-04, TASK-008-04-01, TASK-008-04-02

## Key Changes

### Strategy
- Defined the repository approach for temporary Azure infrastructure used by higher-level tests.
- Chose GitHub Actions plus a repo-local Terraform wrapper over Azure DevOps webhook chaining as the primary orchestration model.

### Cost controls
- Explicitly rejected a long-lived AKS cluster as the default strategy for a private owner.
- Defined trigger restrictions, TTL tagging, janitor cleanup, and minimal-footprint rules.

### Test environment mapping
- Defined separate Azure footprints for `integration-azure` and fully ephemeral `e2e-aks`.
- Clarified that AKS-backed tests should be opt-in, manual, scheduled, or release-oriented rather than default-per-PR.

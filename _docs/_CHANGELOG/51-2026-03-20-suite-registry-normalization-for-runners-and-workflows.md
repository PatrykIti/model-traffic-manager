[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 51: Suite Registry Normalization for Runners and Workflows

**Date:** 2026-03-20
**Version:** 0.1.0
**Tasks:**
- TASK-040-07
- TASK-040-07-01
- TASK-040-07-02

---

## Key Changes

### Canonical Registry

- added a canonical validation suite registry under `scripts/release/validation_suite_registry.py`
- moved suite metadata for scope, tests, rendering, mock behavior, and activation envs into one source of truth

### Runner and Workflow Alignment

- updated the shared Azure/AKS runner to consume suite metadata from the registry
- updated `Makefile` and GitHub workflows to align with the registry-driven suite contract

### Documentation

- documented the suite registry as the canonical operator-facing source of truth for the validation matrix

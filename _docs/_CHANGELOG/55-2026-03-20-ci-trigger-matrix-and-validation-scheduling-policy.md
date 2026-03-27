[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 55: CI Trigger Matrix and Validation Scheduling Policy

**Date:** 2026-03-20
**Version:** 0.1.0
**Tasks:**
- TASK-040-06
- TASK-040-06-01
- TASK-040-06-02
- TASK-040-06-03

---

## Key Changes

### Trigger Policy

- encoded nightly and release eligibility in the canonical suite registry
- kept PR validation limited to the existing quality workflow
- preserved manual per-suite dispatch through suite inputs

### Workflows

- added a curated nightly validation workflow
- added a release-validation workflow for the full release-enabled suite matrix

### Documentation

- documented the final trigger matrix across PR, manual, nightly, and release paths

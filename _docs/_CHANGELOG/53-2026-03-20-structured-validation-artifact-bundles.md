[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 53: Structured Validation Artifact Bundles

**Date:** 2026-03-20
**Version:** 0.1.0
**Tasks:**
- TASK-040-02
- TASK-040-02-01
- TASK-040-02-02
- TASK-040-02-03

---

## Key Changes

### Artifact Contract

- added a stable artifact directory contract for Azure-backed and AKS-backed validation runs
- added a manifest generator that records suite metadata, exit status, cleanup status, and emitted files

### Runner and Workflow Integration

- updated the shared runner to persist Terraform outputs, rendered configs, kubectl diagnostics, pod logs, and port-forward logs in standardized artifact bundles
- updated GitHub workflows to upload the standardized artifact root instead of relying on ad hoc file lists

### Documentation

- documented the standardized validation artifact bundle and its location in local and workflow runs

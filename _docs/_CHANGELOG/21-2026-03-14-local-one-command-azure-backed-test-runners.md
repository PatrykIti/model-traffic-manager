[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 21-2026-03-14-local-one-command-azure-backed-test-runners.md

# 21. Local One-Command Azure-Backed Test Runners

**Date:** 2026-03-14
**Version:** 0.1.0
**Tasks:** TASK-019, TASK-019-01, TASK-019-01-01, TASK-019-01-02, TASK-019-02, TASK-019-02-01, TASK-019-02-02, TASK-019-03

## Key Changes

### Local runners
- Added one-command local runners for `integration-azure` and `e2e-aks`.
- The runners resolve Terraform subscription input from the active Azure CLI context.
- Both runners follow `apply -> test -> destroy` and always attempt cleanup under shell traps.

### AKS local orchestration
- Added local AKS image build/push and deployment orchestration for the e2e path.
- Added federated credential setup, namespace/config creation, rollout checks, and smoke execution.
- Added trap-based cleanup for Terraform resources, federated credentials, port-forward processes, and temporary directories.

### Documentation
- Added Makefile targets and documented the local operator contract for higher-level runs.
- Updated testing documentation to explain the shared tfvars baseline and cleanup guarantees.

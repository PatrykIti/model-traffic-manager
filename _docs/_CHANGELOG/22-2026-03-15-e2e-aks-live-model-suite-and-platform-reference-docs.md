[Repository README](../../README.md) | [Internal docs](../README.md) | [Changelog](./README.md)

# 22. E2E AKS live-model suite and platform reference docs

- **Date:** 2026-03-15
- **Version:** Unreleased
- **Tasks:**
  - `TASK-020`
  - `TASK-020-01`
  - `TASK-020-02`
  - `TASK-020-03`

## Key Changes

### Live-model AKS validation

- Added a dedicated `e2e-aks-live-model` infrastructure scope that provisions AKS, a temporary Azure OpenAI account, model deployments, and Azure RBAC for the router identity.
- Added a dedicated local command path, `make e2e-aks-live-model-local`, that performs `apply -> deploy -> live model validation -> destroy`.
- Validated the full runtime path with a real response through AKS, Workload Identity, router configuration generated from Terraform outputs, and Azure OpenAI.
- Kept guaranteed cleanup under shell traps so `terraform destroy` still runs after validation failures.

### Model-profile alignment

- Aligned the live-model suite with the currently working `swedencentral` profile using `gpt-5` and `gpt-5.1`.
- Hardened the live-model pytest contract for GPT-5-family responses by using the current completion parameter contract and a more robust visible-content assertion.

### Documentation and operator guidance

- Documented the separate live-model suite in the official testing and local-development docs.
- Added the internal reference document `CHATBOT_PLATFORM.md` in English and linked it from the repository and internal documentation indexes.
- Clarified that the platform reference is informational context for the expected chatbot-layer architecture above the router rather than scope for this repository itself.

[Repository README](../README.md) | [Internal docs](../_docs/README.md)

# Infrastructure Scopes

This directory contains the repository-owned Terraform roots used for higher-level validation and infrastructure-backed workflows.

Current scope layout:

- `_shared/` for the non-secret environment baseline reused by multiple test scopes
- `integration-azure/` for lower-cost Azure-backed validation without AKS
- `e2e-aks/` for fully ephemeral AKS-backed validation
- `e2e-aks-live-model/` for AKS validation with a real Azure OpenAI request path

Scope and `tfvars` rules are documented in [_docs/_INFRA/terraform-scopes-and-tfvars.md](../_docs/_INFRA/terraform-scopes-and-tfvars.md).

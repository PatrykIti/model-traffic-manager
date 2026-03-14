[Repository README](../../README.md) | [Internal docs](../README.md) | [_INFRA](./README.md)

# Terraform Scopes and Tfvars Model

## Purpose

This repository uses a scope-first Terraform layout inspired by `genai-infrastructure`, but in a much smaller form.

We copy the operating model, not the full platform volume.

Module rule:

- prefer existing shared Terraform modules when this repository already has them
- use raw `resource` blocks only where there is no suitable module yet

## Core Rule

Each Terraform root should represent one infrastructure concern or validation class.

For this repository that means:

- `infra/integration-azure/` for Azure-backed validation without AKS
- `infra/e2e-aks/` for ephemeral AKS-backed runtime validation

Do not collapse both concerns into one shared root just because some resources overlap.

## Why Scope-First

This model keeps:

- ownership explicit
- `tfvars` easier to reason about
- workflow wiring simpler
- future edits safer when one scope changes and another should not

## Directory Contract

Each active scope should expose:

- `main.tf`
- `variables.tf`
- `providers.tf`
- `outputs.tf`
- optional `locals.tf`
- `env/`
- optional scope-local helpers such as `k8s/` or `imports/`

## Module-First Rule

Inside scope roots:

- use your existing Terraform modules for resources such as AKS or user-assigned identities when available
- keep the scope root thin and orchestration-focused
- keep raw `resource` blocks only for small glue resources that do not have an existing shared module yet, such as the test resource group

## Tfvars Contract

This repository uses one shared non-secret environment baseline plus optional scope-specific overrides.

Current convention:

- `infra/_shared/env/dev1.tfvars`
- `infra/_shared/env/prd1.tfvars`
- optional scope-local `env/dev1.tfvars` or `env/prd1.tfvars` only when a scope truly needs extra knobs

Sensitive values must not be committed to `tfvars`. Secrets and tenant-specific IDs still come from workflow inputs or GitHub/Azure secret stores.

## Shared Variable Style

Keep a slim repeated contract across scopes:

- `environment`
- `subscription_id`
- `location`
- `name_prefix`
- `run_id`
- `tags`

Then keep scope-specific knobs inside that scope only and only when a scope actually needs them.

Examples:

- `infra/_shared/env/dev1.tfvars`
- `infra/e2e-aks/env/dev1.tfvars`

## Scope Boundaries in This Repo

### `_shared`

Owns:

- the common non-secret environment baseline reused by multiple validation scopes

Does not own:

- scope-specific AKS or Azure-only settings
- secrets or run-specific identifiers

### `integration-azure`

Owns:

- temporary resource group
- user-assigned managed identity
- lower-cost Azure-backed validation inputs

Does not own:

- AKS
- Kubernetes manifests

### `e2e-aks`

Owns:

- temporary resource group
- user-assigned managed identity
- AKS cluster
- scope-local Kubernetes runtime manifests for the router smoke path

## Reserved Future Scopes

If this repository grows further, the next optional scopes would be:

- `infra/idm/` for identity-heavy setup if that logic becomes too large
- `infra/states/` if backend/state resources become repo-owned

Do not create those scopes before the repository genuinely needs them.

## Workflow Rule

GitHub workflows should target one scope root at a time, always include the shared baseline, and only add scope-local `env/*.tfvars` when that scope has extra settings.

Examples:

- `terraform -chdir=infra/integration-azure ... -var-file=../_shared/env/dev1.tfvars`
- `terraform -chdir=infra/e2e-aks ... -var-file=../_shared/env/dev1.tfvars -var-file=env/dev1.tfvars`

## Non-Goals

This repository is not trying to recreate the full scope matrix of `genai-infrastructure`.

The goal is:

- similar editing ergonomics
- similar `tfvars` discipline
- clearer boundaries for future infrastructure work

Not:

- a one-to-one copy of every external scope
- heavy environment inheritance or prefix logic

[Repository README](../../README.md) | [Internal docs](../README.md) | [_INFRA](./README.md)

# Terraform Scopes and Tfvars Model

## Purpose

This repository uses a scope-first Terraform layout inspired by `genai-infrastructure`, but in a much smaller form.

We copy the operating model, not the full platform volume.

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

## Tfvars Contract

`tfvars` are per-scope and per-environment, under `env/`.

Current convention:

- `env/dev1.tfvars` for the lower-cost day-to-day validation profile
- `env/prd1.tfvars` for the stricter or release-oriented profile

Sensitive values must not be committed to `tfvars`. Secrets and tenant-specific IDs still come from workflow inputs or GitHub/Azure secret stores.

## Shared Variable Style

Keep a slim repeated contract across scopes:

- `environment`
- `subscription_id`
- `location`
- `name_prefix`
- `run_id`
- `tags`

Then keep scope-specific knobs inside that scope only.

Examples:

- `infra/integration-azure/env/dev1.tfvars`
- `infra/e2e-aks/env/dev1.tfvars`

## Scope Boundaries in This Repo

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

GitHub workflows should target one scope root at a time and use that scope's `env/*.tfvars`.

Examples:

- `terraform -chdir=infra/integration-azure ... -var-file=env/dev1.tfvars`
- `terraform -chdir=infra/e2e-aks ... -var-file=env/dev1.tfvars`

## Non-Goals

This repository is not trying to recreate the full scope matrix of `genai-infrastructure`.

The goal is:

- similar editing ergonomics
- similar `tfvars` discipline
- clearer boundaries for future infrastructure work

Not:

- a one-to-one copy of every external scope
- heavy environment inheritance or prefix logic

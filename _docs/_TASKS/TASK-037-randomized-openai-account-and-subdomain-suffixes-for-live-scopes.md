[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-037: Randomized OpenAI Account and Subdomain Suffixes for Live Scopes
# FileName: TASK-037-randomized-openai-account-and-subdomain-suffixes-for-live-scopes.md

**Priority:** High
**Category:** Validation Infrastructure Hardening
**Estimated Effort:** Small
**Dependencies:** TASK-020, TASK-029, TASK-032
**Status:** **Done** (2026-03-17)

---

## Overview

Stop Azure OpenAI naming collisions in live validation scopes by adding randomized suffixes to generated Cognitive Services account names and default custom subdomains.

Business goal:
- avoid `CustomDomainInUse` conflicts caused by recently deleted Azure OpenAI resources
- make repeated local `e2e-aks-live-model` and `e2e-aks-live-embeddings` runs resilient to soft-delete retention windows
- ensure uniqueness survives the 24-character name limit instead of being truncated away with the old `run_id`-heavy naming pattern

---

## Sub-Tasks

- add the Terraform `random` provider to the live-model and live-embeddings scopes
- generate a stable random suffix per scope apply
- build the default account name and custom subdomain from a shortened base plus the random suffix
- document the behavior in local operator guidance

---

## Testing Requirements

- `terraform -chdir=infra/e2e-aks-live-model init -backend=false`
- `terraform -chdir=infra/e2e-aks-live-model validate`
- `terraform -chdir=infra/e2e-aks-live-embeddings init -backend=false`
- `terraform -chdir=infra/e2e-aks-live-embeddings validate`

---

## Documentation Updates Required

- `infra/e2e-aks-live-model/versions.tf`
- `infra/e2e-aks-live-model/locals.tf`
- `infra/e2e-aks-live-model/random.tf`
- `infra/e2e-aks-live-embeddings/versions.tf`
- `infra/e2e-aks-live-embeddings/locals.tf`
- `infra/e2e-aks-live-embeddings/random.tf`
- `docs/getting-started/local-development.md`
- `_docs/_TASKS/TASK-037-randomized-openai-account-and-subdomain-suffixes-for-live-scopes.md`
- `_docs/_TASKS/README.md`
- `_docs/_CHANGELOG/42-2026-03-17-randomized-openai-account-and-subdomain-suffixes-for-live-scopes.md`
- `_docs/_CHANGELOG/README.md`

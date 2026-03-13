[Repository README](./README.md) | [Official docs](./docs/README.md) | [Internal docs](./_docs/README.md)

# AGENTS.md

## Repository purpose

This repository builds a small, observable AI traffic router for Azure and AKS. It is not a generic AI platform. The MVP focuses on `chat/completions`, `embeddings`, deployment registry, health/failover, Managed Identity, API key fallback, and basic rate/concurrency limiting.

## Language policy

- All Markdown content in this repository must be written in English.
- All official docs, internal docs, task files, changelog entries, contribution guides, and repository metadata files must stay in English.
- New task and changelog slugs should use English words and ASCII hyphenated names.
- If an existing Markdown file is touched, it must remain or be converted to English as part of the change.

## Documentation model

- `docs/` is the official application documentation. It explains what the router does, how it behaves, and how operators or contributors should understand the product.
- `_docs/` is the internal delivery documentation. It stores MVP planning, task decomposition, changelog history, and implementation guidance used to evolve the repository with AI-assisted workflows.
- Do not mix these two audiences. Public/application-facing explanations belong in `docs/`. Internal execution and planning details belong in `_docs/`.

## Core principles

- Secretless by default. If a downstream supports Entra ID, the default outbound auth mode is `managed_identity`.
- Explainable routing is mandatory. Route selection and failover decisions must be reconstructable and observable.
- Keep the repository small, explicit, and testable. Prefer a small amount of owned logic over heavyweight framework magic.
- Use exact dependency pinning and controlled upgrades only.
- Stay aligned with the MVP architecture and pseudocode unless a newer task explicitly changes that direction.

## MVP scope

In scope:
- `chat/completions`
- `embeddings`
- deployment registry
- health, failover, cooldown, and circuit breaker behavior
- `managed_identity`
- `api_key` fallback
- basic rate limiting and concurrency limiting

Out of scope for MVP:
- workspace/prompt management
- publication/share flows
- runtime for custom apps
- full MCP platform layer
- generic OAuth vault
- cost-based, latency-based, ML-scored, cache-aware, or tenant-aware routing

## Architecture

- Clean Architecture is mandatory.
- `app/domain` contains only domain logic. No FastAPI, Redis, Azure SDK, or YAML parsing.
- `app/application` contains use cases, DTOs, orchestration, and ports.
- `app/infrastructure` contains adapters for YAML, Redis, Azure Identity, HTTPX, and observability.
- `app/entrypoints` contains HTTP/API glue only.
- Do not introduce ORM, relational database dependencies, event bus, queues, Celery, Kafka, `utils` dumps, or a catch-all `services.py`.

## Repository structure

Target structure:

```text
model-traffic-manager/
  README.md
  AGENTS.md
  CONTRIBUTING.md
  .pre-commit-config.yaml
  docs/
  _docs/
  configs/
  docker/
  app/
  tests/
```

## Stack and versioning

- Python `3.12.x`
- `uv` for project management, environment sync, and lock handling
- runtime: `fastapi`, `pydantic`, `pydantic-settings`, `httpx`, `uvicorn`, `anyio`, `azure-identity`, `azure-core`, `redis`, `structlog`, `prometheus-client`, OpenTelemetry, `pyyaml`
- dev/test: `pytest`, `pytest-asyncio`, `pytest-cov`, `respx`, `ruff`, `mypy`
- all direct runtime dependencies must use exact pins `==x.y.z`
- `uv.lock` is mandatory and committed with `pyproject.toml`
- do not use floating tags like `latest` for container images or dependency ranges
- dependency upgrades require a dedicated task, updated lock file, regression checks, and a changelog entry

## Configuration and auth

- MVP configuration is YAML validated by Pydantic at startup.
- Main sections are `router`, `deployments`, and `shared_services`.
- Configuration must be semantic: operators should understand `provider`, `account`, `region`, `tier`, `auth mode`, and `health state`.
- Each upstream must explicitly describe `id`, `provider`, `account`, `region`, `tier`, `weight`, `endpoint`, and `auth`.
- Validation is mandatory: unique deployment IDs, unique upstream IDs within a deployment, `tier >= 0`, `weight > 0`, valid URL, required `scope` for `managed_identity`, and required `header_name` / `secret_ref` for `api_key`.
- MVP auth modes are only `managed_identity`, `api_key`, and `none`.
- Client auth and router outbound auth are separate concerns. Do not forward client tokens as the default platform model.
- Managed Identity tokens are cached in-memory per instance using `(auth_mode, client_id, scope)` as the cache key.

## Routing and failover

- MVP routing uses one explicit strategy: `tiered_failover`.
- `tier` meaning is fixed: `0` primary, `1` regional/account failover, `2` disaster recovery / last resort.
- `weight` is only for balancing traffic inside the same tier.
- Selection flow: filter `unhealthy`, `cooldown`, and `circuit_open`; pick the lowest available tier; run weighted round robin within that tier.
- Weighted round robin is preferred over weighted random because it is easier to test, predict, and debug.
- Upstream state must distinguish at least `healthy`, `rate_limited`, `quota_exhausted`, `cooldown`, `unhealthy`, and `circuit_open`.
- `429` means `rate_limited` and must respect `Retry-After` when available.
- Circuit breaker is required per upstream.
- Retry is per request and only for retriable failures such as timeout, connection error, `429`, `500`, `502`, `503`, `504`, and recognized `quota_exhausted`.
- `400`, `401`, `403`, `404`, and payload validation errors do not trigger failover.

## Testing and definition of done

- Tests are part of the definition of done.
- Fast and deterministic unit tests are the default priority.
- Preferred test doubles: `fake`, then `stub`, then `spy`, then `mock`.
- Mandatory coverage areas: domain logic, use cases, auth, failure classification, and failover behavior, plus minimal integration checks for adapters and API wiring.
- The repository uses a permanent layered testing model:
  - `unit`: pure logic, no Azure, no AKS, no real external services
  - `integration-local`: FastAPI plus local config and local/in-process repositories or adapters
  - `integration-azure`: real Azure services, but not deployed on AKS
  - `e2e-aks`: full deployment validation on AKS
- Testing levels are cumulative. Adding a higher-level environment never replaces lower-level tests for the same area.
- Phase mapping:
  - Phase 0 and Phase 1 require `unit` and `integration-local`
  - Phase 2 keeps `unit` and `integration-local`; `integration-azure` becomes useful once real outbound provider calls exist
  - Phase 3 requires `integration-azure` for Managed Identity and Azure-native outbound auth scenarios
  - Phase 4 keeps all prior levels and may expand `integration-azure` for multi-upstream scenarios
  - Phase 5 keeps all prior levels and adds broader infra-backed integration coverage such as Redis-backed behavior
  - `e2e-aks` becomes mandatory once deployment, identity, Helm, and cluster runtime behavior need end-to-end proof
- The default coverage gate is `85%` for `app`.
- Expected quality gate once the Python application scaffold exists:

```text
uv run ruff check .
uv run mypy app
uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=85
```

## Task workflow

- Every repository task must create a task entry in `_docs/_TASKS/`.
- The business-oriented description goes into the main task file, for example `TASK-002-repository-foundation.md`.
- Technical details, pseudocode, target structure, and implementation breakdown go into subtasks, for example `TASK-002-01-public-docs-structure.md`.
- If a subtask becomes too large or too broad, split it again, for example `TASK-002-01-01-routing-reference.md`.
- Every task, subtask, and deeper work item must include `Documentation Updates Required`.
- Every task, subtask, and deeper work item must have `To Do`, `In Progress`, or `Done` status, including a date for `In Progress` and `Done`.
- API or security-sensitive tasks must include `Security Contract`.

## Documentation workflow

- Every documentation directory must contain its own `README.md`.
- Every documentation Markdown file except the repository root `README.md` should start with navigation controls to the parent index or the repository root.
- Whenever behavior changes, update the appropriate audience-facing docs:
  - `docs/` for official product/application documentation
  - `_docs/` for internal planning, workflow, and delivery documentation
- If a new documentation area is created, add its `README.md` and update the indexes above it.

## Changelog workflow

- After completing a task or a coherent set of tasks, create a new entry in `_docs/_CHANGELOG/`.
- The changelog entry must list every completed task and subtask ID that it covers.
- Update both `_docs/_CHANGELOG/README.md` and `_docs/_TASKS/README.md` when the changelog changes.
- Changelog file naming format is `{N}-{YYYY-MM-DD}-short-title.md`, where `N` is strictly increasing and never reused.

## Pre-commit workflow

- `.pre-commit-config.yaml` is the canonical pre-commit entry point for the repository.
- Pre-commit must run before every commit.
- The hooks must enforce repository text guardrails, documentation guardrails, and the Python quality gate once the application scaffold exists.
- When new repository-level checks are introduced, wire them into pre-commit in the same task.

## Execution rule

- If a new process rule is discovered while working in this repository, update `AGENTS.md` in the same task that introduces the rule.

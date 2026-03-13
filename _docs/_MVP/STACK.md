[Repository README](../../README.md) | [Internal docs](../README.md) | [_MVP](./README.md)

# Stack and version policy

## Primary decision

We use:

- Python `3.12`
- `uv` for project management, lock handling, and environments

We are not choosing Poetry as the starting point.

## Why `uv`

Reasons:

- fast resolver and sync
- simple `pyproject.toml`-based model
- `uv.lock` provides reproducibility
- strong fit for CI and Docker builds
- less extra abstraction than Poetry

## Why not Poetry

Poetry is reasonable, but for the MVP router it does not give us enough upside to justify the added behavior and command surface.

We need:

- a simple lock file
- simple environment sync
- a simple build path

`uv` is enough.

## Python version

We target:

- `Python 3.12.x`

Why:

- strong compatibility with the modern AI/web ecosystem
- less risk than aggressively jumping to the newest Python without validating all dependencies

Do not use "floating latest Python".

## Runtime versioning rule

- `3.12.x` is pinned in:
  - `pyproject.toml`
  - Docker image
  - CI
- moving to `3.13` or later requires a dedicated validation and release task

## Runtime libraries

We want a minimal set for MVP.

### API and DTOs

- `fastapi`
- `pydantic`
- `pydantic-settings`

### HTTP and async runtime

- `httpx`
- `uvicorn`
- `anyio`

### Azure auth

- `azure-identity`
- `azure-core`

### Redis

- `redis`

### Observability

- `structlog`
- `prometheus-client`
- `opentelemetry-api`
- `opentelemetry-sdk`
- `opentelemetry-instrumentation-fastapi`
- `opentelemetry-instrumentation-httpx`

### Config

- `pyyaml`

## Dev/test libraries

- `pytest`
- `pytest-asyncio`
- `pytest-cov`
- `respx`
- `ruff`
- `mypy`

## What we do not add for MVP

- ORM
- SQLAlchemy
- Celery
- Kafka client
- generic retry frameworks such as `tenacity`
- external circuit-breaker library if a small internal implementation is enough

Rule:

If the logic is small and domain-specific, prefer implementing it ourselves instead of pulling a heavy dependency.

## Dependency pinning policy

This is critical.

### Runtime dependencies

Every direct dependency must be pinned exactly:

- `package == x.y.z`

### Lock file

Commit:

- `uv.lock`

This is the single source of truth for transitive dependencies.

### No open ranges

Do not allow:

- `>=`
- `^`
- `~`
- `*`

in runtime dependencies.

## Dependency update policy

Dependencies are not updated "incidentally".

Every upgrade requires:

- a dedicated task
- updated lock file
- regression checks
- changelog entry

Example process:

1. branch `deps/1.1.0-refresh`
2. update selected packages
3. `uv lock`
4. run tests
5. release, for example `1.1.0`

## Router SemVer

- `1.0.0` first stable release
- `1.0.x` bugfixes without contract changes
- `1.1.0` new feature or approved dependency bump
- `2.0.0` breaking changes

## Container version control

Apply the same pinning rule to the image:

- pin the base image by digest
- do not use `python:3.12` without a digest
- do not use `latest`

## Repository tools

Target tools:

- `uv` for env and lock handling
- `ruff` for linting and formatting
- `mypy` for static analysis
- `pytest` for tests

## `pyproject.toml` skeleton

The starting point should look roughly like this:

```toml
[project]
name = "ai-router"
version = "0.1.0"
description = "Policy-driven AI router for Azure and AKS"
requires-python = "==3.12.*"
dependencies = [
  "fastapi==X.Y.Z",
  "pydantic==X.Y.Z",
  "pydantic-settings==X.Y.Z",
  "httpx==X.Y.Z",
  "uvicorn==X.Y.Z",
  "anyio==X.Y.Z",
  "azure-identity==X.Y.Z",
  "azure-core==X.Y.Z",
  "redis==X.Y.Z",
  "structlog==X.Y.Z",
  "prometheus-client==X.Y.Z",
  "opentelemetry-api==X.Y.Z",
  "opentelemetry-sdk==X.Y.Z",
  "opentelemetry-instrumentation-fastapi==X.Y.Z",
  "opentelemetry-instrumentation-httpx==X.Y.Z",
  "pyyaml==X.Y.Z",
]

[dependency-groups]
dev = [
  "pytest==X.Y.Z",
  "pytest-asyncio==X.Y.Z",
  "pytest-cov==X.Y.Z",
  "respx==X.Y.Z",
  "ruff==X.Y.Z",
  "mypy==X.Y.Z",
]
```

`X.Y.Z` must not be a range. It must be a concrete, approved version chosen during repository bootstrap.

## Dependency bootstrap rule

When the repository is first created:

1. select the dependency set
2. validate compatibility with Python `3.12`
3. write exact pins into `pyproject.toml`
4. generate `uv.lock`
5. commit both files together

After that there are no spontaneous updates.

## Example tool workflow

```text
uv sync --frozen
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=85
```

## Cluster rule

The cluster must not update dependencies on its own.

That means:

- every dependency is part of the image
- the image is immutable

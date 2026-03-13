[Repository README](../../README.md) | [docs](../README.md) | [Architecture](./README.md)

# System Overview

The router follows Clean Architecture.

High-level shape:

- `app/domain` for pure routing and policy logic
- `app/application` for use cases and orchestration
- `app/infrastructure` for adapters such as config, auth, HTTP, and observability
- `app/entrypoints` for the FastAPI HTTP surface

What is already implemented:

- startup-time YAML loading and validation
- typed deployment/upstream/auth configuration models
- config-backed deployment repository
- `ListDeployments` as the first application use case
- `/deployments` and health endpoints as the first HTTP surfaces

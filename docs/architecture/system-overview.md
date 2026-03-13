[Repository README](../../README.md) | [docs](../README.md) | [Architecture](./README.md)

# System Overview

The router follows Clean Architecture.

High-level shape:

- `app/domain` for pure routing and policy logic
- `app/application` for use cases and orchestration
- `app/infrastructure` for adapters such as config, auth, HTTP, and observability
- `app/entrypoints` for the FastAPI HTTP surface

The current bootstrap implements only the minimum HTTP shell and runtime wiring needed before feature logic is added.

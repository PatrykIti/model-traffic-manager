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
- `RouteChatCompletion` and `RouteEmbeddings` as the current proxying use cases
- tiered multi-upstream selection with weighted round robin and request-level failover
- request correlation, runtime decision events, and `/metrics` as the current observability surface
- `/deployments`, `/v1/chat/completions/{deployment_id}`, `/v1/embeddings/{deployment_id}`, health endpoints, and `/metrics` as the current HTTP surfaces

Boundary note:

- this router is the internal LLM traffic manager for the chatbot system runtime
- it is not the SaaS tenant orchestrator, onboarding service, or tenant control-plane router

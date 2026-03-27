# model-traffic-manager

Azure-native AI traffic routing for teams that need one stable endpoint across Azure OpenAI accounts, regions, and deployments.

`model-traffic-manager` is a policy-driven router for `chat/completions`, `embeddings`, and selected backend-facing shared services. It focuses on secretless auth, explainable routing, health-aware failover, and live AKS validation without turning into a generic AI gateway or tenant control plane.

- One stable endpoint for AI traffic on Azure and AKS
- Managed Identity first, with explicit API-key fallback only when required
- Explainable failover, cooldown, and circuit behavior you can actually debug
- Inbound auth with router-owned API bearer tokens or Microsoft Entra ID

If this project helps your team ship reliable Azure AI traffic faster, sponsorship is welcome. Support directly funds documentation, live validation coverage, and roadmap time for the next production-grade capabilities.

## Why teams use it

- Route across multiple Azure AI / Azure OpenAI accounts and regions without teaching every backend how to fail over.
- Keep outbound auth secretless by default when downstreams support Managed Identity.
- Protect router entrypoints with either opaque API bearer tokens or Entra ID access tokens for app-to-app callers.
- Expose routing decisions, rejected candidates, and caller-safe observability fields for support and audit trails.
- Validate the real deployment path with opt-in Azure and AKS live suites instead of relying only on mocks.

## Product focus

This repository is intentionally narrow:

- it is an internal AI traffic router for Azure-native backends
- it is not a generic AI platform, SaaS control plane, prompt workspace, or tenant orchestrator
- it favors explicit configuration, predictable routing, and operator supportability over framework magic

That focus is the product. The goal is to give platform teams a small, explainable router they can trust in production.

## Current capabilities

- `POST /v1/chat/completions/{deployment_id}` with tiered multi-upstream failover
- `POST /v1/embeddings/{deployment_id}` with tiered multi-upstream failover
- `POST /v1/shared-services/{service_id}` for selected backend-facing shared services
- startup-time YAML validation with typed deployment and shared-service registries
- outbound auth modes `none`, `api_key`, and `managed_identity`
- inbound auth modes `api_bearer_token` and `entra_id`
- weighted round robin within the lowest healthy tier
- cooldown, quota-aware classification, circuit opening, and half-open recovery
- in-memory and Redis-backed runtime state for shared health and limiter coordination
- deployment-level request-rate limiting and concurrency limiting
- request correlation, runtime decision events, Prometheus `/metrics`, and OpenTelemetry trace foundations
- live validation suites for smoke, live chat, live embeddings, load balancing, shared services, inbound auth, observability, and Redis-backed multi-replica behavior

## Quick start

```text
make bootstrap
make check
make run
```

Local setup notes:

- copy or reference values from [`.env.example`](./.env.example)
- keep the router YAML in [`configs/example.router.yaml`](./configs/example.router.yaml) or point `MODEL_TRAFFIC_MANAGER_CONFIG_PATH` to another file
- use `MODEL_TRAFFIC_MANAGER_RUNTIME_STATE_BACKEND=redis` together with `MODEL_TRAFFIC_MANAGER_REDIS_URL` when you want shared runtime state locally

Useful local endpoints after startup:

- `GET /health/live`
- `GET /health/ready`
- `GET /deployments`
- `GET /shared-services`
- `POST /v1/shared-services/{service_id}`
- `POST /v1/chat/completions/{deployment_id}`
- `POST /v1/embeddings/{deployment_id}`

## Validation

The repository keeps a layered validation model:

- local quality gate: `make check`
- Azure-backed integration without AKS: `make integration-azure-local`
- AKS smoke and live suites: `make e2e-aks-local`
- real model-response validation on AKS: `make e2e-aks-live-model-local`
- live inbound auth validation on AKS: `make e2e-aks-live-inbound-auth-local`
- live request-flow observability validation on AKS: `make e2e-aks-live-observability-local`

The higher-level suites are intentionally opt-in because they provision temporary Azure resources and can consume real model quota.

## Documentation

- [Official docs](./docs/README.md) explain the product, runtime behavior, configuration model, routing, and operations guidance.
- [Internal docs](./_docs/README.md) track delivery planning, task decomposition, and internal changelog history.
- [AGENTS.md](./AGENTS.md) is the repository working agreement for maintainers and AI-assisted workflows.

## Community and support

- [Contributing guide](./CONTRIBUTING.md)
- [Support guide](./SUPPORT.md)
- [Security policy](./SECURITY.md)
- [Code of conduct](./CODE_OF_CONDUCT.md)
- [Release changelog](./CHANGELOG.md)

If `model-traffic-manager` saves your team time, reduces routing risk, or helps you standardize Azure AI traffic, support it through the repository sponsor button or [GitHub Sponsors](https://github.com/sponsors/PatrykIti). Sponsorship helps fund documentation, reliability work, live AKS validation, and the larger product roadmap around production chatbot infrastructure.

## License

This repository is licensed under [Apache-2.0](./LICENSE).

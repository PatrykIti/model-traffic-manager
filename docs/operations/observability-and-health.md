[Repository README](../../README.md) | [docs](../README.md) | [Operations](./README.md)

# Observability and Health

The current runtime includes:

- structured logging setup
- health endpoints
- smoke tests for startup and health checks
- in-memory and Redis-backed health-state persistence for upstreams
- cooldown, circuit-open, and half-open recovery transitions that affect routing eligibility
- deployment-level request-rate limiting and concurrency limiting
- HTTP rejection behavior for limiter saturation (`429` for request-rate, `503` for concurrency)
- Redis-backed limiter adapters available in the active runtime when the Redis backend is enabled
- request correlation through `x-request-id`
- structured runtime events for route selection, health updates, limiter rejections, and request completion
- rejected-candidate metadata and explicit failover reasons in route-selection events
- shared-service execution events on the same structured event stream when a shared service is router-callable
- a Prometheus `/metrics` endpoint
- trace spans for inbound requests plus outbound model attempt spans
- an opt-in Azure Monitor / Application Insights export path for OpenTelemetry traces
- final-upstream attribution on the request span, including provider, account, region, and optional `capacity_mode`
- a startup-time topology snapshot in pod logs, plus a lightweight startup trace when Azure Monitor export is enabled
- a persistent outbound HTTP client with explicit connection-pool and timeout policy
- `make release-check` as the current release validation command

Operational notes:

- `GET /shared-services` exposes the runtime view of configured shared services
- `POST /v1/shared-services/{service_id}` reuses the same request correlation and runtime event model for router-proxy shared services
- `MODEL_TRAFFIC_MANAGER_RUNTIME_STATE_BACKEND=redis` switches health and limiter coordination to shared Redis state
- `MODEL_TRAFFIC_MANAGER_OBSERVABILITY_BACKEND=azure_monitor` enables Azure Monitor export for the router-owned trace flow
- `MODEL_TRAFFIC_MANAGER_AZURE_MONITOR_LOG_EXPORT_ENABLED=true` also mirrors Python logs through the Azure Monitor log exporter
- the default local bootstrap still uses `in_memory` state for a zero-dependency startup path

Operational recommendation:

- use the request trace as the primary investigation surface for route selection, failover, cooldown, circuit, and final-upstream attribution
- keep pod logs for startup topology confirmation and last-resort local inspection
- avoid using raw payload logging as a substitute for explicit routing metadata

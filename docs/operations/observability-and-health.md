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
- a Prometheus `/metrics` endpoint
- trace spans for inbound requests plus outbound model attempt spans
- a persistent outbound HTTP client with explicit connection-pool and timeout policy
- `make release-check` as the current release validation command

Operational notes:

- `GET /shared-services` exposes the runtime view of configured shared services
- `MODEL_TRAFFIC_MANAGER_RUNTIME_STATE_BACKEND=redis` switches health and limiter coordination to shared Redis state
- the default local bootstrap still uses `in_memory` state for a zero-dependency startup path

Future iterations can still extend this into broader chaos-style validation and exporter-specific production tuning.

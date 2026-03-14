[Repository README](../../README.md) | [docs](../README.md) | [Operations](./README.md)

# Observability and Health

The current runtime includes:

- structured logging setup
- health endpoints
- smoke tests for startup and health checks
- in-memory health-state persistence for upstreams
- cooldown and circuit-open transitions that affect routing eligibility
- a Redis-backed health-state adapter implementation behind the repository port
- deployment-level request-rate limiting and concurrency limiting
- HTTP rejection behavior for limiter saturation (`429` for request-rate, `503` for concurrency)
- Redis-backed limiter adapters behind the application ports
- request correlation through `x-request-id`
- structured runtime events for route selection, health updates, limiter rejections, and request completion
- a Prometheus `/metrics` endpoint
- trace spans for inbound requests plus outbound model attempt spans

Future iterations will extend this into:

- Azure-backed validation of observability behavior
- richer troubleshooting guidance and operator runbooks
- hardening around exporter configuration and runtime tuning

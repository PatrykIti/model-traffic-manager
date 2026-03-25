[Repository README](../../README.md) | [docs](../README.md) | [Architecture](./README.md)

# Request Lifecycle

Target request flow:

1. client calls a deployment endpoint
2. the API entrypoint maps the request into a use case
3. the use case loads deployment and health state
4. routing policy selects an upstream
5. outbound auth is prepared
6. request is sent
7. health/metrics are updated
8. response is returned

Current status:

- `GET /deployments` is implemented through the config-backed deployment repository
- `GET /shared-services` is implemented through the config-backed shared-service registry
- `POST /v1/shared-services/{service_id}` is implemented for router-proxied HTTP/JSON shared services
- `POST /v1/chat/completions/{deployment_id}` and `POST /v1/embeddings/{deployment_id}` are implemented with tiered multi-upstream selection and request-level failover
- `POST /v1/shared-services/{service_id}` is implemented for router-proxy shared services with HTTP/JSON payloads
- health-state loading and updates are implemented for cooldown, circuit-open, and half-open recovery behavior
- route-selection events record failover reasons and rejected candidates
- metrics and trace hooks are implemented on the active runtime path
- the request span now records the final selected upstream plus operator-facing routing metadata such as provider, account, region, and optional capacity mode
- an opt-in Azure Monitor / Application Insights export path can mirror the request flow into OpenTelemetry traces

Current implemented path:

1. startup loads and validates `configs/example.router.yaml`
2. validated config is stored in the bootstrap container
3. the container exposes config-backed deployment and shared-service repositories
4. `GET /deployments` returns deployment summaries from that repository
5. `GET /shared-services` returns shared-service summaries from that repository
6. `POST /v1/shared-services/{service_id}` either rejects direct-access services or executes router-proxied shared services
7. for tiered shared-service routes, the use case loads persisted health state and applies the same failover logic used by model traffic
8. the routing selector chooses the lowest available healthy tier, prefers healthy candidates over half-open probes, and applies weighted round robin inside the selected tier
9. the use case builds outbound auth headers and sends the upstream request
10. retriable failures are classified, persisted into health state, and may move to the next eligible upstream
11. route-selection, limiter, and completion events are recorded with request correlation metadata
12. the final request span stores the upstream that actually served the request or the terminal failure path that ended it

Startup diagnostics:

1. application startup emits a structured topology snapshot to pod logs
2. the snapshot summarizes active deployments, upstream IDs, tiers, balancing metadata, runtime-state backend, and observability mode
3. when Azure Monitor export is enabled, a lightweight startup trace is also emitted for the boot path

Shared-service execution path:

1. client or backend calls `POST /v1/shared-services/{service_id}`
2. the API entrypoint parses JSON and resolves the shared service from the registry
3. `direct_backend_access` services fail closed because they are metadata-only from the router perspective
4. `single_endpoint` services execute one downstream HTTP/JSON call through the router
5. `tiered_failover` services reuse the health-aware multi-upstream failover path
6. runtime events record the service decision path just like routed LLM traffic

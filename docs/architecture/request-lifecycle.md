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
- `POST /v1/chat/completions/{deployment_id}` and `POST /v1/embeddings/{deployment_id}` are implemented with tiered multi-upstream selection and request-level failover
- health-state loading and updates are implemented for cooldown, circuit-open, and half-open recovery behavior
- route-selection events record failover reasons and rejected candidates
- metrics and trace hooks are implemented on the active runtime path

Current implemented path:

1. startup loads and validates `configs/example.router.yaml`
2. validated config is stored in the bootstrap container
3. the container exposes config-backed deployment and shared-service repositories
4. `GET /deployments` returns deployment summaries from that repository
5. `GET /shared-services` returns shared-service summaries from that repository
6. the use case loads persisted health state for the deployment upstreams
7. the routing selector chooses the lowest available healthy tier, prefers healthy candidates over half-open probes, and applies weighted round robin inside the selected tier
8. the use case builds outbound auth headers and sends the upstream request
9. retriable failures are classified, persisted into health state, and may move to the next eligible upstream
10. route-selection, limiter, and completion events are recorded with request correlation metadata

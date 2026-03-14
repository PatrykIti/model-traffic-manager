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
- `POST /v1/chat/completions/{deployment_id}` and `POST /v1/embeddings/{deployment_id}` are implemented for deterministic single-upstream routing
- health-state loading, failover, retry attempts, metrics, and decision logging are still ahead

Current implemented path:

1. startup loads and validates `configs/example.router.yaml`
2. validated config is stored in the bootstrap container
3. the container exposes a config-backed deployment repository
4. `GET /deployments` returns deployment summaries from that repository
5. `POST /v1/chat/completions/{deployment_id}` resolves one upstream, builds auth headers, and proxies the request
6. `POST /v1/embeddings/{deployment_id}` follows the same single-upstream bootstrap flow

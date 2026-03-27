[Repository README](../../README.md) | [Internal docs](../README.md) | [_MVP](./README.md)

# MVP roadmap

## Phase 0 - repository bootstrap

- create the Python repository
- `uv init`
- `pyproject.toml`
- `uv.lock`
- Dockerfile
- FastAPI skeleton
- Ruff / Mypy / Pytest
- `pytest-cov`

Output:

- the service starts as a repository scaffold

## Phase 1 - domain and config

- domain models
- Pydantic config models
- YAML loading
- config validation
- deployment listing
- unit tests for validation and domain logic

Output:

- the service starts and reads valid config

## Phase 2 - single-upstream routing

- `RouteChatCompletion`
- `RouteEmbeddings`
- HTTPX outbound invoker
- auth `none` and `api_key`
- basic error mapping
- unit tests for use cases with mocked ports

Output:

- router works for one upstream

## Phase 3 - Managed Identity

- `managed_identity` auth mode
- Azure token provider
- token cache
- integration tests with stub
- unit tests for auth service and token cache

Output:

- secretless outbound auth

## Phase 4 - multi-upstream and tiers

- selection policy
- weighted round robin
- failover across tiers
- request attempts
- domain tests for selection and failover

Output:

- primary/secondary routing

## Phase 5 - health, cooldown, and circuit breaker

- Redis health repository
- failure classification
- cooldown after `429`
- circuit breaker after repeated failures
- tests for health state logic and failure classification

Output:

- sensible behavior under outages

## Phase 6 - observability

- structlog
- Prometheus
- OpenTelemetry
- explainable route decisions
- tests for decision logs and metric events

Output:

- clear visibility into what happened and why

## Phase 7 - hardening

- timeout policy
- connection pool tuning
- load testing
- chaos scenarios
- security review
- stronger and stabilized coverage gate

Output:

- candidate for `1.0.0`

[Repository README](../../README.md) | [Internal docs](../README.md) | [_MVP](./README.md)

# Repository structure

## Goal

The repository should stay small, readable, and aligned with Clean Architecture.

## Proposed structure

```text
ai-router/
  pyproject.toml
  uv.lock
  README.md
  .python-version
  .gitignore
  docker/
    Dockerfile
    entrypoint.sh
  configs/
    example.router.yaml
  app/
    domain/
      entities/
        deployment.py
        upstream.py
      value_objects/
        auth_policy.py
        route_decision.py
        health_state.py
      policies/
        routing_policy.py
        failure_classification.py
      services/
        upstream_selector.py
    application/
      dto/
        route_request.py
        route_response.py
      ports/
        deployment_repository.py
        health_repository.py
        token_provider.py
        outbound_invoker.py
        rate_limiter.py
        metrics_port.py
      use_cases/
        route_chat_completion.py
        route_embeddings.py
        list_deployments.py
        record_upstream_result.py
    infrastructure/
      config/
        models.py
        yaml_loader.py
      auth/
        azure_msi_token_provider.py
        api_key_provider.py
      http/
        httpx_outbound_invoker.py
        fastapi_dependencies.py
      persistence/
        redis_health_repository.py
      observability/
        metrics.py
        tracing.py
        logging.py
    entrypoints/
      api/
        main.py
        routes_chat.py
        routes_embeddings.py
        routes_deployments.py
        error_handlers.py
  tests/
    unit/
      domain/
      application/
      infrastructure/
    integration/
      api/
      infrastructure/
```

## Directory ownership

### `app/domain`

Only domain logic.

No imports from:

- FastAPI
- Redis
- Azure SDK

### `app/application`

Use cases and contracts.

This is where we:

- assemble requests
- call policies
- use ports

### `app/infrastructure`

Everything that talks to the outside world:

- YAML
- Redis
- Azure Identity
- HTTPX
- telemetry

### `app/entrypoints`

Web framework and HTTP mapping.

### `tests/unit`

Test:

- upstream selection
- failure classification
- auth policy mapping
- use case orchestration

without real Redis or real Azure.

Use mocks, fakes, and stubs such as:

- mocked ports
- fake clock
- fake token provider
- fake outbound invoker
- fake health repository

### `tests/integration`

Test:

- FastAPI endpoints
- Redis adapter
- outbound invoker
- MSI provider through controlled stub/mock

For MVP, integration tests complement unit tests; they do not replace them.

## What to avoid

- utils dump
- shared helpers without clear ownership
- mixing configuration with domain logic
- a `services.py` that does everything

[README repo](../../README.md) | [_docs](../README.md) | [_MVP](./README.md)

# Repository structure

## Cel

Repo ma byc male, czytelne i zgodne z Clean Architecture.

## Proponowana struktura

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

## Odpowiedzialnosc katalogow

## `app/domain`

Tylko logika domenowa.

Bez importow:

- FastAPI
- Redis
- Azure SDK

## `app/application`

Use case'y i kontrakty.

To jest miejsce, gdzie:

- skladamy request
- wywolujemy polityki
- korzystamy z portow

## `app/infrastructure`

Wszystko, co gada ze swiatem zewnetrznym:

- YAML
- Redis
- Azure Identity
- HTTPX
- telemetry

## `app/entrypoints`

Framework webowy i mapowanie HTTP.

## `tests/unit`

Testujemy:

- selekcje upstreamow
- failure classification
- auth policy mapping
- use case orchestration

bez prawdziwego Redis i bez prawdziwego Azure.

Tu uzywamy mockow i stubow:

- mockowane porty
- fake clock
- fake token provider
- fake outbound invoker
- fake health repository

## `tests/integration`

Testujemy:

- FastAPI endpointy
- Redis adapter
- outbound invoker
- MSI provider przez stub/mock

Na MVP integracyjne testy maja byc dodatkiem do unit testow, nie ich zamiennikiem.

## Czego unikamy

- utils dump
- wspolnych helperow bez odpowiedzialnosci
- mieszania configu z logika domeny
- "services.py" robiacego wszystko

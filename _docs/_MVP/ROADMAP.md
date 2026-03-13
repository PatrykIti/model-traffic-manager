[README repo](../../README.md) | [_docs](../README.md) | [_MVP](./README.md)

# Roadmap MVP

## Faza 0 - bootstrap repo

- utworzenie repo Python
- `uv init`
- `pyproject.toml`
- `uv.lock`
- Dockerfile
- FastAPI skeleton
- Ruff / Mypy / Pytest
- `pytest-cov`

## Faza 1 - domain i config

- modele domenowe
- modele Pydantic configu
- ladowanie YAML
- walidacja configu
- listowanie deploymentow
- unit testy dla walidacji i domeny

Wyjscie:

- serwis startuje i czyta poprawny config

## Faza 2 - routing single upstream

- `RouteChatCompletion`
- `RouteEmbeddings`
- outbound invoker HTTPX
- auth `none` i `api_key`
- podstawowe mapowanie bledow
- unit testy use case'ow z mockowanymi portami

Wyjscie:

- router dziala dla jednego upstreamu

## Faza 3 - Managed Identity

- `managed_identity` auth mode
- Azure token provider
- token cache
- testy integracyjne przez stub
- unit testy dla auth service i token cache

Wyjscie:

- secretless outbound auth

## Faza 4 - multi-upstream i tiers

- selection policy
- weighted round robin
- failover miedzy tierami
- request attempts
- testy domenowe dla selekcji i failoveru

Wyjscie:

- primary/secondary routing

## Faza 5 - health, cooldown, circuit breaker

- Redis health repository
- failure classification
- cooldown po `429`
- circuit breaker po seriach porazek
- testy logiki health state i klasyfikacji bledow

Wyjscie:

- sensowne zachowanie przy awariach

## Faza 6 - observability

- structlog
- Prometheus
- OpenTelemetry
- explainable route decisions
- testy mapowania decision logs i metrics events

Wyjscie:

- widac, co sie dzieje i dlaczego

## Faza 7 - hardening

- timeout policy
- connection pool tuning
- load testing
- chaos scenarios
- security review
- podniesienie i ustabilizowanie coverage gate

Wyjscie:

- kandydat do `1.0.0`

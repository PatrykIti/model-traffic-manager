[README repo](../../README.md) | [_docs](../README.md) | [_MVP](./README.md)

# Testing strategy

## Zasada glowna

Wszystko ma byc testowane tak, zeby bylo wiadomo, ze dziala przed deploymentem.

Na MVP testy nie sa dodatkiem. Sa czescia definicji done.

## Co jest obowiazkowe

- unit testy dla domeny
- unit testy dla use case'ow
- unit testy dla logiki auth
- unit testy dla klasyfikacji bledow i failoveru
- integracyjne minimum dla adapterow i API
- coverage sprawdzany przez `pytest-cov`

## Priorytet testow

### 1. Unit tests

To ma byc glowny typ testow.

Testujemy:

- routing policy
- selection upstreamu
- fallback miedzy tierami
- circuit breaker
- cooldown po `429`
- klasyfikacje bledow
- token cache
- mapowanie auth headers
- use case orchestration

Unit testy maja byc:

- szybkie
- deterministyczne
- bez prawdziwego Redis
- bez prawdziwego Azure
- bez prawdziwych zewnetrznych endpointow

### 2. Integration tests

Tylko tyle, ile potrzebne do potwierdzenia, ze adaptery sa dobrze spiete:

- FastAPI endpointy
- Redis repository
- HTTPX invoker
- MSI token provider przez kontrolowany stub/mock

### 3. E2E

Nie sa wymagane na sam start MVP.

Mozna je dodac pozniej, gdy bedzie pierwszy staging deployment.

## Jak mockujemy

Mockowanie ma byc zgodne z clean architecture.

Najpierw mockujemy porty, nie framework i nie prywatne detale klas.

### Mockowane elementy

- `DeploymentRepository`
- `HealthRepository`
- `TokenProvider`
- `OutboundInvoker`
- `RateLimiterPort`
- `ClockPort`
- `MetricsPort`

### Preferred test doubles

Kolejnosc preferencji:

1. fake
2. stub
3. spy
4. mock

Jesli wystarczy fake albo stub, nie trzeba isc w agresywne mockowanie.

## Co sprawdzamy testami

## Routing

- wybiera najnizszy zdrowy tier
- nie wybiera upstreamu w cooldownie
- nie wybiera upstreamu z `circuit_open`
- przechodzi do kolejnego tieru, gdy primary odpada
- zachowuje weighted round robin w obrebie tieru

## Failover

- retriable bledy przechodza do kolejnej proby
- non-retriable bledy nie odpalaja failoveru
- `429` ustawia cooldown
- seria `5xx` otwiera circuit
- `half-open` pozwala na probe powrotu

## Auth

- `managed_identity` pobiera token dla poprawnego `scope`
- `managed_identity` uzywa `client_id`, jesli jest ustawiony
- token cache nie pobiera ponownie tokena bez potrzeby
- `api_key` zwraca poprawny header
- `none` nie doklada auth headers

## API

- poprawne mapowanie bledow domenowych na HTTP
- poprawne przekazanie payloadu do use case'a
- zwrocenie odpowiedzi upstreamu bez psucia kontraktu

## Coverage

Na start wymagamy:

- `pytest --cov=app --cov-report=term-missing --cov-fail-under=85`

To jest minimalny prog dla MVP.

Docelowo po ustabilizowaniu projektu mozna podniesc np. do `90`.

## Coverage policy

Coverage nie jest celem samym w sobie.

Ale:

- brak coverage oznacza, ze nie wiemy, czego nie testujemy
- prog coverage chroni przed erozja testow

Dlatego coverage ma byc gate'em w CI.

## Definition of Done dla kazdej zmiany

Zmiana jest gotowa, gdy:

- ma testy jednostkowe dla nowej logiki
- nie psuje istniejacych testow
- przechodzi coverage gate
- przechodzi lint i type-check

Minimalny check:

```text
uv run ruff check .
uv run mypy app
uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=85
```

## Czego nie robimy

- nie polegamy tylko na manualnym testowaniu
- nie testujemy przez sleep-driven flaky tests
- nie robimy testow, ktore wymagaja prawdziwego Azure w CI unitowym
- nie mockujemy wszystkiego na slepo na poziomie framework magic

## Najwazniejsza zasada

> Logika routingu i auth ma byc udowadnialna testami jednostkowymi.

Bez tego taki router szybko stanie sie trudny do zaufania operacyjnie.

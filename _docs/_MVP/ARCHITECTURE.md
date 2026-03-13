[README repo](../../README.md) | [_docs](../README.md) | [_MVP](./README.md)

# Architecture

## Architektura logiczna

Przyjmujemy Clean Architecture.

Chcemy rozdzielic:

- domene routingu
- use case'y aplikacyjne
- adaptery infrastrukturalne
- framework HTTP

tak, aby routing i auth nie byly zalezne od FastAPI, Redis ani Azure SDK.

## Warstwy

## 1. Domain

Najczystsza warstwa.

Zawiera:

- encje
- value objects
- polityki
- uslugi domenowe

Przykladowe typy:

- `Deployment`
- `Upstream`
- `AuthPolicy`
- `RoutingPolicy`
- `HealthState`
- `CircuitState`
- `RouteDecision`
- `FailureReason`

W tej warstwie nie ma:

- HTTP
- Redis
- Azure SDK
- YAML parsera

## 2. Application

Warstwa use case'ow.

Zawiera:

- orkiestracje requestu
- wywolywanie polityk domenowych
- wywolywanie portow
- translacje DTO wejsciowych/wyjsciowych

Przykladowe use case'y:

- `RouteChatCompletion`
- `RouteEmbeddings`
- `ListDeployments`
- `EvaluateCandidateUpstreams`
- `AcquireOutboundCredentials`
- `RecordUpstreamFailure`
- `RecordUpstreamSuccess`

## 3. Ports

Porty to kontrakty do zewnetrznego swiata.

Przykladowe porty:

- `DeploymentRepository`
- `HealthRepository`
- `TokenProvider`
- `OutboundInvoker`
- `RateLimiterPort`
- `MetricsPort`
- `TracerPort`
- `ClockPort`

Ten model jest tez potrzebny pod testy:

- use case testujemy na mockowanych portach
- domene testujemy bez infrastruktury
- adaptery testujemy osobno kontraktowo

## 4. Infrastructure / Adapters

Implementacje portow.

Przyklady:

- YAML config repository
- Redis health repository
- Azure MSI token provider
- HTTPX outbound invoker
- Prometheus adapter
- OpenTelemetry adapter

## 5. Entrypoints

Framework i API.

Na MVP:

- FastAPI
- DTO request/response
- mapowanie bledow domenowych na HTTP

## Bounded contexts w MVP

Nie robimy wielu mikroserwisow. Robimy jeden serwis, ale logicznie rozdzielamy konteksty:

- Routing
- Outbound Auth
- Health and Failover
- Config Loading
- Observability

## Glowny flow requestu

1. Klient wywoluje deployment.
2. Entrypoint mapuje request do use case'a.
3. Use case pobiera definicje deploymentu.
4. Use case pobiera health state upstreamow.
5. Domena wybiera najlepszy kandydat.
6. Application pyta `TokenProvider` o outbound auth.
7. `OutboundInvoker` wysyla request.
8. Wynik aktualizuje health state i metrics.
9. Odpowiedz wraca do klienta.

## Error model

Nie chcemy, zeby wszystkie bledy byly "500".

Podstawowe klasy bledow:

- `DeploymentNotFound`
- `NoHealthyUpstream`
- `UpstreamRateLimited`
- `UpstreamQuotaExhausted`
- `AuthAcquisitionFailed`
- `OutboundTimeout`
- `OutboundConnectionError`
- `ConfigValidationError`

## Komponenty runtime

Minimalny zestaw komponentow:

- API process
- config loader
- Redis connection
- outbound HTTP client pool
- token cache
- metrics endpoint

## Dane trwale i ulotne

### Dane trwale

Na MVP:

- konfiguracja w repo i obrazie
- opcjonalnie mounted config file

### Dane ulotne

W Redis:

- circuit breaker state
- cooldowny po bledach
- rate limit counters
- optional distributed health state

## Co celowo omijamy

Nie wprowadzamy osobnych warstw typu:

- ORM
- baza relacyjna
- event bus
- kolejki

Nie sa potrzebne w MVP routera.

## Diagram odpowiedzialnosci

```text
FastAPI -> Application Use Case -> Domain Policy
                              -> Ports
                              -> Infrastructure Adapters
```

## Dodatkowe decyzje architektoniczne

- async first
- bez ukrywania flow w framework magic
- domena testowana bez infrastruktury
- adaptery testowane kontraktowo
- config walidowany przy starcie
- brak dynamicznego self-mutation configu w v1
- kazdy use case musi miec unit testy

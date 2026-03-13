[README repo](../../README.md) | [_docs](../README.md) | [_MVP](./README.md)

# Routing i failover

## Cel

Routing ma byc:

- prosty do zrozumienia
- przewidywalny
- dobrze obserwowalny
- wystarczajaco mocny operacyjnie

Nie budujemy na MVP skomplikowanego policy engine.

## Model domenowy

Glowny model:

- `Deployment`
- `Upstream`
- `HealthState`
- `CircuitState`
- `RouteDecision`

## `tier`

Zostawiamy `tier`, ale nadajemy mu jawne znaczenie.

- `tier=0` -> primary
- `tier=1` -> regional/account failover
- `tier=2` -> DR / last resort

To nie jest "ukryty priorytet", tylko oficjalna hierarchia fallbacku.

## `weight`

`weight` sluzy tylko do rozkladu ruchu w obrebie tego samego tieru.

Nie uzywamy go do:

- opisu kosztu
- opisu zdrowia
- opisu waznosci biznesowej

## Algorytm wyboru

Na MVP:

1. wybierz upstreamy dla deploymentu
2. odfiltruj `unhealthy`, `cooldown`, `circuit_open`
3. podziel kandydatow po `tier`
4. wez najnizszy dostepny tier
5. w obrebie tieru wybierz przez weighted round robin

## Dlaczego nie weighted random

Weighted round robin jest bardziej przewidywalny operacyjnie niz losowanie.

Latwiej:

- testowac
- przewidywac rozklad
- debugowac

## Klasy stanów upstreamu

Upstream moze byc:

- `healthy`
- `rate_limited`
- `quota_exhausted`
- `cooldown`
- `unhealthy`
- `circuit_open`

To jest lepsze niz wrzucanie wszystkiego do jednego "failed".

## Kiedy oznaczamy upstream jako uszkodzony

Przy:

- timeout
- connection error
- `500`
- `502`
- `503`
- `504`

## Kiedy oznaczamy upstream jako rate limited

Przy:

- `429`

Jesli mamy `Retry-After`, respektujemy go.

## Kiedy oznaczamy upstream jako quota exhausted

Gdy provider lub adapter zwraca sygnal, ze problem nie jest chwilowym rate limit, tylko wyczerpaniem przydzialu.

Na MVP mozna to ustalic przez:

- znane statusy lub patterny odpowiedzi
- adapter-specific mapper

## Circuit breaker

Potrzebujemy prostego circuit breakera per upstream.

### Reguly

- po `N` kolejnych porazkach otwieramy circuit
- po czasie `half_open_after` probujemy pojedynczy request testowy
- sukces zamyka circuit
- porazka znowu otwiera circuit

## Cooldown

Po `429` albo niektorych bledach nakladamy cooldown.

To chroni przed:

- mieleniem requestow na juz zly upstream
- niepotrzebnym zwiekszaniem presji na provider

## Retry policy

Retry jest per request.

Na MVP:

- maksymalnie kilka prob
- przejscie na kolejny upstream przy bledzie retriable
- bez skomplikowanej adaptacji

## Co jest retriable

- timeout
- connection error
- `429`
- `500`
- `502`
- `503`
- `504`

## Co nie jest retriable

- `400`
- `401`
- `403`
- `404`
- bledy walidacji payloadu

## Explainable routing

Kazda decyzja routingu powinna zapisac:

- deployment id
- upstream id
- provider
- account
- region
- tier
- attempt number
- decision reason
- failover reason

Przyklad `decision_reason`:

- `selected_primary_healthy`
- `selected_secondary_primary_rate_limited`
- `selected_dr_primary_circuit_open`

## Persistence stanu routingu

Na MVP:

- Redis dla shared state pomiedzy instancjami
- fallback do in-memory przy local dev

W Redis trzymamy:

- licznik porazek
- circuit state
- cooldown expiry
- optional round robin cursor

## Co poprawiamy wzgledem DIAL Core

- jawny model `provider/account/region`
- circuit breaker
- explainable decision log
- rozroznienie `rate_limited` vs `quota_exhausted`
- przewidywalny weighted round robin

## Czego nie robimy na MVP

- routing po koszcie
- routing po latency
- dynamiczny scoring ML
- cache-aware prefix routing
- tenant-aware routing

To wszystko zostaje na pozniej.

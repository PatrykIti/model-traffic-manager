[README repo](./README.md) | [_docs](./_docs/README.md)

# AGENTS.md

## Cel repo

Repo buduje prosty, dobrze obserwowalny AI traffic router dla Azure i AKS. To nie jest ogolna platforma AI. Priorytetem MVP sa `chat/completions`, `embeddings`, deployment registry, health/failover, Managed Identity, API key fallback oraz proste rate/concurrency limiting.

## Zasady nadrzedne

- Secretless by default. Dla downstreamow wspierajacych Entra ID domyslnym outbound auth jest `managed_identity`; `api_key` jest fallbackiem, a `none` tylko dla zaufanych zasobow wewnetrznych.
- Explainable routing jest obowiazkowy. Decyzja routingu musi byc mozliwa do odtworzenia i wyjasnienia.
- Minimum zaleznosci, minimum magic, exact pinning wersji.
- Async first, jawny przeplyw requestu, brak ukrywania logiki w framework magic.
- Konfiguracja jest wersjonowana z kodem i walidowana przy starcie. W MVP nie ma live editing przez API.

## Zakres MVP

W scope:
- `chat/completions`
- `embeddings`
- deployment registry
- health, failover, cooldown i circuit breaker
- `managed_identity`
- `api_key` fallback
- podstawowe rate limiting i concurrency limiting

Poza zakresem MVP:
- workspace danych i promptow
- publication/share
- runtime custom apps
- pelna warstwa MCP platform
- generic OAuth vault
- routing po koszcie, latency, ML scoring, cache-aware prefix routing i tenant-aware routing

## Architektura

- Obowiazuje Clean Architecture.
- `app/domain` zawiera tylko logike domenowa. Bez FastAPI, Redis, Azure SDK i parsera YAML.
- `app/application` zawiera use case'y, DTO i orkiestracje.
- `app/application/ports` przechowuje kontrakty do zewnetrznego swiata.
- `app/infrastructure` implementuje adaptery do YAML, Redis, Azure Identity, HTTPX i observability.
- `app/entrypoints` odpowiada tylko za HTTP/API i mapowanie bledow.
- Nie wprowadzamy ORM, relacyjnej bazy, event busa, kolejek, Celery, Kafki, `utils dump` ani ogolnego `services.py`.

## Struktura repo

Docelowa struktura repo:

```text
model-traffic-manager/
  README.md
  AGENTS.md
  pyproject.toml
  uv.lock
  docker/
  configs/
  app/
    domain/
    application/
    infrastructure/
    entrypoints/
  tests/
    unit/
    integration/
  _docs/
```

## Stack i wersje

- Python `3.12.x`
- `uv` do zarzadzania projektem, lockiem i srodowiskiem
- runtime: `fastapi`, `pydantic`, `pydantic-settings`, `httpx`, `uvicorn`, `anyio`, `azure-identity`, `azure-core`, `redis`, `structlog`, `prometheus-client`, OpenTelemetry, `pyyaml`
- dev/test: `pytest`, `pytest-asyncio`, `pytest-cov`, `respx`, `ruff`, `mypy`
- wszystkie bezposrednie zaleznosci sa pinowane exact `==x.y.z`
- `uv.lock` jest obowiazkowy i commitowany razem z `pyproject.toml`
- nie uzywamy `latest`, nie uzywamy nieprzypietych tagow obrazow bazowych
- aktualizacja bibliotek wymaga osobnego taska, odswiezenia locka, testow regresji i changelogu

## Konfiguracja i auth

- Konfiguracja MVP jest w YAML i walidowana przez Pydantic przy starcie.
- Glowne sekcje configu to `router`, `deployments`, `shared_services`.
- Konfiguracja ma byc semantyczna: operator ma widziec `provider`, `account`, `region`, `tier`, `auth mode`, `health state`.
- Kazdy upstream ma jawnie opisane `id`, `provider`, `account`, `region`, `tier`, `weight`, `endpoint`, `auth`.
- Walidacja configu jest obowiazkowa: unikalne `deployment.id`, unikalne `upstream.id` w deployment, `tier >= 0`, `weight > 0`, poprawny URL, wymagany `scope` dla `managed_identity`, wymagane `header_name` i `secret_ref` dla `api_key`.
- W MVP sa tylko trzy tryby auth: `managed_identity`, `api_key`, `none`.
- Router nie forwarduje tokenow klienta do downstreamow jako glownego mechanizmu platformowego.
- Tokeny `managed_identity` sa cache'owane in-memory per instancja pod kluczem `(auth_mode, client_id, scope)` i odswiezane przed expiry.

## Routing i failover

- Obowiazuje jedna jawna strategia MVP: `tiered_failover`.
- Znaczenie `tier` jest stale: `0` primary, `1` failover regional/account, `2` DR/last resort.
- `weight` sluzy tylko do rozkladu ruchu w obrebie tego samego tieru.
- Algorytm wyboru: odfiltruj `unhealthy`, `cooldown`, `circuit_open`; wybierz najnizszy dostepny tier; w jego obrebie uzyj weighted round robin.
- Weighted round robin jest preferowany nad weighted random ze wzgledow operacyjnych i testowalnosci.
- Upstream state musi rozrozniac co najmniej `healthy`, `rate_limited`, `quota_exhausted`, `cooldown`, `unhealthy`, `circuit_open`.
- `429` oznacza `rate_limited` i wymaga respektowania `Retry-After`, jesli jest dostepny.
- Circuit breaker per upstream jest obowiazkowy: otwarcie po serii porazek, `half-open` po czasie, sukces zamyka circuit.
- Retry policy jest per request i prosta: kilka prob, failover na kolejny upstream tylko dla retriable failure.
- Retriable sa: timeout, connection error, `429`, `500`, `502`, `503`, `504` i rozpoznane `quota_exhausted`.
- Bledy `400`, `401`, `403`, `404` i walidacja payloadu nie uruchamiaja failoveru.
- Shared routing state trzymamy w Redis; local dev moze miec fallback in-memory.

## Testy i Definition of Done

- Testy sa obowiazkowa czescia definicji done.
- Priorytet maja szybkie i deterministyczne unit testy bez prawdziwego Redis, Azure i zewnetrznych endpointow.
- Preferowane test doubles: `fake`, potem `stub`, potem `spy`, a dopiero na koncu `mock`.
- Obowiazkowe sa unit testy dla domeny, use case'ow, auth, klasyfikacji bledow i failoveru oraz minimalne integration testy adapterow i API.
- Coverage gate na start wynosi `85%` dla `app` i ma byc egzekwowany w CI.
- Minimalny check przed domknieciem zmiany:

```text
uv run ruff check .
uv run mypy app
uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=85
```

## Workflow taskow

- Zawsze dla kazdego zadania wykonywanego w repo tworzymy task w `_docs/_TASKS/`.
- Glowny, biznesowy opis pracy trafia do pliku glownego taska: `TASK-001-nazwa.md`.
- Bardziej techniczny opis, pseudokod, plan implementacji i docelowa struktura repo trafia do subtaska: `TASK-001-01-nazwa.md`.
- Jesli obszar jest zbyt duzy albo subtask robi sie zbyt obszerny, rozbijamy go dalej, np. `TASK-001-01-01-nazwa.md`.
- Dla nowych nazw uzywamy slugow ASCII z malych liter i lacznikow.
- Kazdy task, subtask i glebszy poziom musi miec sekcje `Documentation Updates Required`.
- Kazdy task, subtask i glebszy poziom musi miec status `To Do`, `In Progress` albo `Done` wraz z data dla `In Progress` i `Done`.
- W tasku glownym opisujemy przede wszystkim sens biznesowy, scope, zaleznosci i wynik.
- W subtaskach opisujemy techniczne szczegoly, pseudokod, target structure, kolejnosc wdrozenia i ryzyka.
- Przy taskach API lub security-sensitive dodajemy sekcje `Security Contract`.
- Wzorce sa w `_docs/_TASKS/EXAMPLE_TASK.md` oraz `_docs/_CHANGELOG/EXAMPLE_CHANGELOG.md`.

## Workflow dokumentacji

- Kazdy katalog dokumentacji musi miec wlasny `README.md`.
- Kazdy plik Markdown musi miec kontrolki do nawigacji do nadrzednego indeksu albo root `README.md`.
- Przy kazdym tasku trzeba zaplanowac i wykonac aktualizacje dokumentacji w `_docs/`, tak aby repo pozostalo zrozumiale funkcjonalnie i strukturalnie.
- Przy dodaniu nowego katalogu dokumentacji trzeba dodac jego `README.md` i zaktualizowac indeksy wyzej.
- Dokumentacja ma tlumaczyc nie tylko co powstaje, ale tez gdzie to bedzie w repo i jak dziala logika systemu.

## Workflow changelogu

- Po zakonczeniu taska lub zestawu taskow z jednej sesji pracy tworzymy nowy wpis w `_docs/_CHANGELOG/`.
- Wpis changelogu musi wymieniac wszystkie zamkniete ID taskow i subtaskow.
- Po dodaniu wpisu aktualizujemy indeks i kanban board w `_docs/_CHANGELOG/README.md` oraz statusy w `_docs/_TASKS/README.md`.
- Nazwa pliku changelogu ma format `{N}-{YYYY-MM-DD}-short-title.md`, gdzie `N` jest rosnace i nie jest uzywane ponownie.

## Dodatkowe zasady wykonawcze

- Kazda zmiana ma byc spojna z pseudokodem i roadmapa z `_docs/_MVP/`.
- Startup aplikacji ma ladowac YAML, walidowac go, sprawdzac unikalnosc i polityki auth przed zarejestrowaniem configu.
- Flow use case'ow ma pozostac jawny: pobranie deploymentu, health state, wybor upstreamu, auth headers, outbound call, klasyfikacja bledu, aktualizacja health/metrics, ewentualny failover.
- Jesli pojawia sie nowa regula procesu, ktorej brakuje w tym pliku, trzeba dopisac ja tutaj w ramach taska, ktory ja wprowadza.

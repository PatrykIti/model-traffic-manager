[README repo](../../README.md) | [_docs](../README.md) | [_MVP](./README.md)

# Stack i polityka wersji

## Decyzja glowna

Uzywamy:

- Python `3.12`
- `uv` do zarzadzania projektem, lockiem i srodowiskiem

Nie wybieramy Poetry na start.

## Dlaczego `uv`

Powody:

- szybki resolver i sync
- prosty model oparty o `pyproject.toml`
- `uv.lock` daje reprodukowalnosc
- dobrze nadaje sie do CI i Docker buildow
- mniej dodatkowej abstrakcji niz Poetry

## Dlaczego nie Poetry

Poetry jest sensowne, ale na MVP routera nie daje nam przewagi, a dodaje kolejna warstwe zachowan i komend.

Potrzebujemy:

- prostego locka
- prostego sync
- prostego builda

`uv` wystarcza.

## Wersja Pythona

Na start celujemy w:

- `Python 3.12.x`

Powod:

- bardzo dobra kompatybilnosc z nowoczesnym ekosystemem AI/web
- mniej ryzyka niz agresywne wejscie w najnowsza wersje bez walidacji wszystkich bibliotek

Nie robimy "floating latest Python".

## Zasada wersjonowania runtime

- `3.12.x` jest pinowane w:
  - `pyproject.toml`
  - obrazie Docker
  - CI
- zmiana na `3.13` albo wyzej wymaga osobnej walidacji i osobnego release planu

## Biblioteki runtime

Na MVP chcemy minimalny zestaw.

### API i DTO

- `fastapi`
- `pydantic`
- `pydantic-settings`

### HTTP i async runtime

- `httpx`
- `uvicorn`
- `anyio`

### Azure auth

- `azure-identity`
- `azure-core`

### Redis

- `redis`

### Observability

- `structlog`
- `prometheus-client`
- `opentelemetry-api`
- `opentelemetry-sdk`
- `opentelemetry-instrumentation-fastapi`
- `opentelemetry-instrumentation-httpx`

### Config

- `pyyaml`

## Biblioteki dev/test

- `pytest`
- `pytest-asyncio`
- `pytest-cov`
- `respx`
- `ruff`
- `mypy`

## Czego nie bierzemy na MVP

- ORM
- SQLAlchemy
- Celery
- Kafka client
- generic retry framework typu `tenacity`
- zewnetrzna biblioteka circuit breaker, jesli mozemy miec mala wlasna implementacje

Zasada:

jesli logika jest mala i domenowa, wolimy ja napisac sami zamiast sciagac ciezka zaleznosc.

## Polityka pinowania wersji

To jest krytyczne.

### Runtime dependencies

Kazda bezposrednia zaleznosc ma byc przypieta exact:

- `package == x.y.z`

### Lock file

Commitujemy:

- `uv.lock`

To jest jedyne zrodlo prawdy dla transitive dependencies.

### Brak otwartych zakresow

Nie dopuszczamy:

- `>=`
- `^`
- `~`
- `*`

w runtime dependencies.

## Polityka aktualizacji bibliotek

Biblioteki nie aktualizuja sie "przy okazji".

Zmiany robimy tylko:

- w osobnym zadaniu
- z aktualizacja locka
- z testami regresji
- z changelogiem

Przyklad procesu:

1. branch `deps/1.1.0-refresh`
2. update wybranych bibliotek
3. `uv lock`
4. testy
5. release np. `1.1.0`

## SemVer dla routera

- `1.0.0` - pierwsza stabilna wersja
- `1.0.x` - bugfixy bez zmian kontraktow
- `1.1.0` - minor z nowa funkcja lub zatwierdzonym bumpem bibliotek
- `2.0.0` - breaking changes

## Kontrola wersji kontenera

Tak samo pinujemy obraz.

Zasada:

- pinujemy obraz bazowy po digescie
- nie uzywamy "python:3.12" bez digestu
- nie uzywamy "latest"

## Narzedzia repo

Docelowo:

- `uv` do env i locka
- `ruff` do lint + format
- `mypy` do statycznej analizy
- `pytest` do testow

## Szkic `pyproject.toml`

Punkt startowy powinien wygladac mniej wiecej tak:

```toml
[project]
name = "ai-router"
version = "0.1.0"
description = "Policy-driven AI router for Azure and AKS"
requires-python = "==3.12.*"
dependencies = [
  "fastapi==X.Y.Z",
  "pydantic==X.Y.Z",
  "pydantic-settings==X.Y.Z",
  "httpx==X.Y.Z",
  "uvicorn==X.Y.Z",
  "anyio==X.Y.Z",
  "azure-identity==X.Y.Z",
  "azure-core==X.Y.Z",
  "redis==X.Y.Z",
  "structlog==X.Y.Z",
  "prometheus-client==X.Y.Z",
  "opentelemetry-api==X.Y.Z",
  "opentelemetry-sdk==X.Y.Z",
  "opentelemetry-instrumentation-fastapi==X.Y.Z",
  "opentelemetry-instrumentation-httpx==X.Y.Z",
  "pyyaml==X.Y.Z",
]

[dependency-groups]
dev = [
  "pytest==X.Y.Z",
  "pytest-asyncio==X.Y.Z",
  "pytest-cov==X.Y.Z",
  "respx==X.Y.Z",
  "ruff==X.Y.Z",
  "mypy==X.Y.Z",
]
```

`X.Y.Z` nie ma byc zakresem. To maja byc konkretne, zatwierdzone wersje wpisane przy bootstrapie repo.

## Zasada bootstrapu zaleznosci

Na etapie utworzenia repo robimy jednorazowo:

1. wybieramy zestaw bibliotek
2. sprawdzamy kompatybilnosc z Python `3.12`
3. wpisujemy exact pins do `pyproject.toml`
4. generujemy `uv.lock`
5. commitujemy oba pliki razem

Od tego momentu nie ma "samoczynnych aktualizacji".

## Przykadowy workflow narzedziowy

```text
uv sync --frozen
uv run ruff check .
uv run ruff format --check .
uv run mypy app
uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=85
```

## Zasada dla klastra

Klaster nie moze "sam" zaktualizowac zaleznosci.

To oznacza:

- wszystkie zaleznosci sa w obrazie
- obraz jest immutable
- rollout zawsze jest powiazany z konkretna wersja aplikacji

Wniosek:

nie aktualizujemy bibliotek przez restart poda, tylko przez release nowego obrazu.

## Polityka testow

Kazda zmiana ma byc weryfikowana testami.

Minimalny zestaw na MVP:

- unit testy dla domeny
- unit testy dla use case'ow
- testy adapterow z mockowaniem zaleznosci zewnetrznych
- coverage sprawdzany w CI przez `pytest-cov`

Docelowy prog startowy:

- `--cov-fail-under=85`

Potem mozemy go podniesc, ale nie schodzimy ponizej tego bez swiadomej decyzji.

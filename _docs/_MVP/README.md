[README repo](../../README.md) | [_docs](../README.md)

# MVP AI Router - indeks

Ten katalog jest zbiorem dokumentow startowych dla nowego repo z routerem AI w Pythonie.

To nie jest opis DIAL Core. To jest projekt naszego prostszego, bardziej cloud-native produktu, inspirowanego analiza z `_BUSINESS/`.

## Kolejnosc czytania

1. [BUSINESS.md](./BUSINESS.md)
   Co budujemy, dla kogo i jaki problem rozwiazujemy.
2. [ARCHITECTURE.md](./ARCHITECTURE.md)
   Clean Architecture, granice warstw, glowne komponenty i flow requestu.
3. [STACK.md](./STACK.md)
   Python, narzedzia, pakiety, polityka pinowania wersji i release management.
4. [CONFIGURATION.md](./CONFIGURATION.md)
   Docelowy model konfiguracyjny i przykladowy YAML.
5. [AUTH_MSI.md](./AUTH_MSI.md)
   Jak dziala Managed Identity / Workload Identity i kiedy uzywamy innych trybow auth.
6. [ROUTING.md](./ROUTING.md)
   Routing, tiers, health, failover, cooldown, circuit breaker, decyzje routingu.
7. [REPOSITORY_STRUCTURE.md](./REPOSITORY_STRUCTURE.md)
   Docelowa struktura repo i odpowiedzialnosc pakietow.
8. [TESTING.md](./TESTING.md)
   Strategia testow: unit testy, mockowanie, coverage i definicja done.
9. [PSEUDOCODE.md](./PSEUDOCODE.md)
   Use case'y, flow i szkielety implementacyjne.
10. [ROADMAP.md](./ROADMAP.md)
   Proponowana kolejnosc implementacji MVP.

## Zasady projektu

- najpierw router, nie cala platforma AI
- secretless by default
- Managed Identity jako first-class capability
- prosty model domenowy: deployment, upstream, provider, account, region, auth, health
- minimum zaleznosci i minimum magic
- exact pinning wersji
- jedna jawna strategia routingu na MVP
- testability by design
- obowiazkowe unit testy i kontrola coverage

## Co jest poza zakresem MVP

Na start nie budujemy:

- workspace plikow i promptow
- publication/share/invitations
- code interpretera
- generic OAuth vault
- schema-rich apps
- pelnego MCP platform layer

To wszystko mozna dolozyc pozniej, ale nie ma prawa rozbic prostoty v1.

## Relacja do `_BUSINESS`

- `_BUSINESS/` opisuje istniejace repo i luki produktowe
- `_MVP/` opisuje docelowy nowy router i jak go zbudowac

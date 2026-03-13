[README repo](../../README.md) | [_docs](../README.md) | [_MVP](./README.md)

# Business MVP

## Co budujemy

Budujemy router AI dla AKS i Azure, ktory:

- wystawia jeden stabilny endpoint do deploymentow AI
- routuje ruch miedzy wieloma kontami i regionami
- sam autoryzuje sie do uslug downstream przez Managed Identity
- daje operatorowi prostszy model konfiguracji niz DIAL Core

## Dla kogo

Produkt jest dla zespolow platformowych i AI platform teams, ktore:

- maja kilka kont Azure OpenAI / AI Foundry
- maja wiele regionow
- chca failover miedzy kontami i regionami
- nie chca trzymac sekretow w konfiguracji
- chca miec jawna decyzje routingu i observability

## Problem biznesowy

Dzisiejszy stan zwykle wyglada tak:

- wiele endpointow AI
- reczne API keys
- slaba widocznosc, dlaczego request trafil tam, gdzie trafil
- trudny failover po `429` albo awarii regionu
- konfiguracja, ktora opisuje endpointy, ale nie opisuje semantyki biznesowej

## Nasza odpowiedz

Router ma byc prosty, ale semantyczny.

Operator ma widziec:

- provider
- account
- region
- tier
- auth mode
- health state

a nie tylko surowe URL-e i parametry pomocnicze.

## Najwazniejsza przewaga produktu

### Secretless by default

Jesli downstream wspiera Entra ID, operator nie daje sekretu.

Zamiast tego:

- przypina tozsamosc do routera
- nadaje RBAC
- ustawia `scope`

Router sam robi reszte.

### Regional and account failover as first-class capability

Failover miedzy:

- regionami
- kontami AI
- wariantami upstreamow

nie jest sztuczka konfiguracyjna, tylko jawna funkcja produktu.

### Explainable routing

Kazda decyzja routingu ma byc mozliwa do wyjasnienia:

- dlaczego upstream A odpadl
- dlaczego wybrano upstream B
- czy powod byl health, quota, `429`, timeout czy policy fallback

## Zakres MVP

### W scope

- chat/completions
- embeddings
- podstawowy deployment registry
- health i failover
- Managed Identity
- API key fallback
- proste rate limiting i concurrency limiting

### Out of scope

- workspace danych
- prompt management
- publication/share
- runtime dla custom apps
- generic integration platform

## Jednozdaniowy positioning

To nie ma byc "platforma AI do wszystkiego".

To ma byc:

> bardzo dobry, dobrze obserwowalny AI traffic router dla Azure i AKS.

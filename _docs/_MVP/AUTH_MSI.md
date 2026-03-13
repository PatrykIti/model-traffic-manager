[README repo](../../README.md) | [_docs](../README.md) | [_MVP](./README.md)

# Managed Identity i outbound auth

## Cel

Auth ma byc prosty i secretless tam, gdzie to mozliwe.

Jesli downstream wspiera Microsoft Entra ID, router powinien:

- sam wykryc tozsamosc workloadu
- sam pobrac token
- sam wyslac bearer token do downstreamu

bez recznego sekretu.

## Jaki model Azure zakladamy

Dla AKS zakladamy:

- Azure Workload Identity

Nie projektujemy tego jako "identity klastra", tylko jako tozsamosc workloadu routera.

To jest bezpieczniejsze i bardziej precyzyjne.

## Tryby auth w MVP

### 1. `managed_identity`

Preferowany tryb.

Uzywany dla:

- Azure Blob
- Azure OpenAI / AI Foundry, jesli endpoint wspiera AAD
- Key Vault
- Redis z AAD
- wewnetrznych uslug chronionych przez Entra ID

### 2. `api_key`

Fallback dla downstreamow, ktore nie wspieraja Entra ID.

### 3. `none`

Dla zasobow wewnetrznych bez auth albo za innym trusted boundary.

## Jak dziala `managed_identity`

Jesli upstream ma:

```yaml
auth:
  mode: managed_identity
  scope: https://storage.azure.com/.default
```

to router:

1. tworzy `DefaultAzureCredential`
2. opcjonalnie wybiera user-assigned identity przez `client_id`
3. pobiera token dla podanego `scope`
4. cache'uje token do czasu bezpiecznego odswiezenia
5. wysyla `Authorization: Bearer ...`

## `client_id`

Pole opcjonalne.

Znaczenie:

- brak `client_id` -> domyslna identity workloadu
- ustawiony `client_id` -> konkretna user-assigned managed identity

To daje mozliwosc:

- jednej identity dla calego routera
- albo wielu dedykowanych identity do roznych klas upstreamow

## Kiedy warto miec wiele identity

Jesli chcesz odseparowac:

- odczyt Blob
- wywolania AOAI
- dostep do Key Vault
- dostep do wewnetrznych API

to mozna pozniej dodac polityke:

- jedna identity per service class
- albo jedna identity per deployment class

Ale MVP nie musi tego komplikowac. Wystarczy wsparcie dla `client_id`.

## RBAC model

To kluczowy element.

Operator przy `managed_identity` powinien robic glownie:

- przypiecie identity do routera
- nadanie RBAC dla tej identity
- ustawienie `scope` w configu

Przyklady:

- Blob: odpowiednia rola na storage account albo kontenerze
- Key Vault: odpowiednie uprawnienia do key/secrets
- AOAI/AIFoundry: odpowiednia rola na zasobie
- wewnetrzne API: aplikacja rejestrujaca audience i odpowiednia autoryzacja

## Czego nie robimy

Nie forwardujemy klientowskich tokenow do downstreamow jako glowny mechanizm platformowy.

Klient auth to jedna rzecz.

Outbound service auth routera to druga rzecz.

Te rzeczy maja byc oddzielone.

## Token cache

Potrzebujemy lokalnego cache tokenow:

- klucz: `(auth_mode, client_id, scope)`
- wartosc: token + expiry

Zasada:

- refresh przed expiry
- bez globalnego Redis cache na MVP
- cache in-memory per instancja wystarczy

## Port domenowy

Warstwa application nie moze znac Azure SDK.

Potrzebny port:

```text
TokenProvider.get_bearer_token(auth_policy) -> BearerToken
```

Implementacja Azure siedzi w infrastrukturze.

## Pseudokod

```text
if auth.mode == MANAGED_IDENTITY:
    token = token_cache.get(client_id, scope)
    if token missing or expiring:
        token = default_azure_credential.get_token(scope, client_id?)
        token_cache.put(token)
    return Authorization: Bearer token
```

## Kiedy `api_key`

Tylko gdy:

- downstream nie wspiera Entra ID
- albo integracja jest zewnetrzna i narzuca API key

`api_key` nie moze byc domyslnym modelem dla Azure-native uslug.

## Docelowa zasada produktu

> Jesli downstream wspiera Managed Identity, operator nie podaje sekretu.

To jest jedna z glownych przewag tego routera.

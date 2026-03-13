[README repo](../../README.md) | [_docs](../README.md) | [_MVP](./README.md)

# Configuration model

## Cel

Konfiguracja ma byc prostsza semantycznie niz w DIAL Core.

Operator ma czytac:

- co to za deployment
- ktory upstream jest primary
- ktory jest secondary
- jakim auth to idzie
- jaki scope dostaje token

zamiast rozszyfrowywac znaczenie surowych endpointow.

## Format

Na MVP:

- YAML
- walidowany przy starcie przez Pydantic

Nie robimy dynamicznego edytora configu ani API do zmian configu w v1.

## Glowne sekcje

- `router`
- `deployments`
- `shared_services`

## Przyklad

```yaml
router:
  instance_name: ai-router-prod
  timeout_ms: 30000
  max_attempts: 3
  retryable_status_codes: [429, 500, 502, 503, 504]
  health:
    failure_threshold: 3
    cooldown_seconds: 30
    half_open_after_seconds: 60

deployments:
  - id: gpt-4o-chat
    kind: llm
    protocol: openai_chat
    routing:
      strategy: tiered_failover
    limits:
      max_concurrency: 200
      request_rate_per_second: 50
    upstreams:
      - id: aoai-weu-primary
        provider: azure_openai
        account: aoai-prod-01
        region: westeurope
        tier: 0
        weight: 100
        endpoint: https://aoai-prod-01.openai.azure.com/openai/deployments/gpt-4o/chat/completions
        auth:
          mode: managed_identity
          scope: https://cognitiveservices.azure.com/.default
      - id: aoai-neu-secondary
        provider: azure_openai
        account: aoai-dr-01
        region: northeurope
        tier: 1
        weight: 100
        endpoint: https://aoai-dr-01.openai.azure.com/openai/deployments/gpt-4o/chat/completions
        auth:
          mode: managed_identity
          scope: https://cognitiveservices.azure.com/.default

shared_services:
  blob_storage:
    endpoint: https://mydata.blob.core.windows.net
    auth:
      mode: managed_identity
      scope: https://storage.azure.com/.default
```

## Znaczenie sekcji

## `router`

Ustawienia instancji:

- timeouty
- retry
- health policy
- metadane instancji

## `deployments`

To logiczne uslugi wystawiane klientom.

Kazdy deployment ma:

- `id`
- `kind`
- `protocol`
- `routing`
- `limits`
- `upstreams`

## `shared_services`

To zasoby wspolne, z ktorych router sam korzysta:

- blob
- key vault
- inne wewnetrzne API

## Model upstreamu

Kazdy upstream ma:

- `id`
- `provider`
- `account`
- `region`
- `tier`
- `weight`
- `endpoint`
- `auth`

To sa jawne byty domenowe, nie tylko pola techniczne.

## Model auth

Na MVP tylko:

- `managed_identity`
- `api_key`
- `none`

### `managed_identity`

Pola:

- `mode`
- `scope`
- opcjonalnie `client_id`

### `api_key`

Pola:

- `mode`
- `header_name`
- `secret_ref`

`secret_ref` ma wskazywac na sekret dostarczony przez platforme deploymentowa, nie na plain text w configu.

## Zasady walidacji

- `deployment.id` unikalne
- `upstream.id` unikalne w deployment
- `tier >= 0`
- `weight > 0`
- `endpoint` musi byc poprawnym URL
- `scope` wymagany dla `managed_identity`
- `header_name` i `secret_ref` wymagane dla `api_key`

## Czego unikamy

Nie chcemy configu, ktory:

- miesza modele, role, share, pliki i runtime w jednym miejscu
- wymaga wielu specjalnych przypadkow
- ukrywa znaczenie domenowe

## Strategia zmian configu

Na MVP:

- config jest wersjonowany z kodem
- rollout configu idzie przez release obrazu lub mounted versioned file
- brak live editing przez API

To jest bardziej przewidywalne i prostsze operacyjnie.

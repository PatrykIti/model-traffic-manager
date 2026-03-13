[Repository README](../../README.md) | [Internal docs](../README.md) | [_MVP](./README.md)

# Configuration model

## Goal

Configuration should be semantically simpler than in DIAL Core.

Operators should be able to read:

- what deployment this is
- which upstream is primary
- which upstream is secondary
- what auth mode it uses
- what token scope it receives

instead of decoding the meaning of raw endpoints.

## Format

For MVP:

- YAML
- validated at startup with Pydantic

We are not building a dynamic config editor or a config mutation API in v1.

## Main sections

- `router`
- `deployments`
- `shared_services`

## Example

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

## Section meaning

### `router`

Instance-level settings:

- timeouts
- retry policy
- health policy
- instance metadata

### `deployments`

Logical services exposed to clients.

Every deployment has:

- `id`
- `kind`
- `protocol`
- `routing`
- `limits`
- `upstreams`

### `shared_services`

Shared resources used by the router itself:

- blob storage
- key vault
- other internal services

## Upstream model

Every upstream has:

- `id`
- `provider`
- `account`
- `region`
- `tier`
- `weight`
- `endpoint`
- `auth`

These are explicit domain concepts, not just technical fields.

## Auth model

For MVP only:

- `managed_identity`
- `api_key`
- `none`

### `managed_identity`

Fields:

- `mode`
- `scope`
- optional `client_id`

### `api_key`

Fields:

- `mode`
- `header_name`
- `secret_ref`

`secret_ref` must point to a secret supplied by the deployment platform, not plain text embedded in config.

## Validation rules

- unique `deployment.id`
- unique `upstream.id` within a deployment
- `tier >= 0`
- `weight > 0`
- `endpoint` must be a valid URL
- `scope` is required for `managed_identity`
- `header_name` and `secret_ref` are required for `api_key`

## What to avoid

We do not want config that:

- mixes models, roles, shares, files, and runtime concerns in one place
- requires too many special cases
- hides domain meaning

## Config change strategy

For MVP:

- config is versioned with code
- config rollout happens through an image release or mounted versioned file
- no live editing through API

This is more predictable and operationally simpler.

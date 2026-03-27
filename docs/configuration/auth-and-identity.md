[Repository README](../../README.md) | [docs](../README.md) | [Configuration](./README.md)

# Auth and Identity

The router has two distinct auth planes:

- inbound client auth for callers of `model-traffic-manager`
- outbound upstream auth for the downstream services the router calls

## Inbound Client Auth

Current inbound auth modes are:

- `api_bearer_token`
- `entra_id`

### `api_bearer_token`

Use this when a caller should authenticate with one router-owned opaque bearer token.

Shape:

```yaml
router:
  inbound_auth:
    providers:
      - kind: api_bearer_token
        token_id: bot-system-be-token
        display_name: Bot System Backend Token
        consumer_role: bot-system-be
        secret_ref: env://ROUTER_INBOUND_API_TOKEN
```

The caller sends:

```text
Authorization: Bearer <opaque-token>
```

The router resolves the expected token through `secret_ref` and validates it with constant-time comparison.

### `entra_id`

Use this for service-to-service callers that authenticate with Microsoft Entra ID access tokens.

Shape:

```yaml
router:
  inbound_auth:
    providers:
      - kind: entra_id
        tenant_id: 11111111-1111-1111-1111-111111111111
        audiences: [api://mtm-router-api]
        applications:
          - client_app_id: 22222222-2222-2222-2222-222222222222
            display_name: Bot System Backend
            consumer_role: bot-system-be
            required_app_roles: [invoke.router]
```

Recommended Entra model:

- the router is a protected web API
- the `aud` identifies the router API app registration
- each caller has its own app registration or managed identity
- federated credentials are configured on the caller identity
- app-only authorization uses app roles and the `roles` claim

## Outbound Upstream Auth

The router supports three outbound auth modes:

- `managed_identity`
- `api_key`
- `none`

These modes apply to both deployment upstreams and eligible shared-service upstreams.

## `managed_identity`

Use this for Azure-native services and any downstream that accepts Microsoft Entra ID tokens.

Minimal shape:

```yaml
auth:
  mode: managed_identity
  scope: https://cognitiveservices.azure.com/.default
```

### Default process identity

If `client_id` is omitted, the router uses the default identity available to the running process.

That means:

- on AKS with one Workload Identity mapping, that identity is used
- on other Azure runtimes, the default managed identity available to the process is used

### Explicit identity selection

If `client_id` is present, the router asks Azure Identity for a token using that exact user-assigned identity.

Example:

```yaml
auth:
  mode: managed_identity
  scope: https://cognitiveservices.azure.com/.default
  client_id: 11111111-1111-1111-1111-111111111111
```

This is useful when:

- one identity should be used for Azure OpenAI
- another identity should be used for Storage or internal APIs
- you want least-privilege separation by downstream class

Internally the router uses `DefaultAzureCredential(managed_identity_client_id=client_id)` when `client_id` is set, and `DefaultAzureCredential()` semantics when it is omitted.

## `api_key`

Use this only when the downstream does not support Entra ID or when an integration contract requires API key auth.

Shape:

```yaml
auth:
  mode: api_key
  header_name: api-key
  secret_ref: env://THIRD_PARTY_LLM_API_KEY
```

The router resolves the secret from the referenced environment variable. The secret value is not stored in the YAML file.

## `none`

Use this only for trusted internal services where no outbound auth header should be added.

Shape:

```yaml
auth:
  mode: none
```

## Mixed-Mode Configurations

The router supports mixed auth modes in one config. For example:

- `managed_identity` for Azure OpenAI
- `api_key` for an external fallback model endpoint
- `none` for an internal platform API

## Full Example Files

Ready-to-copy example router configs:

- [auth-identity-default-managed-identity.router.yaml](../../configs/examples/auth-identity-default-managed-identity.router.yaml)
- [auth-identity-explicit-client-ids.router.yaml](../../configs/examples/auth-identity-explicit-client-ids.router.yaml)
- [auth-identity-mixed-modes.router.yaml](../../configs/examples/auth-identity-mixed-modes.router.yaml)
- [auth-inbound-api-bearer.router.yaml](../../configs/examples/auth-inbound-api-bearer.router.yaml)
- [auth-inbound-entra-id.router.yaml](../../configs/examples/auth-inbound-entra-id.router.yaml)

What each example demonstrates:

- `auth-identity-default-managed-identity.router.yaml`
  default process identity with no explicit `client_id`
- `auth-identity-explicit-client-ids.router.yaml`
  explicit user-assigned identity selection per downstream class
- `auth-identity-mixed-modes.router.yaml`
  one router config that mixes `managed_identity`, `api_key`, and `none`
- `auth-inbound-api-bearer.router.yaml`
  router-owned inbound bearer token validation
- `auth-inbound-entra-id.router.yaml`
  protected-API Entra ID inbound validation for app-only callers

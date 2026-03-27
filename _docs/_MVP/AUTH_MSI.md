[Repository README](../../README.md) | [Internal docs](../README.md) | [_MVP](./README.md)

# Managed Identity and outbound auth

## Goal

Auth should be simple and secretless whenever possible.

If a downstream supports Microsoft Entra ID, the router should:

- detect the workload identity
- acquire a token
- send the bearer token downstream

without a manually managed secret.

## Azure model we assume

For AKS we assume:

- Azure Workload Identity

We design it as workload identity for the router itself, not as generic cluster identity.

That is safer and more precise.

## Auth modes in MVP

### 1. `managed_identity`

Preferred mode.

Used for:

- Azure Blob
- Azure OpenAI / AI Foundry when the endpoint supports AAD
- Key Vault
- Redis with AAD
- internal services protected by Entra ID

### 2. `api_key`

Fallback for downstreams that do not support Entra ID.

### 3. `none`

For internal resources without auth or behind another trusted boundary.

## How `managed_identity` works

If an upstream has:

```yaml
auth:
  mode: managed_identity
  scope: https://storage.azure.com/.default
```

the router:

1. creates `DefaultAzureCredential`
2. optionally selects a user-assigned identity via `client_id`
3. acquires a token for the configured `scope`
4. caches the token until safe refresh time
5. sends `Authorization: Bearer ...`

## `client_id`

Optional field.

Meaning:

- no `client_id` -> default workload identity
- configured `client_id` -> specific user-assigned managed identity

This supports:

- one identity for the whole router
- or multiple dedicated identities for different upstream classes

## When multiple identities make sense

If you want to separate:

- Blob read access
- Azure OpenAI calls
- Key Vault access
- internal API access

then later you can add a policy such as:

- one identity per service class
- or one identity per deployment class

But MVP does not need that complexity. Support for `client_id` is enough.

## RBAC model

This is a key point.

For `managed_identity`, operators should mainly:

- attach an identity to the router
- grant RBAC to that identity
- configure the `scope`

Examples:

- Blob: correct role on the storage account or container
- Key Vault: correct permissions for keys/secrets
- Azure OpenAI / AI Foundry: correct role on the resource
- internal APIs: app registration with the right audience and authorization model

## What we do not do

We do not forward client tokens to downstreams as the default platform mechanism.

Client auth is one concern.

Router outbound service auth is another concern.

They must stay separate.

## Token cache

We need a local token cache:

- key: `(auth_mode, client_id, scope)`
- value: token + expiry

Rule:

- refresh before expiry
- no global Redis token cache for MVP
- in-memory cache per instance is enough

## Domain port

Application code must not know the Azure SDK.

Required port:

```text
TokenProvider.get_bearer_token(auth_policy) -> BearerToken
```

The Azure implementation belongs in infrastructure.

## Pseudocode

```text
if auth.mode == MANAGED_IDENTITY:
    token = token_cache.get(client_id, scope)
    if token missing or expiring:
        token = default_azure_credential.get_token(scope, client_id?)
        token_cache.put(token)
    return Authorization: Bearer token
```

## When to use `api_key`

Only when:

- the downstream does not support Entra ID
- or an external integration requires API key auth

`api_key` must not become the default model for Azure-native services.

## Product rule

> If the downstream supports Managed Identity, the operator should not provide a secret.

This is one of the main advantages of the router.

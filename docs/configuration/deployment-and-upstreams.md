[Repository README](../../README.md) | [docs](../README.md) | [Configuration](./README.md)

# Deployments and Upstreams

The router treats deployments and upstreams as explicit domain concepts.

Each deployment is expected to describe:

- its logical identifier
- protocol and kind
- routing settings
- limits
- upstream definitions

Each upstream should expose:

- `id`
- `provider`
- `account`
- `region`
- `tier`
- `weight`
- `endpoint`
- `auth`

Current validation rules already enforced by the application:

- deployment IDs must be unique
- upstream IDs must be unique inside a deployment
- `managed_identity` requires `scope`
- `api_key` requires `header_name` and `secret_ref`
- `tier` must be greater than or equal to zero
- `weight` must be greater than zero

Current API surface:

- `GET /deployments` returns the validated deployment registry as deployment summaries

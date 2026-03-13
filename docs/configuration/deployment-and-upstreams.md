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

[Repository README](../../README.md) | [docs](../README.md) | [Configuration](./README.md)

# Load Balancing

The router can already balance traffic inside the same routing tier, but only when the pool is logically safe.

## Core Rule

The router balances only inside:

- the lowest available `tier`
- and one compatible same-tier pool

This keeps balancing and failover separate:

- same-tier balancing
  for equivalent upstreams
- higher-tier fallback
  for degraded or deliberately different alternatives

## First-Stage Controls

Current first-stage controls are:

- `weight`
- `compatibility_group`
- `model_name`
- `model_version`
- `deployment_name`
- `balancing_policy`
- `warm_standby`
- `drain`
- `target_share_percent`
- `max_share_percent`

## What Each Field Means

### `compatibility_group`

Tells the router which same-tier upstreams are allowed to be balanced together.

Use it to say:
- these two `gpt-4.1` primaries are equivalent
- these two `text-embedding-3-small` deployments are equivalent

Do not use it to hide incompatible model differences.

### `weight`

Base weighted-round-robin share when no explicit target share is provided.

### `target_share_percent`

A more explicit traffic-share input than raw `weight`.

Current implementation:
- if present, it becomes the effective weight used by the selector
- active upstreams in the same pool must sum to `100`

### `max_share_percent`

Current implementation:
- acts as a safety guard against the configured effective share becoming too large
- protects against obviously over-weighted configurations

This is not yet a rolling runtime quota controller. It is a configuration-time safety guard.

### `balancing_policy`

Current supported values:

- `weighted_round_robin`
- `active_standby`

### `warm_standby`

Marks an upstream as healthy and ready, but not part of normal traffic when an active peer is available.

### `drain`

Stops new traffic from being sent to an upstream without pretending the upstream is unhealthy.

## Chat vs Embeddings

### Chat

Safe active-active patterns:

- same model, same version, different region
- same model, same version, different account
- same model, same version, different deployment copy

Different model families should usually stay in fallback tiers instead of one active balanced pool.

### Embeddings

Embeddings are stricter.

Recommended rule:
- balance only when the embedding model and vector-space contract are equivalent

In practice:
- `text-embedding-3-small` with `text-embedding-3-small`
  can share one pool
- `text-embedding-3-small` with `text-embedding-3-large`
  should not

## Commented Example Files

Ready-to-copy examples with inline comments:

- [load-balancing-chat-active-active.router.yaml](../../configs/examples/load-balancing-chat-active-active.router.yaml)
- [load-balancing-chat-active-standby-with-fallback.router.yaml](../../configs/examples/load-balancing-chat-active-standby-with-fallback.router.yaml)
- [load-balancing-embeddings-compatible-pool.router.yaml](../../configs/examples/load-balancing-embeddings-compatible-pool.router.yaml)

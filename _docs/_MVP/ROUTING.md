[Repository README](../../README.md) | [Internal docs](../README.md) | [_MVP](./README.md)

# Routing and failover

## Goal

Routing should be:

- easy to understand
- predictable
- observable
- operationally strong enough

We are not building a complicated policy engine for MVP.

## Domain model

Main model:

- `Deployment`
- `Upstream`
- `HealthState`
- `CircuitState`
- `RouteDecision`

## `tier`

We keep `tier`, but give it explicit meaning.

- `tier=0` -> primary
- `tier=1` -> regional/account failover
- `tier=2` -> DR / last resort

This is not a hidden priority. It is the official fallback hierarchy.

## `weight`

`weight` is only used for traffic distribution inside the same tier.

Do not use it for:

- cost
- health
- business priority

## Selection algorithm

For MVP:

1. select upstreams for the deployment
2. filter out `unhealthy`, `cooldown`, and `circuit_open`
3. group candidates by `tier`
4. choose the lowest available tier
5. within that tier, use weighted round robin

## Why not weighted random

Weighted round robin is more predictable operationally than random selection.

It is easier to:

- test
- predict traffic distribution
- debug

## Upstream state classes

An upstream can be:

- `healthy`
- `rate_limited`
- `quota_exhausted`
- `cooldown`
- `unhealthy`
- `circuit_open`

This is better than reducing everything to a single "failed" state.

## When we mark an upstream as unhealthy

On:

- timeout
- connection error
- `500`
- `502`
- `503`
- `504`

## When we mark an upstream as rate limited

On:

- `429`

If `Retry-After` is present, we respect it.

## When we mark an upstream as quota exhausted

When the provider or adapter signals that the problem is not temporary rate limiting but actual quota exhaustion.

For MVP this can be detected through:

- known status codes or response patterns
- adapter-specific mapping

## Circuit breaker

We need a simple circuit breaker per upstream.

### Rules

- after `N` consecutive failures, open the circuit
- after `half_open_after`, allow a single probe request
- a success closes the circuit
- a failure opens it again

## Cooldown

After `429` or selected failures, apply cooldown.

This prevents:

- repeatedly hammering a bad upstream
- adding unnecessary pressure to the provider

## Retry policy

Retry is per request.

For MVP:

- only a small number of attempts
- move to the next upstream for retriable failures
- no complex adaptive logic

## What is retriable

- timeout
- connection error
- `429`
- `500`
- `502`
- `503`
- `504`

## What is not retriable

- `400`
- `401`
- `403`
- `404`
- payload validation errors

## Explainable routing

Every routing decision should record:

- deployment ID
- upstream ID
- provider
- account
- region
- tier
- attempt number
- decision reason
- failover reason

Example `decision_reason` values:

- `selected_primary_healthy`
- `selected_secondary_primary_rate_limited`
- `selected_dr_primary_circuit_open`

## Routing state persistence

For MVP:

- Redis for shared state across instances
- in-memory fallback for local development

Store in Redis:

- failure counters
- circuit state
- cooldown expiry
- optional round robin cursor

## What we improve over DIAL Core

- explicit `provider/account/region` model
- circuit breaker
- explainable decision log
- clear distinction between `rate_limited` and `quota_exhausted`
- predictable weighted round robin

## What we do not build for MVP

- cost-based routing
- latency-based routing
- dynamic ML scoring
- cache-aware prefix routing
- tenant-aware routing

These can come later.

[Repository README](../../README.md) | [docs](../README.md) | [Routing](./README.md)

# Routing Strategy

The MVP routing strategy is `tiered_failover`.

Core rules:

- choose the lowest healthy tier
- distribute traffic inside a tier with weighted round robin
- keep routing decisions explainable

Current implementation status:

- multi-upstream tier selection is implemented
- weighted round robin is used inside the selected tier
- request-level failover can move to another eligible upstream on retriable failures
- persistent health-state filtering, cooldown, and circuit breaker behavior are still ahead

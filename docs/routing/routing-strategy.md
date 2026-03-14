[Repository README](../../README.md) | [docs](../README.md) | [Routing](./README.md)

# Routing Strategy

The MVP routing strategy is `tiered_failover`.

Core rules:

- choose the lowest healthy tier
- distribute traffic inside a tier with weighted round robin
- keep routing decisions explainable

Current implementation status:

- the full `tiered_failover` policy is not implemented yet
- the current Phase 2 path uses deterministic single-upstream selection
- the later routing phases will replace that bootstrap behavior with tier-aware weighted selection and failover

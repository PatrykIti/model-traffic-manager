[Repository README](../../README.md) | [docs](../README.md) | [Routing](./README.md)

# Routing Strategy

The MVP routing strategy is `tiered_failover`.

Core rules:

- choose the lowest healthy tier
- distribute traffic inside a tier with weighted round robin
- keep routing decisions explainable

The routing shell is not implemented yet, but the repository is being prepared specifically for this model.

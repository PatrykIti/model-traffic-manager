[Repository README](../../README.md) | [docs](../README.md) | [Reference](./README.md)

# Decision Reasons

Current routing decision reasons include:

- `selected_primary_weighted_round_robin`
- `selected_failover_tier_weighted_round_robin`
- `selected_same_tier_retry_candidate`
- `selected_higher_tier_retry_candidate`

These reasons explain which tier was selected and whether the router stayed in the same tier or moved higher during retry flow.

Future observability work should expand this catalog with emitted event examples and troubleshooting guidance.

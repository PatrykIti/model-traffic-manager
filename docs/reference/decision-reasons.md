[Repository README](../../README.md) | [docs](../README.md) | [Reference](./README.md)

# Decision Reasons

Current routing decision reasons include:

- `selected_primary_weighted_round_robin`
- `selected_failover_tier_weighted_round_robin`
- `selected_same_tier_retry_candidate`
- `selected_higher_tier_retry_candidate`

These reasons explain which tier was selected and whether the router stayed in the same tier or moved higher during retry flow.

Current runtime event types that use these reasons include:

- `route_selected`
- `health_state_updated`
- `limiter_rejected`
- `request_completed`

Key runtime event fields include:

- `request_id`
- `deployment_id`
- `endpoint_kind`
- `upstream_id`
- `selected_tier`
- `decision_reason`
- `failure_reason`
- `health_status`
- `limiter_reason`
- `status_code`

Future observability work should expand this catalog with Azure-backed validation and troubleshooting guidance.

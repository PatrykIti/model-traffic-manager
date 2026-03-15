[Repository README](../../README.md) | [docs](../README.md) | [Reference](./README.md)

# Decision Reasons

Current routing decision reasons include:

- `selected_primary_healthy`
- `selected_failover_tier`
- `selected_same_tier_retry`
- `selected_higher_tier_retry`
- `selected_half_open_probe`

These reasons explain whether the router selected a healthy primary candidate, failed over to a higher tier, retried within the same tier, or deliberately sent a half-open recovery probe.

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
- `failover_reason`
- `failure_reason`
- `health_status`
- `limiter_reason`
- `status_code`
- `rejected_candidates`

`rejected_candidates` records the upstreams filtered out before a route decision, including:

- `upstream_id`
- `provider`
- `account`
- `region`
- `tier`
- rejection `reason`

Common rejection reasons include:

- `rate_limited`
- `quota_exhausted`
- `unhealthy`
- `circuit_open`
- `half_open_waiting_probe`
- `half_open_probe_in_progress`
- `already_attempted`

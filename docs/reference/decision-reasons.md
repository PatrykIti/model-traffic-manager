[Repository README](../../README.md) | [docs](../README.md) | [Reference](./README.md)

# Decision Reasons

Current routing decision reasons include:

- `selected_primary_healthy`
- `selected_failover_tier`
- `selected_same_tier_retry`
- `selected_higher_tier_retry`
- `selected_half_open_probe`
- `selected_shared_service_single_endpoint`
- `selected_provider_managed_endpoint`

These reasons explain whether the router selected a healthy primary candidate, failed over to a higher tier, retried within the same tier, deliberately sent a half-open recovery probe, or executed a shared service through a single semantic endpoint.

Current runtime event types that use these reasons include:

- `route_selected`
- `health_state_updated`
- `limiter_rejected`
- `request_completed`

Key runtime event fields include:

- `request_id`
- `deployment_id`
- `consumer_role`
- `endpoint_kind`
- `upstream_id`
- `provider`
- `account`
- `region`
- `model_name`
- `model_version`
- `deployment_name`
- `capacity_mode`
- `auth_mode`
- `selected_tier`
- `decision_reason`
- `failover_reason`
- `failure_reason`
- `health_status`
- `limiter_reason`
- `status_code`
- `rejected_candidates`

Request-flow note:

- the current request span stores the final upstream metadata on successful and terminal responses so operators can query which upstream actually handled a request without reconstructing that answer from raw pod logs alone
- `consumer_role` lets operators group traces by the consuming backend profile behind one router config, independent of the final upstream that served the request

`rejected_candidates` records the upstreams filtered out before a route decision, including:

- `upstream_id`
- `provider`
- `account`
- `region`
- `tier`
- rejection `reason`

Common rejection reasons include:

- `cooldown_rate_limited`
- `cooldown_quota_exhausted`
- `cooldown_unhealthy`
- `warm_standby_waiting`
- `drain`
- `rate_limited`
- `quota_exhausted`
- `unhealthy`
- `circuit_open`
- `half_open_waiting_probe`
- `half_open_probe_in_progress`
- `already_attempted`

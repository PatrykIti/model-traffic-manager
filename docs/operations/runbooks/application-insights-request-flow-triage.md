[Repository README](../../../README.md) | [docs](../../README.md) | [Operations](../README.md) | [Runbooks](./README.md)

# Application Insights Request-Flow Triage

Use this runbook when operators need to understand which upstream handled a routed request or why the router failed over between upstreams.

## Symptom

- a client request succeeded but the wrong capacity pool appeared to answer it
- a `chat/completions` or `embeddings` request failed and operators need to know which upstream, tier, or failover reason was involved
- PAYG-backed and PTU-backed capacity appear to behave differently and operators need a correlated request-flow view

## Required Signals

- request correlation via `x-request-id`
- request-flow traces in Azure Monitor / Application Insights
- pod startup logs for the router topology snapshot

## Quick Checks

1. confirm that `MODEL_TRAFFIC_MANAGER_OBSERVABILITY_BACKEND=azure_monitor` is enabled on the running pod
2. confirm that the pod emitted a `router_topology_snapshot` event at startup
3. start from one of these identifiers:
   - `request_id`
   - `deployment_id`
   - `upstream_id`
   - `account`
   - `region`

## Interpretation Guide

- `router.final_upstream_id` identifies the upstream that actually served the terminal response
- `router.final_provider`, `router.final_account`, and `router.final_region` identify the support boundary for the final response path
- `router.final_capacity_mode` distinguishes explicit operator metadata such as `ptu` versus `payg` when the config defines it
- `route_selected` events on the request span show each attempt and the decision reason that led to it
- `request_completed` shows whether the request ended in success, a non-retriable response, or a retriable path that exhausted attempts

## Escalation Hints

- if the final upstream points to a PTU-backed path and failures cluster there, compare against neighboring PAYG traces for the same deployment
- if the final upstream points to a PAYG-backed path after PTU degradation, inspect the earlier `route_selected` and `health_state_updated` events for cooldown, rate limiting, quota exhaustion, or circuit-open transitions
- if the startup topology snapshot does not match the expected deployment graph, fix configuration rollout before debugging traffic behavior

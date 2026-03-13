[README repo](../../README.md) | [_docs](../README.md) | [_MVP](./README.md)

# Pseudocode

## Route chat completion

```text
use_case RouteChatCompletion(request):
    deployment = deployment_repository.get(request.deployment_id)
    if deployment is None:
        raise DeploymentNotFound

    candidates = deployment.upstreams
    states = health_repository.get_states(deployment.id)

    decision = routing_policy.select(
        deployment=deployment,
        upstreams=candidates,
        states=states,
    )

    last_error = None

    for attempt in range(1, request.max_attempts + 1):
        upstream = decision.current_upstream()

        auth_headers = auth_service.build_headers(upstream.auth)

        response = outbound_invoker.send(
            endpoint=upstream.endpoint,
            body=request.body,
            headers=auth_headers,
            timeout=deployment.timeout,
        )

        if response.success:
            health_repository.mark_success(upstream.id)
            metrics.record_success(decision, response)
            return response

        failure = failure_classifier.classify(response)
        health_repository.mark_failure(upstream.id, failure)
        metrics.record_failure(decision, failure)

        if not failure.retriable:
            raise map_failure_to_exception(failure)

        next_upstream = routing_policy.failover(decision, failure)
        if next_upstream is None:
            raise NoHealthyUpstream

        decision = decision.with_next_upstream(next_upstream)
        last_error = failure

    raise map_failure_to_exception(last_error)
```

## Build auth headers

```text
service AuthService.build_headers(auth_policy):
    if auth_policy.mode == NONE:
        return {}

    if auth_policy.mode == API_KEY:
        secret = secret_provider.get(auth_policy.secret_ref)
        return {auth_policy.header_name: secret}

    if auth_policy.mode == MANAGED_IDENTITY:
        token = token_provider.get_token(
            scope=auth_policy.scope,
            client_id=auth_policy.client_id,
        )
        return {"Authorization": f"Bearer {token.value}"}

    raise UnsupportedAuthMode
```

## Select upstream

```text
policy RoutingPolicy.select(deployment, upstreams, states):
    healthy = []

    for upstream in upstreams:
        state = states.get(upstream.id, default_healthy_state())
        if state.is_available():
            healthy.append((upstream, state))

    if not healthy:
        raise NoHealthyUpstream

    grouped = group_by_tier(healthy)
    selected_tier = min(grouped.keys())
    tier_upstreams = grouped[selected_tier]

    upstream = weighted_round_robin.pick(tier_upstreams)

    return RouteDecision(
        deployment_id=deployment.id,
        selected_tier=selected_tier,
        selected_upstream=upstream,
        reason="selected_primary_healthy" or other,
    )
```

## Classify failure

```text
classifier classify(response_or_exception):
    if exception is timeout:
        return Failure(retriable=True, reason=TIMEOUT)

    if exception is connection_error:
        return Failure(retriable=True, reason=NETWORK_ERROR)

    if status == 429:
        return Failure(retriable=True, reason=RATE_LIMITED, retry_after=header)

    if status in [500, 502, 503, 504]:
        return Failure(retriable=True, reason=UNHEALTHY)

    if response matches quota exhausted signature:
        return Failure(retriable=True, reason=QUOTA_EXHAUSTED)

    return Failure(retriable=False, reason=NON_RETRIABLE)
```

## Token provider cache

```text
provider get_token(scope, client_id):
    key = (scope, client_id)
    token = cache.get(key)

    if token exists and token.not_expiring_soon():
        return token

    token = azure_default_credential(client_id?).get_token(scope)
    cache.put(key, token)
    return token
```

## Health state update

```text
repository mark_failure(upstream_id, failure):
    state = load(upstream_id)

    if failure.reason == RATE_LIMITED:
        state.cooldown_until = now + retry_after_or_default

    if failure.reason in [TIMEOUT, NETWORK_ERROR, UNHEALTHY]:
        state.consecutive_failures += 1

    if state.consecutive_failures >= threshold:
        state.circuit = OPEN
        state.half_open_after = now + circuit_open_seconds

    save(state)
```

## Startup config load

```text
startup():
    raw = yaml_loader.load(path)
    config = pydantic_validate(raw)
    validate_unique_ids(config)
    validate_auth_policies(config)
    validate_deployments(config)
    container.register(config)
```

## Minimal HTTP entrypoint

```text
POST /v1/chat/completions/{deployment_id}
    -> parse request body
    -> call RouteChatCompletion
    -> map domain errors to HTTP
    -> return upstream response
```

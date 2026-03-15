[Repository README](../../README.md) | [docs](../README.md) | [Routing](./README.md)

# Failover and Health

The router is expected to distinguish:

- healthy
- rate limited
- quota exhausted
- cooldown
- unhealthy
- circuit open

The MVP health model includes:

- cooldown after `429`
- circuit breaker per upstream
- half-open recovery probing after the circuit-open window
- retry only for retriable failures
- observable decision reasons for failover

Current implementation status:

- request-level failover across multiple upstreams is implemented
- retriable HTTP and transport failures can move traffic to another eligible upstream
- healthy candidates are preferred over half-open recovery candidates within the same tier
- expired circuit-open windows move into a half-open recovery phase instead of immediately returning to full healthy traffic
- only one half-open probe can be active for the same upstream at a time
- `429` responses can place an upstream into a rate-limited cooldown window
- repeated retriable failures can open a per-upstream circuit
- in-memory state remains the default local mode
- Redis-backed health and limiter state is active when `MODEL_TRAFFIC_MANAGER_RUNTIME_STATE_BACKEND=redis`

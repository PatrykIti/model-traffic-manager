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
- retry only for retriable failures
- observable decision reasons for failover

Current implementation status:

- request-level failover across multiple upstreams is implemented
- retriable HTTP and transport failures can move traffic to another eligible upstream
- in-memory health-state persistence is active in the bootstrap runtime
- `429` responses can place an upstream into a rate-limited cooldown window
- repeated retriable failures can open a per-upstream circuit
- a Redis-backed health-state adapter exists for shared persistence, but the default runtime still uses in-memory state

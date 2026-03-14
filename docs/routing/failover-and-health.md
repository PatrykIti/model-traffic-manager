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
- health-state persistence, cooldown, and circuit breaker behavior are still ahead

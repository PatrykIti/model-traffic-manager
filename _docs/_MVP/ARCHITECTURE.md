[Repository README](../../README.md) | [Internal docs](../README.md) | [_MVP](./README.md)

# Architecture

## Logical architecture

We are adopting Clean Architecture.

We want to separate:

- routing domain logic
- application use cases
- infrastructure adapters
- HTTP framework concerns

so routing and auth do not depend on FastAPI, Redis, or the Azure SDK.

## Layers

### 1. Domain

The purest layer.

It contains:

- entities
- value objects
- policies
- domain services

Example types:

- `Deployment`
- `Upstream`
- `AuthPolicy`
- `RoutingPolicy`
- `HealthState`
- `CircuitState`
- `RouteDecision`
- `FailureReason`

This layer must not contain:

- HTTP
- Redis
- Azure SDK
- YAML parsing

### 2. Application

The use-case layer.

It contains:

- request orchestration
- invocation of domain policies
- calls to ports
- translation of input/output DTOs

Example use cases:

- `RouteChatCompletion`
- `RouteEmbeddings`
- `ListDeployments`
- `EvaluateCandidateUpstreams`
- `AcquireOutboundCredentials`
- `RecordUpstreamFailure`
- `RecordUpstreamSuccess`

### 3. Ports

Ports are contracts to the outside world.

Example ports:

- `DeploymentRepository`
- `HealthRepository`
- `TokenProvider`
- `OutboundInvoker`
- `RateLimiterPort`
- `MetricsPort`
- `TracerPort`
- `ClockPort`

This model is also necessary for testing:

- use cases are tested with mocked or fake ports
- domain logic is tested without infrastructure
- adapters are tested separately with contract-style checks

### 4. Infrastructure / Adapters

Implementations of the ports.

Examples:

- YAML config repository
- Redis health repository
- Azure MSI token provider
- HTTPX outbound invoker
- Prometheus adapter
- OpenTelemetry adapter

### 5. Entrypoints

Framework and API.

For MVP:

- FastAPI
- request/response DTO mapping
- domain-to-HTTP error mapping

## Bounded contexts in MVP

We are not building multiple microservices. We are building one service with logical contexts:

- Routing
- Outbound Auth
- Health and Failover
- Config Loading
- Observability

## Main request flow

1. Client calls a deployment endpoint.
2. Entrypoint maps the request into a use case.
3. The use case loads the deployment definition.
4. The use case loads upstream health state.
5. Domain logic selects the best candidate.
6. Application asks `TokenProvider` for outbound auth.
7. `OutboundInvoker` sends the request.
8. The result updates health state and metrics.
9. The response is returned to the client.

## Error model

We do not want every error to become a generic `500`.

Basic error classes:

- `DeploymentNotFound`
- `NoHealthyUpstream`
- `UpstreamRateLimited`
- `UpstreamQuotaExhausted`
- `AuthAcquisitionFailed`
- `OutboundTimeout`
- `OutboundConnectionError`
- `ConfigValidationError`

## Runtime components

Minimal component set:

- API process
- config loader
- Redis connection
- outbound HTTP client pool
- token cache
- metrics endpoint

## Durable vs ephemeral data

### Durable data

For MVP:

- configuration stored in the repo and image
- optionally a mounted versioned config file

### Ephemeral data

In Redis:

- circuit breaker state
- cooldown windows after failures
- rate limit counters
- optional distributed health state

## What we intentionally avoid

Do not introduce:

- ORM
- relational database
- event bus
- queues

They are not needed for the MVP router.

## Responsibility diagram

```text
FastAPI -> Application Use Case -> Domain Policy
                              -> Ports
                              -> Infrastructure Adapters
```

## Additional architectural decisions

- async first
- no hidden flow inside framework magic
- domain logic tested without infrastructure
- adapters tested with contract-style checks
- config validated at startup
- no dynamic self-mutation of config in v1
- every use case must have unit tests

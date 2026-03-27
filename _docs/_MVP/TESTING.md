[Repository README](../../README.md) | [Internal docs](../README.md) | [_MVP](./README.md)

# Testing strategy

## Main rule

Everything must be tested in a way that proves it works before deployment.

For MVP, tests are not optional. They are part of the definition of done.

## Mandatory coverage

- unit tests for domain logic
- unit tests for use cases
- unit tests for auth logic
- unit tests for failure classification and failover
- minimum integration coverage for adapters and API
- coverage tracked through `pytest-cov`

## Testing priority

### 1. Unit tests

This should be the main test type.

Test:

- routing policy
- upstream selection
- tier fallback
- circuit breaker
- cooldown after `429`
- failure classification
- token cache
- auth header mapping
- use case orchestration

Unit tests must be:

- fast
- deterministic
- free of real Redis
- free of real Azure
- free of real external endpoints

### 2. Integration tests

Only enough to confirm adapters are wired correctly:

- FastAPI endpoints
- Redis repository
- HTTPX invoker
- MSI token provider through a controlled stub/mock

### 3. End-to-end tests

Not required at the very start of MVP.

They can be added later once the first staging deployment exists.

## How we mock

Mocking must respect Clean Architecture.

Mock ports first, not framework internals or private implementation details.

### Mocked elements

- `DeploymentRepository`
- `HealthRepository`
- `TokenProvider`
- `OutboundInvoker`
- `RateLimiterPort`
- `ClockPort`
- `MetricsPort`

### Preferred test doubles

Order of preference:

1. fake
2. stub
3. spy
4. mock

If a fake or stub is enough, do not reach for aggressive mocking.

## What tests must prove

### Routing

- selects the lowest healthy tier
- does not select upstreams in cooldown
- does not select upstreams with `circuit_open`
- falls back to the next tier when primary is unavailable
- preserves weighted round robin inside the same tier

### Failover

- retriable errors move to the next attempt
- non-retriable errors do not trigger failover
- `429` sets cooldown
- repeated `5xx` opens the circuit
- half-open allows recovery probing

### Auth

- `managed_identity` acquires a token for the correct `scope`
- `managed_identity` uses `client_id` when configured
- token cache does not reacquire tokens unnecessarily
- `api_key` returns the correct header
- `none` adds no auth headers

### API

- correct mapping from domain errors to HTTP
- correct forwarding of payload to the use case
- correct return of upstream response without breaking the contract

## Coverage

Initial requirement:

- `pytest --cov=app --cov-report=term-missing --cov-fail-under=85`

This is the minimum bar for MVP.

Later, once the project stabilizes, the gate can be raised to something like `90`.

## Coverage policy

Coverage is not the goal by itself.

But:

- missing coverage means we do not know what is untested
- a coverage gate protects against test erosion

So coverage must be a CI gate.

## Definition of Done for every change

A change is done when:

- it has unit tests for new logic
- it does not break existing tests
- it passes the coverage gate
- it passes lint and type-check

Minimum check:

```text
uv run ruff check .
uv run mypy app
uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=85
```

## What we do not do

- do not rely only on manual testing
- do not create sleep-driven flaky tests
- do not require real Azure in unit CI
- do not blindly mock framework magic

## Most important rule

> Routing and auth logic must be provable with unit tests.

Without that, the router quickly becomes hard to trust operationally.

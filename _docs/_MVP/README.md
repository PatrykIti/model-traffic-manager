[Repository README](../../README.md) | [Internal docs](../README.md)

# AI Router MVP Index

This directory contains the bootstrap documentation for the new Python repository that will host the AI router.

It is not a description of DIAL Core. It describes our smaller, more cloud-native product inspired by the gaps identified in the business analysis.

## Recommended reading order

1. [BUSINESS.md](./BUSINESS.md)
   What we are building, for whom, and what problem we are solving.
2. [ARCHITECTURE.md](./ARCHITECTURE.md)
   Clean Architecture, layer boundaries, main components, and request flow.
3. [STACK.md](./STACK.md)
   Python stack, tooling, dependency pinning policy, and release management.
4. [CONFIGURATION.md](./CONFIGURATION.md)
   Target configuration model and sample YAML.
5. [AUTH_MSI.md](./AUTH_MSI.md)
   Managed Identity / Workload Identity and fallback auth modes.
6. [ROUTING.md](./ROUTING.md)
   Routing tiers, health, failover, cooldown, circuit breaker, and routing decisions.
7. [REPOSITORY_STRUCTURE.md](./REPOSITORY_STRUCTURE.md)
   Target repository layout and package ownership.
8. [TESTING.md](./TESTING.md)
   Testing strategy, mocking model, coverage, and definition of done.
9. [PSEUDOCODE.md](./PSEUDOCODE.md)
   Use cases, flows, and implementation skeletons.
10. [ROADMAP.md](./ROADMAP.md)
    Proposed implementation sequence for the MVP.

## Project rules

- router first, not a full AI platform
- secretless by default
- Managed Identity as a first-class capability
- simple domain model: deployment, upstream, provider, account, region, auth, health
- minimal dependencies and minimal magic
- exact version pinning
- one explicit routing strategy for MVP
- testability by design
- mandatory unit tests and coverage control

## Outside MVP scope

Do not build these features at the start:

- file and prompt workspace
- publication/share/invitations
- code interpreter
- generic OAuth vault
- schema-rich apps
- full MCP platform layer

They can be added later, but they must not break the simplicity of v1.

## Relation to `_BUSINESS`

- `_BUSINESS/` describes the current-state repo and product gaps
- `_MVP/` describes the target router and how to build it

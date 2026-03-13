[Repository README](../../README.md) | [Internal docs](../README.md) | [_MVP](./README.md)

# Business MVP

## What we are building

We are building an AI router for AKS and Azure that:

- exposes one stable endpoint for AI deployments
- routes traffic across multiple accounts and regions
- authenticates to downstream services through Managed Identity
- gives operators a simpler configuration model than DIAL Core

## Who it is for

The product is for platform teams and AI platform teams that:

- operate several Azure OpenAI / Azure AI accounts
- work across multiple regions
- need failover across accounts and regions
- do not want to manage secrets in configuration
- need explicit routing decisions and observability

## Business problem

The current situation usually looks like this:

- many AI endpoints
- manual API keys
- poor visibility into why a request went to a given target
- difficult failover after `429` or a regional outage
- configuration that describes endpoints but not business meaning

## Our answer

The router should be simple but semantic.

Operators should see:

- provider
- account
- region
- tier
- auth mode
- health state

instead of raw URLs and opaque helper parameters.

## Main product advantage

### Secretless by default

If a downstream supports Entra ID, the operator should not provide a secret.

Instead, the operator:

- assigns an identity to the router
- grants RBAC to that identity
- sets the `scope`

The router does the rest.

### Regional and account failover as a first-class capability

Failover across:

- regions
- AI accounts
- upstream variants

is a product feature, not a configuration trick.

### Explainable routing

Every routing decision must be explainable:

- why upstream A was rejected
- why upstream B was selected
- whether the reason was health, quota, `429`, timeout, or policy fallback

## MVP scope

### In scope

- chat/completions
- embeddings
- basic deployment registry
- health and failover
- Managed Identity
- API key fallback
- basic rate limiting and concurrency limiting

### Out of scope

- data workspace
- prompt management
- publication/share
- runtime for custom apps
- generic integration platform

## One-sentence positioning

This should not become "an AI platform for everything".

It should become:

> a very good, highly observable AI traffic router for Azure and AKS

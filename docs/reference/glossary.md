[Repository README](../../README.md) | [docs](../README.md) | [Reference](./README.md)

# Glossary

- **deployment**: a logical router-facing service exposed to clients
- **upstream**: a concrete downstream endpoint candidate
- **auth policy**: the outbound authentication contract attached to an upstream
- **tier**: the explicit failover priority level
- **cooldown**: temporary avoidance window after rate limiting or selected failures
- **circuit open**: upstream protection state that blocks selection until probe time
- **deployment registry**: the validated set of deployments loaded from router configuration
- **shared service**: a non-LLM service described in router configuration for backend access, metadata exposure, or router-mediated execution
- **inbound client auth**: the authentication layer used by callers of `model-traffic-manager`
- **app role**: an Entra ID application permission exposed by the router API app and assigned to calling service principals
- **federated credential**: an Entra trust that lets an external OIDC workload obtain tokens without client secrets
- **direct backend access**: a shared-service mode where the router stores metadata but does not proxy execution
- **router proxy**: a shared-service mode where the backend calls the service through the router
- **provider-managed availability**: a shared-service assumption that the service or provider owns the availability model instead of router-managed multi-upstream failover

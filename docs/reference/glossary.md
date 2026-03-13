[Repository README](../../README.md) | [docs](../README.md) | [Reference](./README.md)

# Glossary

- **deployment**: a logical router-facing service exposed to clients
- **upstream**: a concrete downstream endpoint candidate
- **auth policy**: the outbound authentication contract attached to an upstream
- **tier**: the explicit failover priority level
- **cooldown**: temporary avoidance window after rate limiting or selected failures
- **circuit open**: upstream protection state that blocks selection until probe time
- **deployment registry**: the validated set of deployments loaded from router configuration

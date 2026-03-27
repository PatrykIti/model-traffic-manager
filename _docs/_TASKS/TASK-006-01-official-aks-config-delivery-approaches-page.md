[Repository README](../../README.md) | [Internal docs](../README.md) | [_TASKS](./README.md)

# TASK-006-01: Official AKS Config Delivery Approaches Page
# FileName: TASK-006-01-official-aks-config-delivery-approaches-page.md

**Priority:** High
**Category:** Official Documentation
**Estimated Effort:** Small
**Dependencies:** TASK-006
**Status:** **Done** (2026-03-13)

---

## Overview

Create the official documentation page that compares three AKS approaches for providing router config to the application.

Scope:
- mounted Kubernetes Secret as a file
- Kubernetes Secret injected as environment variable
- ConfigMap for config plus Secret for actual secret material

---

## Pseudocode

```text
document_aks_config_delivery():
    explain current runtime contract
    describe three AKS delivery approaches
    mark one as recommended for current code
    explain trade-offs and operational caveats
```

---

## Testing Requirements

- the page clearly states that the current code reads config from a file path
- the page clearly states that env-var YAML would require additional implementation
- the page clearly separates configuration material from true secrets

---

## Documentation Updates Required

- `docs/operations/aks-configuration-delivery.md`
- `docs/operations/README.md`
- `docs/operations/deployment-model.md`
- `docs/configuration/configuration-model.md`

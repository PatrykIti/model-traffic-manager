[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# Filename: 6-2026-03-13-aks-configuration-delivery-approaches.md

# 6. AKS Configuration Delivery Approaches Documentation

**Date:** 2026-03-13
**Version:** 0.1.0
**Tasks:** TASK-006, TASK-006-01

## Key Changes

### Official docs
- Added an AKS-focused documentation page that compares three ways to deliver router config to the application.
- Documented mounted Kubernetes Secret as a file, full YAML via environment variable, and ConfigMap plus Secret split.

### Guidance
- Clarified that the current code already supports file-based config delivery through `MODEL_TRAFFIC_MANAGER_CONFIG_PATH`.
- Clarified that full YAML via a single environment variable would require additional application support.
- Added a recommendation for the current codebase and a longer-term recommendation for separating config from true secret material.

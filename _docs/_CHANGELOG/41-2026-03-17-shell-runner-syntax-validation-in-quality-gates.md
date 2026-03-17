[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 41: Shell Runner Syntax Validation in Quality Gates

**Date:** 2026-03-17
**Version:** 0.1.0
**Tasks:**
- TASK-036

---

## Key Changes

### Quality Gates

- added explicit shell-syntax validation to the repository `Makefile`
- extended the shared pre-commit quality gate so tracked `.sh` files are syntax-checked automatically

### Runner Hardening

- simplified GHCR credential resolution in the Azure/AKS runner to avoid fragile nested shell expansion
- kept the live runner flow functionally unchanged while making the script easier to parse and maintain

### Documentation

- updated root and local-development docs so the stronger release gate is visible

[Repository README](../../README.md) | [Internal docs](../README.md) | [_CHANGELOG](./README.md)

# 62: Observability Live Suite Log Capture and Query Hardening

**Date:** 2026-03-26
**Version:** 0.1.0
**Tasks:**
- TASK-045

---

## Key Changes

### Log Capture

- make-driven local test targets now tee output into stable files under `/tmp/mtm-local-logs`
- the shared Azure/AKS runner now writes a `suite-run.log` plus `pytest.log` into the suite artifact directory

### Observability Query Hardening

- inbound request spans are now created as `SERVER` spans and outbound upstream spans as `CLIENT` spans, improving Azure Monitor mapping
- the live observability test now falls back from `requests` to `traces` when querying Application Insights
- startup-log inspection now reads the full deployment log instead of a short tail

### Log Noise Reduction

- Azure SDK HTTP pipeline logging is now forced down to `WARNING` to reduce console spam during live observability runs

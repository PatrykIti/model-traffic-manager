[Repository README](../../../README.md) | [docs](../../README.md) | [Operations](../README.md) | [Runbooks](./README.md)

# Storage Fixture and Cleanup Failures

## Symptom

- storage fixture fails during apply with:
  - `KeyBasedAuthenticationNotPermitted`
- destroy leaves behind partial resources
- artifact bundle shows `cleanup_failed`

## Likely Cause

- storage-module behavior conflicts with the selected account settings
- cleanup failed after only part of the suite was provisioned
- janitor filters or ownership tags were missing or inconsistent

## Quick Checks

- inspect:
  - `manifest.json`
  - `cleanup-report.json`
  - `terraform-outputs.json`
- inspect resource-group tags in Azure

## Fix

- use the fixture configuration known to work with the selected storage module behavior
- confirm expected ownership tags:
  - `codex-repo`
  - `codex-scope`
  - `codex-environment`
  - `codex-run-id`
  - `codex-suite`
  - `codex-temporary`
  - `created_on`
  - `expires_on`
- if destroy failed, use the janitor or a targeted manual cleanup after ownership is confirmed

## Safe To Rerun

- rerun only after confirming cleanup state and ownership tags

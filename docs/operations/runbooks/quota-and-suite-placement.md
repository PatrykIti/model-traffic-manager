[Repository README](../../../README.md) | [docs](../../README.md) | [Operations](../README.md) | [Runbooks](./README.md)

# Quota and Suite Placement

## Symptom

- AKS apply fails with:
  - `ErrCode_InsufficientVCPUQuota`
  - `QuotaExceeded`
  - `OperationNotAllowed`

## Likely Cause

- the selected VM family has no remaining vCPU quota in the target region
- rollout surge would require extra quota beyond nominal node size
- the suite is assigned to the wrong region or family for the current subscription

## Quick Checks

- confirm the suite placement in `infra/<scope>/env/<environment>.tfvars`
- confirm the region and VM family quotas in Azure
- remember that rollout surge can temporarily increase vCPU demand

## Fix

- use the documented suite placement matrix from the official docs
- adjust the per-suite `env/<environment>.tfvars`, not global shared defaults
- if needed, move the suite to the other region or to the other allowed VM family

## Safe To Rerun

- yes, after the suite placement or quota assignment is corrected

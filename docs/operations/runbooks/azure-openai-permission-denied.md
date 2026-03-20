[Repository README](../../../README.md) | [docs](../../README.md) | [Operations](../README.md) | [Runbooks](./README.md)

# Azure OpenAI Permission Denied

## Symptom

- `401` with:
  - `{"error":{"code":"PermissionDenied","message":"Principal does not have access to API/Operation."}}`
- or role-assignment creation fails with:
  - `UnmatchedPrincipalType`

## Likely Cause

- the executing principal does not have `Cognitive Services OpenAI User` on the Azure OpenAI account
- or the role assignment was created with the wrong `principal_type`
- or role-assignment propagation is still catching up after apply

## Quick Checks

```bash
az role assignment list \
  --scope "$OPENAI_ACCOUNT_ID" \
  --query "[].{principalId:principalId, role:roleDefinitionName, principalType:principalType}" \
  -o table
```

## Fix

- ensure the executor principal is assigned `Cognitive Services OpenAI User`
- do not force `principal_type=ServicePrincipal` when the executor is actually a `User`
- rerun after short propagation delay if the role assignment was just created

## Safe To Rerun

- yes, after the role assignment is corrected or propagation time has passed

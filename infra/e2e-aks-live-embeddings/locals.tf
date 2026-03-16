locals {
  scope_key           = "e2e-aks-live-embeddings"
  base_name           = lower(substr("${var.environment}-${local.scope_key}-${var.name_prefix}-${var.run_id}", 0, 42))
  resource_group_name = substr("${local.base_name}-rg", 0, 90)
  node_resource_group_name = substr(
    "nrg-${var.environment}-${local.scope_key}-${var.name_prefix}-${var.run_id}",
    0,
    80,
  )
  identity_name = substr("${local.base_name}-uai", 0, 64)
  aks_name      = substr("${local.base_name}-aks", 0, 63)
  dns_prefix    = substr(replace("${var.environment}${var.name_prefix}${var.run_id}", "-", ""), 0, 40)

  openai_account_name = substr(
    replace("${var.environment}${var.name_prefix}${var.run_id}oaiemb", "-", ""),
    0,
    24,
  )
  openai_subdomain_name = coalesce(var.openai_custom_subdomain_name, local.openai_account_name)

  enabled_openai_embedding_deployments = [
    for deployment in var.openai_embedding_deployments : deployment
    if try(deployment.enabled, true)
  ]

  common_tags = merge(var.tags, {
    "codex-repo"        = "model-traffic-manager"
    "codex-scope"       = local.scope_key
    "codex-environment" = var.environment
    "codex-run-id"      = var.run_id
  })
}

locals {
  scope_key           = "integration-azure"
  base_name           = lower(substr("${var.environment}-${local.scope_key}-${var.name_prefix}-${var.run_id}", 0, 42))
  resource_group_name = substr("${local.base_name}-rg", 0, 90)
  identity_name       = substr("${local.base_name}-uai", 0, 64)
  created_on          = timestamp()
  expires_on          = timeadd(timestamp(), "${var.ttl_hours}h")

  common_tags = merge(var.tags, {
    "codex-repo"        = "model-traffic-manager"
    "codex-scope"       = local.scope_key
    "codex-environment" = var.environment
    "codex-run-id"      = var.run_id
    "codex-suite"       = local.scope_key
    "codex-temporary"   = "true"
    "created_on"        = local.created_on
    "expires_on"        = local.expires_on
  })
}

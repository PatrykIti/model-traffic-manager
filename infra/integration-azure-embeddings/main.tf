resource "azurerm_resource_group" "test" {
  name     = local.resource_group_name
  location = var.location
  tags     = local.common_tags
}

module "router_identity" {
  source = "git::https://github.com/PatrykIti/azurerm-terraform-modules//modules/azurerm_user_assigned_identity?ref=UAIv1.0.0"

  name                = local.identity_name
  resource_group_name = azurerm_resource_group.test.name
  location            = azurerm_resource_group.test.location
  tags                = local.common_tags
}

module "openai_account" {
  source = "git::https://github.com/PatrykIti/azurerm-terraform-modules//modules/azurerm_cognitive_account?ref=COGv1.0.0"

  name                            = local.openai_account_name
  resource_group_name             = azurerm_resource_group.test.name
  location                        = var.openai_location
  kind                            = "OpenAI"
  sku_name                        = "S0"
  custom_subdomain_name           = local.openai_subdomain_name
  public_network_access_enabled   = true
  local_auth_enabled              = false
  outbound_network_access_restricted = false

  deployments = [
    for deployment in local.enabled_openai_embedding_deployments : {
      name = deployment.azure_deployment_name
      model = {
        format  = "OpenAI"
        name    = deployment.model_name
        version = deployment.model_version
      }
      sku = {
        name     = deployment.sku_name
        capacity = deployment.capacity
      }
      version_upgrade_option = "NoAutoUpgrade"
    }
  ]

  tags = local.common_tags
}

module "openai_role_assignment" {
  source = "git::https://github.com/PatrykIti/azurerm-terraform-modules//modules/azurerm_role_assignment?ref=RAv1.0.0"

  scope                = module.openai_account.id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = module.router_identity.principal_id
  principal_type       = "ServicePrincipal"
  description          = "Allow the router user-assigned identity to invoke Azure OpenAI embeddings."
}

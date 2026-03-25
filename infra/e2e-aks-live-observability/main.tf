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

module "aks_cluster" {
  source = "git::https://github.com/PatrykIti/azurerm-terraform-modules//modules/azurerm_kubernetes_cluster?ref=AKSv2.1.0"

  name                = local.aks_name
  resource_group_name = azurerm_resource_group.test.name
  location            = azurerm_resource_group.test.location
  node_resource_group = local.node_resource_group_name

  dns_config = {
    dns_prefix = local.dns_prefix
  }

  kubernetes_config = {
    kubernetes_version = var.kubernetes_version
  }

  sku_config = {
    sku_tier = "Free"
  }

  identity = {
    type         = "SystemAssigned"
    identity_ids = null
  }

  default_node_pool = {
    name                 = "system"
    node_count           = 1
    vm_size              = var.aks_node_vm_size
    auto_scaling_enabled = false
    os_disk_size_gb      = 30
    upgrade_settings = {
      max_surge = "33%"
    }
  }

  network_profile = {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }

  features = {
    workload_identity_enabled = true
    oidc_issuer_enabled       = true
  }

  tags = local.common_tags
}

module "openai_account" {
  source = "git::https://github.com/PatrykIti/azurerm-terraform-modules//modules/azurerm_cognitive_account?ref=COGv1.0.0"

  name                        = local.openai_account_name
  resource_group_name         = azurerm_resource_group.test.name
  location                    = var.openai_location
  kind                        = "OpenAI"
  sku_name                    = "S0"
  custom_subdomain_name       = local.openai_subdomain_name
  public_network_access_enabled = true
  local_auth_enabled          = false
  outbound_network_access_restricted = false

  deployments = [
    for deployment in local.enabled_observability_deployments : {
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
  description          = "Allow the router user-assigned identity to invoke Azure OpenAI."
}

module "log_analytics_workspace" {
  source = "git::https://github.com/PatrykIti/azurerm-terraform-modules//modules/azurerm_log_analytics_workspace?ref=LAWv1.1.0"

  name                = local.log_analytics_name
  resource_group_name = azurerm_resource_group.test.name
  location            = azurerm_resource_group.test.location
  workspace = {
    sku               = var.log_analytics_workspace.sku
    retention_in_days = var.log_analytics_workspace.retention_in_days
  }
  tags = local.common_tags
}

module "application_insights" {
  source = "git::https://github.com/PatrykIti/azurerm-terraform-modules//modules/azurerm_application_insights?ref=APPINSv1.1.0"

  name                = local.application_insights_name
  resource_group_name = azurerm_resource_group.test.name
  location            = azurerm_resource_group.test.location
  workspace_id        = module.log_analytics_workspace.id
  application_type    = var.application_insights.application_type
  sampling_percentage = var.application_insights.sampling_percentage
  tags                = local.common_tags
}

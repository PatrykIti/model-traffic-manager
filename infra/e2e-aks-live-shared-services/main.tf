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

module "archive_storage_account" {
  source = "git::https://github.com/PatrykIti/azurerm-terraform-modules//modules/azurerm_storage_account?ref=SAv2.1.0"

  name                     = local.storage_account_name
  resource_group_name      = azurerm_resource_group.test.name
  location                 = azurerm_resource_group.test.location
  account_replication_type = var.storage_account_replication_type
  tags                     = local.common_tags

  security_settings = {
    shared_access_key_enabled     = false
    public_network_access_enabled = true
  }

  default_to_oauth_authentication = true
}

module "archive_storage_role_assignment" {
  source = "git::https://github.com/PatrykIti/azurerm-terraform-modules//modules/azurerm_role_assignment?ref=RAv1.0.0"

  scope                = module.archive_storage_account.id
  role_definition_name = "Storage Blob Data Contributor"
  principal_id         = module.router_identity.principal_id
  principal_type       = "ServicePrincipal"
  description          = "Allow the router user-assigned identity to access the shared archive storage account."
}

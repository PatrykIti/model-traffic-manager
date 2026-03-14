resource "azurerm_resource_group" "test" {
  name     = local.resource_group_name
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_user_assigned_identity" "router" {
  name                = local.identity_name
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name
  tags                = local.common_tags
}

resource "azurerm_kubernetes_cluster" "e2e" {
  count = var.test_level == "e2e-aks" ? 1 : 0

  name                = local.aks_name
  location            = azurerm_resource_group.test.location
  resource_group_name = azurerm_resource_group.test.name
  dns_prefix          = local.dns_prefix
  kubernetes_version  = var.kubernetes_version
  sku_tier            = "Free"

  oidc_issuer_enabled       = true
  workload_identity_enabled = true

  default_node_pool {
    name                 = "system"
    node_count           = 1
    vm_size              = var.aks_node_vm_size
    auto_scaling_enabled = false
    os_disk_size_gb      = 30
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin    = "azure"
    load_balancer_sku = "standard"
  }

  tags = local.common_tags
}

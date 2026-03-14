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

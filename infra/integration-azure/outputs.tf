output "environment" {
  value = var.environment
}

output "resource_group_name" {
  value = azurerm_resource_group.test.name
}

output "location" {
  value = azurerm_resource_group.test.location
}

output "user_assigned_identity_name" {
  value = module.router_identity.name
}

output "user_assigned_identity_client_id" {
  value = module.router_identity.client_id
}

output "user_assigned_identity_principal_id" {
  value = module.router_identity.principal_id
}

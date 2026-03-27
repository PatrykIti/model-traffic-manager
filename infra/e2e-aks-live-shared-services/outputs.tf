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

output "aks_cluster_name" {
  value = module.aks_cluster.name
}

output "aks_oidc_issuer_url" {
  value = module.aks_cluster.oidc_issuer_url
}

output "conversation_archive_blob_endpoint" {
  value = module.archive_storage_account.primary_blob_endpoint
}

output "conversation_archive_storage_account_id" {
  value = module.archive_storage_account.id
}

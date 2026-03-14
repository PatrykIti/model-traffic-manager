output "resource_group_name" {
  value = azurerm_resource_group.test.name
}

output "location" {
  value = azurerm_resource_group.test.location
}

output "user_assigned_identity_name" {
  value = azurerm_user_assigned_identity.router.name
}

output "user_assigned_identity_client_id" {
  value = azurerm_user_assigned_identity.router.client_id
}

output "user_assigned_identity_principal_id" {
  value = azurerm_user_assigned_identity.router.principal_id
}

output "aks_cluster_name" {
  value = length(azurerm_kubernetes_cluster.e2e) > 0 ? azurerm_kubernetes_cluster.e2e[0].name : null
}

output "aks_oidc_issuer_url" {
  value = length(azurerm_kubernetes_cluster.e2e) > 0 ? azurerm_kubernetes_cluster.e2e[0].oidc_issuer_url : null
}

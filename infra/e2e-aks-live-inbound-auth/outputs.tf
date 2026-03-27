output "environment" {
  value = var.environment
}

output "resource_group_name" {
  value = azurerm_resource_group.test.name
}

output "location" {
  value = azurerm_resource_group.test.location
}

output "router_identity_name" {
  value = module.router_identity.name
}

output "user_assigned_identity_name" {
  value = module.router_identity.name
}

output "router_identity_client_id" {
  value = module.router_identity.client_id
}

output "user_assigned_identity_client_id" {
  value = module.router_identity.client_id
}

output "router_identity_principal_id" {
  value = module.router_identity.principal_id
}

output "user_assigned_identity_principal_id" {
  value = module.router_identity.principal_id
}

output "caller_identity_name" {
  value = module.caller_identity.name
}

output "caller_identity_client_id" {
  value = module.caller_identity.client_id
}

output "caller_identity_principal_id" {
  value = module.caller_identity.principal_id
}

output "aks_cluster_name" {
  value = module.aks_cluster.name
}

output "aks_oidc_issuer_url" {
  value = module.aks_cluster.oidc_issuer_url
}

output "openai_account_endpoint" {
  value = module.openai_account.endpoint
}

output "openai_account_id" {
  value = module.openai_account.id
}

output "router_auth_deployments" {
  value = {
    for deployment in local.enabled_auth_deployments :
    deployment.router_deployment_id => {
      azure_deployment_name = deployment.azure_deployment_name
      model_name            = deployment.model_name
      model_version         = deployment.model_version
    }
  }
}

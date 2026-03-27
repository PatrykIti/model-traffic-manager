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

output "openai_account_endpoint" {
  value = module.openai_account.endpoint
}

output "openai_account_id" {
  value = module.openai_account.id
}

output "log_analytics_workspace_name" {
  value = module.log_analytics_workspace.name
}

output "log_analytics_workspace_id" {
  value = module.log_analytics_workspace.id
}

output "log_analytics_workspace_customer_id" {
  value = module.log_analytics_workspace.workspace_id
}

output "application_insights_name" {
  value = module.application_insights.name
}

output "application_insights_app_id" {
  value = module.application_insights.app_id
}

output "application_insights_id" {
  value = module.application_insights.id
}

output "router_observability_deployments" {
  value = {
    for deployment in local.enabled_observability_deployments :
    deployment.router_deployment_id => {
      azure_deployment_name = deployment.azure_deployment_name
      consumer_role         = deployment.consumer_role
      model_name            = deployment.model_name
      model_version         = deployment.model_version
    }
  }
}

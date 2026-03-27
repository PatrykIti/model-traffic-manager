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

output "openai_account_endpoint" {
  value = module.openai_account.endpoint
}

output "openai_account_id" {
  value = module.openai_account.id
}

output "provider_scope" {
  value = "https://cognitiveservices.azure.com/.default"
}

output "provider_chat_deployments" {
  value = {
    for deployment in local.enabled_openai_chat_deployments :
    deployment.router_deployment_id => {
      azure_deployment_name = deployment.azure_deployment_name
      model_name            = deployment.model_name
      model_version         = deployment.model_version
    }
  }
}

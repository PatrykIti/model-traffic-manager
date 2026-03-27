location         = "westeurope"
aks_node_vm_size = "Standard_D2s_v4"

openai_location = "swedencentral"

auth_deployments = [
  {
    router_deployment_id  = "gpt-5-1-auth"
    azure_deployment_name = "gpt-5-1"
    model_name            = "gpt-5.1"
    model_version         = "2025-11-13"
    sku_name              = "GlobalStandard"
    capacity              = 1
    enabled               = true
  }
]

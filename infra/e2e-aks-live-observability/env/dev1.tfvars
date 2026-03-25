location         = "westeurope"
aks_node_vm_size = "Standard_D2s_v4"

openai_location = "swedencentral"

observability_deployments = [
  {
    router_deployment_id  = "gpt-5-1-observability"
    azure_deployment_name = "gpt-5-1"
    consumer_role         = "bot-system-be"
    model_name            = "gpt-5.1"
    model_version         = "2025-11-13"
    sku_name              = "GlobalStandard"
    capacity              = 1
    enabled               = true
  }
]

openai_location = "swedencentral"

openai_chat_deployments = [
  {
    router_deployment_id  = "gpt-5-1"
    azure_deployment_name = "gpt-5-1"
    model_name            = "gpt-5.1"
    model_version         = "2025-11-13"
    sku_name              = "GlobalStandard"
    capacity              = 1
    enabled               = true
  },
  {
    router_deployment_id  = "gpt-5-2"
    azure_deployment_name = "gpt-5-2"
    model_name            = "gpt-5.2"
    model_version         = "2025-12-11"
    sku_name              = "GlobalStandard"
    capacity              = 1
    enabled               = true
  }
]

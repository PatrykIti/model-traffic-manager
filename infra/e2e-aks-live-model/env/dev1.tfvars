openai_location = "swedencentral"

openai_chat_deployments = [
  {
    router_deployment_id  = "gpt-5-1-chat"
    azure_deployment_name = "gpt-5-1-chat"
    model_name            = "gpt-5.1-chat"
    model_version         = "2025-11-13"
    sku_name              = "GlobalStandard"
    capacity              = 1
    enabled               = true
  },
  {
    router_deployment_id  = "gpt-5-2-chat"
    azure_deployment_name = "gpt-5-2-chat"
    model_name            = "gpt-5.2-chat"
    model_version         = "2025-11-13"
    sku_name              = "GlobalStandard"
    capacity              = 1
    enabled               = true
  }
]

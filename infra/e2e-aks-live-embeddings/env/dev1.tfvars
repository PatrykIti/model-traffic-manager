location         = "northeurope"
aks_node_vm_size = "Standard_D2s_v4"

openai_location = "germanywestcentral"

openai_embedding_deployments = [
  {
    router_deployment_id  = "text-embedding-3-small"
    azure_deployment_name = "text-embedding-3-small"
    model_name            = "text-embedding-3-small"
    model_version         = "1"
    sku_name              = "GlobalStandard"
    capacity              = 1
    enabled               = true
  }
]

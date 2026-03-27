variable "environment" {
  type = string
}

variable "subscription_id" {
  type = string
}

variable "location" {
  type = string
}

variable "name_prefix" {
  type = string
}

variable "run_id" {
  type = string
}

variable "ttl_hours" {
  type    = number
  default = 6
}

variable "kubernetes_version" {
  type    = string
  default = null
}

variable "aks_node_vm_size" {
  type    = string
  default = "Standard_D2s_v4"
}

variable "openai_location" {
  type    = string
  default = "swedencentral"
}

variable "openai_chat_deployments" {
  type = list(object({
    router_deployment_id  = string
    azure_deployment_name = string
    model_name            = string
    model_version         = string
    sku_name              = string
    capacity              = number
    enabled               = optional(bool, true)
  }))
}

variable "openai_custom_subdomain_name" {
  type    = string
  default = null
}

variable "tags" {
  type    = map(string)
  default = {}
}

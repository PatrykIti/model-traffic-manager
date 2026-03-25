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

variable "observability_deployments" {
  type = list(object({
    router_deployment_id  = string
    azure_deployment_name = string
    consumer_role         = string
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

variable "log_analytics_workspace" {
  type = object({
    sku               = optional(string, "PerGB2018")
    retention_in_days = optional(number, 30)
  })
  default = {}
}

variable "application_insights" {
  type = object({
    application_type   = optional(string, "web")
    sampling_percentage = optional(number, 100)
  })
  default = {}
}

variable "tags" {
  type    = map(string)
  default = {}
}

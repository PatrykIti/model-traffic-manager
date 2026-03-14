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

variable "test_level" {
  type = string

  validation {
    condition     = contains(["integration-azure", "e2e-aks"], var.test_level)
    error_message = "test_level must be either integration-azure or e2e-aks."
  }
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
  default = "Standard_B2s"
}

variable "tags" {
  type    = map(string)
  default = {}
}

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
  default = "Standard_B2s"
}

variable "storage_account_replication_type" {
  type    = string
  default = "RAGRS"
}

variable "tags" {
  type    = map(string)
  default = {}
}

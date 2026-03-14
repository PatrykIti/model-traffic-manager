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

variable "tags" {
  type    = map(string)
  default = {}
}

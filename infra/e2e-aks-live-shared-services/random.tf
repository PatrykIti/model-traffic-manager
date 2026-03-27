resource "random_string" "storage_suffix" {
  length  = 6
  lower   = true
  numeric = true
  special = false
  upper   = false
}

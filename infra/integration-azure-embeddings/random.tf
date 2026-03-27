resource "random_string" "openai_suffix" {
  length  = 6
  lower   = true
  numeric = true
  special = false
  upper   = false
}

environment       = "prd1"
location          = "westeurope"
name_prefix       = "mtm"
ttl_hours         = 6
aks_node_vm_size  = "Standard_B2s"
kubernetes_version = null

tags = {
  "scope-profile" = "release"
}

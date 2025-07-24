output "name" { value = kubernetes_service_account.ksa.metadata[0].name }
output "namespace" { value = var.namespace }
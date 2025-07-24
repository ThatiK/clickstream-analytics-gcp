resource "kubernetes_cluster_role" "role" {
  metadata {
    name = var.role_name
  }

  rule {
    api_groups = var.api_groups
    resources  = var.resources
    verbs      = var.verbs
  }
}

resource "kubernetes_cluster_role_binding" "role_binding" {
  metadata {
    name = var.role_binding_name
  }

  role_ref {
    api_group = "rbac.authorization.k8s.io"
    kind      = "ClusterRole"
    name      = kubernetes_cluster_role.role.metadata[0].name
  }

  subject {
    kind      = "ServiceAccount"
    name      = var.service_account_name
    namespace = var.service_account_namespace
  }
}
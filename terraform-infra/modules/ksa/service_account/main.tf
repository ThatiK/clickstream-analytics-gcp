resource "kubernetes_service_account" "ksa" {
  metadata {
    name      = var.ksa_name
    namespace = var.namespace
    annotations = {
      "iam.gke.io/gcp-service-account" = var.iam_sa_email
    }
  }
}

# optional RBAC
resource "kubernetes_role" "ksa_role" {
  metadata {
    name      = "${var.ksa_name}-role"
    namespace = var.namespace
  }

  dynamic "rule" {
    for_each = var.rbac_rules
    content {
      api_groups = rule.value.api_groups
      resources  = rule.value.resources
      verbs      = rule.value.verbs
    }
  }
}


resource "kubernetes_role_binding" "ksa_rb" {
  metadata {
    name      = "${var.ksa_name}-rb"
    namespace = var.namespace
  }

  role_ref {
    kind      = "Role"
    name      = kubernetes_role.ksa_role.metadata[0].name
    api_group = "rbac.authorization.k8s.io"
  }

  subject {
    kind      = "ServiceAccount"
    name      = kubernetes_service_account.ksa.metadata[0].name
    namespace = var.namespace
  }
}
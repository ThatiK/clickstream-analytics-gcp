#resource "google_service_account_iam_binding" "wi_user" {
#  service_account_id = var.iam_sa_name
#  role               = "roles/iam.workloadIdentityUser"
#  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.ksa_namespace}/${var.ksa_name}]"
#}

resource "google_service_account_iam_member" "wi_user" {
  service_account_id = var.iam_sa_name
  role               = "roles/iam.workloadIdentityUser"
  member             = "serviceAccount:${var.project_id}.svc.id.goog[${var.ksa_namespace}/${var.ksa_name}]"
}
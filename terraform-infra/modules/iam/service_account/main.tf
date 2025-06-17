resource "google_service_account" "this" {
  account_id   = var.account_id
  display_name = var.display_name
  description  = var.description
}

resource "google_project_iam_member" "this" {
  for_each = toset(var.iam_roles)
  project  = var.project_id
  role     = each.key
  member   = "serviceAccount:${google_service_account.this.email}"
}

# Self-impersonation: Allow the service account to act as itself
resource "google_service_account_iam_member" "self_impersonation" {
  service_account_id = google_service_account.this.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${google_service_account.this.email}"
}
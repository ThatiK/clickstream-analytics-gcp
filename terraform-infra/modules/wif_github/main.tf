resource "google_iam_workload_identity_pool" "github_pool" {
  project                   = var.project_id
  workload_identity_pool_id = var.pool_id
  display_name              = "GitHub Workload Identity Pool"
  description               = "Pool to allow GitHub Actions to access GCP resources"
}

resource "google_iam_workload_identity_pool_provider" "github_provider" {
  project                               = var.project_id
  workload_identity_pool_id             = google_iam_workload_identity_pool.github_pool.workload_identity_pool_id
  workload_identity_pool_provider_id    = var.provider_id
  display_name                          = "GitHub Provider"
  description                           = "OIDC identity provider for GitHub Actions"
  
  attribute_mapping = {
    "google.subject"             = "assertion.sub"
    "attribute.repository"       = "assertion.repository"
  }

  #  Only allow OIDC tokens from a specific repo (or add more later)
  attribute_condition = "attribute.repository == \"${var.repo}\""

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }
}

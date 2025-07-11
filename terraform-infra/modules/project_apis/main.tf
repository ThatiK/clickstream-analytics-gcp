resource "google_project_service" "enabled_apis" {
  for_each           = toset(var.apis)
  service            = each.key
  project            = var.project_id
  disable_on_destroy = false
}

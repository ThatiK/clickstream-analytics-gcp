resource "google_storage_bucket" "this" {
  name          = var.bucket_name
  location      = var.location
  force_destroy = true
}

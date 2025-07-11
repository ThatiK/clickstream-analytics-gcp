resource "google_bigquery_dataset" "this" {
  dataset_id                 = var.dataset_id
  location                   = var.location
  description                = var.description
  delete_contents_on_destroy = true

  labels = var.labels
}
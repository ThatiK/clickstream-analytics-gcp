provider "google" {
  project = var.project_id
  region  = var.region
}

module "gcs_bucket" {
  source      = "./modules/gcs_bucket"
  project_id  = var.project_id
  bucket_name = var.gcs_bucket_name
  location    = var.region
}

#module "dataproc_cluster" {
#  source       = "./modules/dataproc_cluster"
#  project_id   = var.project_id
#  region       = var.region
#  cluster_name = var.dataproc_cluster_name
#}

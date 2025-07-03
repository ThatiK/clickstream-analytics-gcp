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

### IAM ###

module "sa_data_eng" {
  source       = "./modules/iam/service_account"
  project_id   = var.project_id
  account_id   = "caec-data-eng-sa"
  display_name = "CAEC Data Engineer SA"
  iam_roles = [
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",      
    "roles/storage.objectViewer", 
    "roles/storage.objectCreator",
    "roles/dataproc.editor",      
    "roles/dataproc.worker",      
    "roles/logging.logWriter",    
  ]
}

#module "sa_analyst" {
#  source       = "./modules/iam/service_account"
#  project_id   = var.project_id
#  account_id   = "caec-analyst-sa"
#  display_name = "CAEC Data Analyst SA"
#  roles = {
#    "roles/bigquery.dataViewer" = "Read-only access to modeled data"
#  }
#}
#
#module "sa_steward" {
#  source       = "./modules/iam/service_account"
#  project_id   = var.project_id
#  account_id   = "caec-steward-sa"
#  display_name = "CAEC Data Steward SA"
#  roles = {
#    "roles/bigquery.metadataViewer" = "Can inspect table schemas"
#    "roles/datacatalog.viewer"      = "Can view data catalog entries"
#    "roles/viewer"                  = "Basic viewer rights for audit"
#  }
#}


### BIG QUERY ###

module "bq_staging" {
  source      = "./modules/bigquery_dataset"
  dataset_id  = "caec_staging"
  description = "Cleaned raw data models"
  labels = {
    layer = "staging"
    owner = "data-engineering"
  }
}

module "bq_warehouse" {
  source      = "./modules/bigquery_dataset"
  dataset_id  = "caec_warehouse"
  description = "Fact and dimension models"
  labels = {
    layer = "warehouse"
    owner = "data-engineering"
  }
}

module "bq_marts" {
  source      = "./modules/bigquery_dataset"
  dataset_id  = "caec_analytics"
  description = "Reporting marts"
  labels = {
    layer = "marts"
    owner = "data-engineering"
  }
}
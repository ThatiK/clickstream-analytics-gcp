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

module "caec_airflow_sa" {
  source       = "./modules/iam/service_account"
  display_name  = "CAEC Airflow Service Account"
  project_id   = var.project_id
  account_id   = "caec-airflow-sa"
  description  = "Used by Airflow to run Spark jobs, access GCS and BigQuery"
  iam_roles    = [
    "roles/dataproc.editor",
    "roles/dataproc.worker",
    "roles/storage.objectAdmin",
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/logging.logWriter"
  ]
}

module "caec_dbt_sa" {
  source       = "./modules/iam/service_account"
  project_id   = var.project_id
  account_id   = "caec-dbt-sa"
  display_name = "CAEC dbt Service Account"
  description  = "Used by dbt to run models on BigQuery"
  iam_roles    = [
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser"
  ]
}


variable "project_id" {}

variable "project_number" {
  type = string
}

variable "region" {
  default = "us-central1"
}

variable "gcs_bucket_data" {
  default = "caec-data"
}

variable "gcs_bucket_dags" {
  default = "caec-dags"
}

variable "gcs_bucket_scripts" {
  default = "caec-scripts"
}

variable "gcs_bucket_artifacts" {
  default = "caec-artifacts"
}

variable "repository_id" {
  default = "caec-docker"
}

variable "composer_env_name" {
  default = "caec-airflow"
}

variable "composer_image_version" {
  default = "composer-2.13.5-airflow-2.10.5"
}

#variable "dataproc_cluster_name" {
#  default = "caec-cluster"
#}

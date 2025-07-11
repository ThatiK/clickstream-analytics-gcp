variable "project_id" {}
variable "region" {}
variable "env_name" {}
variable "env_size" {}
variable "dag_bucket" {}
variable "worker_service_account" {}
variable "image_version" {}
variable "env_variables" {
  type    = map(string)
  default = {}
}

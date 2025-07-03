variable "dataset_id" {
  type = string
}

variable "location" {
  type    = string
  default = "us-central1"
}

variable "description" {
  type    = string
  default = "Managed by Terraform"
}

variable "labels" {
  type    = map(string)
  default = {}
}
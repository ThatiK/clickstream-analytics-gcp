variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "account_id" {
  description = "Service Account ID (without domain)"
  type        = string
}

variable "display_name" {
  description = "Display name for the service account"
  type        = string
  default     = ""
}

variable "description" {
  description = "Description for the service account"
  type        = string
  default     = ""
}

variable "iam_roles" {
  description = "List of IAM roles to bind to this service account"
  type        = list(string)
}



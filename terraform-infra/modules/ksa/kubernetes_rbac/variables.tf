variable "role_name" {
  description = "Name of the Kubernetes ClusterRole"
  type        = string
}

variable "api_groups" {
  description = "API groups for the ClusterRole"
  type        = list(string)
}

variable "resources" {
  description = "Resources for the ClusterRole"
  type        = list(string)
}

variable "verbs" {
  description = "Verbs for the ClusterRole"
  type        = list(string)
}

variable "role_binding_name" {
  description = "Name of the Kubernetes ClusterRoleBinding"
  type        = string
}

variable "service_account_name" {
  description = "Name of the Kubernetes Service Account"
  type        = string
}

variable "service_account_namespace" {
  description = "Namespace of the Kubernetes Service Account"
  type        = string
}
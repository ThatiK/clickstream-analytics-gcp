variable "project_id" {}
variable "pool_id"     { default = "github-pool-v2" }
variable "provider_id" { default = "github-oidc" }
variable "repo"        { description = "GitHub repo in org/repo form" }

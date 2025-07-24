variable "ksa_name" { type = string }
variable "namespace" {
  type    = string
  default = "default"
}
variable "iam_sa_email" {
  type = string
}
variable "rbac_rules" { # list(object({ api_groups = list(string)
  description = "Optional custom RBAC rule set"
  type = list(object({ api_groups = list(string) #                 verbs     = list(string) }))
    resources = list(string)
    verbs     = list(string)
    })
  )
  default = [{
    api_groups = [""],
    resources  = ["pods", "pods/log", "pods/exec"],
    verbs      = ["get", "list", "watch", "create", "delete"]
  }]
}
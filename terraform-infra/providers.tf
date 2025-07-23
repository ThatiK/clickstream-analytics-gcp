

###########################################################
# Discover the Composer‑managed GKE cluster endpoint
###########################################################
data "google_composer_environment" "env" {
  name     = var.composer_env_name
  region   = var.region
}

locals {
  # gke_cluster format:
  # //container.googleapis.com/projects/<proj>/locations/<region>/clusters/<cluster-name>
  gke_cluster_name = regex("clusters/(.*)$", data.google_composer_environment.env.config[0].gke_cluster)[0]
}

data "google_container_cluster" "composer_cluster" {
  name     = local.gke_cluster_name
  location = var.region
  project  = var.project_id
}

data "google_client_config" "default" {}

provider "kubernetes" {
  host                   = "https://${data.google_container_cluster.composer_cluster.endpoint}"
  cluster_ca_certificate = base64decode(data.google_container_cluster.composer_cluster.master_auth[0].cluster_ca_certificate)
  token                  = data.google_client_config.default.access_token
}

#provider "kubernetes" {
#  config_path = "~/.kube/config"
#}
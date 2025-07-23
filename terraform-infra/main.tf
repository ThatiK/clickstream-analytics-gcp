provider "google" {
  project     = var.project_id
  region      = var.region
  credentials = file("${path.module}/../keys/caec-ops-sa.json")
}

###################
### ENABLE APIS ###
###################

module "enable_apis" {
  source     = "./modules/project_apis"
  project_id = var.project_id
  apis = [
    "compute.googleapis.com",
    "container.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "cloudtrace.googleapis.com",
    "bigquery.googleapis.com",
    "storage.googleapis.com",
    "composer.googleapis.com",
    "artifactregistry.googleapis.com",
    "dataproc.googleapis.com",
    "logging.googleapis.com",
    "monitoring.googleapis.com"
  ]
}


###########
### GCS ###
###########

module "data_bucket" {
  source      = "./modules/gcs_bucket"
  bucket_name = var.gcs_bucket_data
  location    = var.region
  project_id  = var.project_id
}

module "dags_bucket" {
  source      = "./modules/gcs_bucket"
  bucket_name = var.gcs_bucket_dags
  location    = var.region
  project_id  = var.project_id
}

module "scripts_bucket" {
  source      = "./modules/gcs_bucket"
  bucket_name = var.gcs_bucket_scripts
  location    = var.region
  project_id  = var.project_id
}

module "artifacts_bucket" {
  source      = "./modules/gcs_bucket"
  bucket_name = var.gcs_bucket_artifacts
  location    = var.region
  project_id  = var.project_id
}



###########
### IAM ###
###########

module "sa_ops" {
  source       = "./modules/iam/service_account"
  project_id   = var.project_id
  account_id   = "caec-ops-sa"
  display_name = "CAEC Operations Support Service Account"
  iam_roles = [
    "roles/resourcemanager.projectIamAdmin",
    "roles/storage.admin",
    "roles/bigquery.admin",
    "roles/composer.admin",
    "roles/iam.serviceAccountAdmin",
    "roles/artifactregistry.admin",
    "roles/compute.networkAdmin",
    "roles/serviceusage.serviceUsageAdmin",
    "roles/iam.serviceAccountUser",
    "roles/iam.workloadIdentityPoolAdmin",
    "roles/container.viewer",
    "roles/container.admin",
    "roles/iam.serviceAccountAdmin",
  ]
}

module "sa_data_eng" {
  source       = "./modules/iam/service_account"
  project_id   = var.project_id
  account_id   = "caec-data-eng-sa"
  display_name = "CAEC Data Engineer Service Account"
  iam_roles = [
    # BigQuery / Storage / Spark roles 
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/storage.objectViewer",
    "roles/storage.objectCreator",
    "roles/dataproc.editor",
    "roles/dataproc.worker",

    # Composer-specific runtime roles
    "roles/composer.worker",
    "roles/artifactregistry.reader",
    "roles/artifactregistry.writer",
    "roles/logging.logWriter",
    "roles/monitoring.metricWriter",
    "roles/cloudtrace.agent",

    # GKE node roles ──
    "roles/container.defaultNodeServiceAccount",
    "roles/container.nodeServiceAccount",
    "roles/container.viewer"
  ]
}

module "sa_analyst" {
  source       = "./modules/iam/service_account"
  project_id   = var.project_id
  account_id   = "caec-analyst-sa"
  display_name = "CAEC Data Analyst Service Account"
  iam_roles = [
    "roles/bigquery.dataViewer",
    "roles/storage.objectViewer"
  ]
}



#################
### BIG QUERY ###
#################

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


###################
### ARTIFACTORY ###
###################
module "artifact_registry" {
  source        = "./modules/artifact_registry"
  location      = var.region
  repository_id = var.repository_id
  description   = "Docker images for CAEC CI/CD"
}


################
### COMPOSER ###
################

# Required for Composer V2 creation: grant composer service agent extended permissions
resource "google_project_iam_member" "composer_service_agent_ext" {
  project = var.project_id
  role    = "roles/composer.ServiceAgentV2Ext"
  member  = "serviceAccount:service-${var.project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}

# Composer SA can act as data-eng-sa
resource "google_service_account_iam_member" "composer_can_act_as_data_eng" {
  service_account_id = module.sa_data_eng.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:service-${var.project_number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}

# ops-sa can act as data-eng-sa
resource "google_service_account_iam_member" "ops_can_act_as_data_eng" {
  service_account_id = module.sa_data_eng.name
  role               = "roles/iam.serviceAccountUser"
  member             = "serviceAccount:${module.sa_ops.email}"
}

module "composer_env" {
  source                 = "./modules/composer_env"
  project_id             = var.project_id
  region                 = var.region
  env_name               = var.composer_env_name
  dag_bucket             = var.gcs_bucket_dags
  worker_service_account = module.sa_data_eng.email

  image_version = var.composer_image_version

  env_variables = {
    CAEC_PROJECT_ID     = var.project_id
    CAEC_REGION         = var.region
    CAEC_DATA_BUCKET    = var.gcs_bucket_data
    CAEC_SA_EMAIL       = module.sa_data_eng.email
    CAEC_SCRIPTS_BUCKET = var.gcs_bucket_scripts
    CAEC_ENV            = var.composer_env
  }

  env_size = "ENVIRONMENT_SIZE_SMALL"

  depends_on = [module.enable_apis]
}

#locals {
#  composer_namespace = module.composer_env.gke_namespace
#}
#
#output "gke_namespace" {
#  description = "The GKE namespace created by the Composer environment"
#  value       = local.composer_namespace
#}

##################
### GITHUB WIF ###
##################
module "github_wif" {
  source     = "./modules/wif_github"
  project_id = var.project_id
  repo       = var.github_repo
}

# Allow GitHub tokens to impersonate the Ops SA  (terraform jobs)
resource "google_service_account_iam_member" "github_impersonate_ops" {
  service_account_id = module.sa_ops.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/projects/${var.project_number}/locations/global/workloadIdentityPools/github-pool-v2/attribute.repository/${var.github_repo}"
}

# Allow GitHub tokens to impersonate the Data-Eng SA  (build / run)
resource "google_service_account_iam_member" "github_impersonate_data_eng" {
  service_account_id = module.sa_data_eng.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/projects/${var.project_number}/locations/global/workloadIdentityPools/github-pool-v2/attribute.repository/${var.github_repo}"
}


#########################################
##  Kubernetes Service Account + RBAC ###
#########################################

module "kubernetes_rbac" {
  source = "./modules/ksa/kubernetes_rbac"

  role_name               = "default-sa-full-pod-access"
  api_groups              = [""]
  resources               = ["pods", "pods/log"]
  verbs                   = ["get", "list", "watch", "create", "delete", "update", "patch"]
  role_binding_name       = "default-sa-cluster-reader-binding"
  service_account_name    = "default"
  service_account_namespace = "composer-2-13-7-airflow-2-9-3-5cfba5c4"
}


module "wi_binding_default_ksa" {
  source         = "./modules/iam/workload_identity_binding"
  iam_sa_name    = module.sa_data_eng.name
  iam_sa_email   = module.sa_data_eng.email
  project_id    = var.project_id
  ksa_name       = "default"              
  ksa_namespace  = "composer-2-13-7-airflow-2-9-3-5cfba5c4"
}
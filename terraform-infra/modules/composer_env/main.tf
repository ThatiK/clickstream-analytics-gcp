resource "google_composer_environment" "composer" {
  name   = var.env_name
  region = var.region
  project = var.project_id

  config {
    software_config {
      image_version = var.image_version
      airflow_config_overrides = {
        core-dags_are_paused_at_creation = "false"
      }
      env_variables = var.env_variables
    }

    node_config {
      service_account = var.worker_service_account
    }

    workloads_config {
      scheduler {
        cpu        = 1
        memory_gb  = 2
        storage_gb = 1
      }
      web_server {
        cpu        = 1
        memory_gb  = 2
        storage_gb = 1
      }
      worker {
        cpu        = 1
        memory_gb  = 2
        storage_gb = 1
      }
    }

    environment_size = "ENVIRONMENT_SIZE_SMALL"
    #dag_gcs_prefix   = "gs://${var.dag_bucket}/dags"
  }

}

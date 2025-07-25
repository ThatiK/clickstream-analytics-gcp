resource "google_composer_environment" "composer" {
  name    = var.env_name
  region  = var.region
  project = var.project_id

  config {

    environment_size = var.env_size

    node_config {
      service_account = var.worker_service_account
    }

    software_config {
      image_version = var.image_version
      #airflow_config_overrides = var.airflow_config_overrides
      env_variables = var.env_variables

      pypi_packages = {
        "apache-airflow-providers-cncf-kubernetes" = ">=10.4.2"
      }
    }
  }

}

#output "gke_namespace" {
#  value = google_composer_environment.composer.config.0.software_config.0.pypi_packages["composer-namespace"]
#}

resource "null_resource" "composer_namespace" {
  provisioner "local-exec" {
    command = <<EOT
      kubectl get ns -o json | jq -r '.items[].metadata.name' | grep ^composer-
    EOT
  }

  depends_on = [google_composer_environment.composer]
}
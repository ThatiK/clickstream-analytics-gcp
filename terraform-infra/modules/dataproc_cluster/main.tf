resource "google_dataproc_cluster" "this" {
  name   = var.cluster_name
  region = var.region

  cluster_config {
    master_config {
      num_instances = 1
      machine_type  = "n1-standard-2"
    }

    worker_config {
      num_instances = 2
      machine_type  = "n1-standard-2"
    }

    gce_cluster_config {
      zone = "${var.region}-a"
    }

    software_config {
      image_version        = "2.1-debian11"
    }
  }
}

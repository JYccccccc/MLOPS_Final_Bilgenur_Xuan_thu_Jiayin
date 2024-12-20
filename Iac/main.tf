provider "google" {
  project = var.project_id
  region  = var.region
  credentials = file("~/.config/gcloud/application_default_credentials.json")
}

resource "google_compute_instance" "vm_instance" {
  count        = var.instance_count
  name         = "terraform-vm-${count.index}"
  machine_type = var.instance_type
  zone         = "${var.region}-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {}
  }
}

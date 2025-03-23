provider "google" {
  project = "34781"
  region  = "us-central1"
}

resource "google_compute_instance" "default" {
  name         = "aa-microservice-vm"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

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

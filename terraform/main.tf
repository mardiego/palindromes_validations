terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

provider "null" {}

# Start Minikube Cluster
resource "null_resource" "start_minikube" {
  provisioner "local-exec" {
    command = "minikube start --driver=docker"
  }

  triggers = {
    always_run = "${timestamp()}"
  }
}

# Verify Minikube Cluster
resource "null_resource" "verify_minikube" {
  depends_on = [null_resource.start_minikube]

  provisioner "local-exec" {
    command = "kubectl cluster-info"
  }
}

# Enable Minikube Add-ons (Optional)
resource "null_resource" "enable_ingress" {
  depends_on = [null_resource.start_minikube]

  provisioner "local-exec" {
    command = "minikube addons enable ingress"
  }
}


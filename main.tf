terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.20" # Use a recent version
    }
  }
}

# Configure the Kubernetes provider.
# For Docker Desktop, it usually auto-detects the kubeconfig.
provider "kubernetes" {
  config_path    = "~/.kube/config"     # Tells Terraform where to find your kubeconfig file
  config_context = "docker-desktop"     # Specifies which cluster context to use (usually 'docker-desktop' for Docker Desktop)
}

# Define a Kubernetes Deployment for your application
resource "kubernetes_deployment" "sre_app_deployment" {
  metadata {
    name   = "sre-app-deployment"
    labels = {
      App = "sre-app"
    }
  }

  spec {
    replicas = 1 # Start with one copy of your application

    selector {
      match_labels = {
        App = "sre-app"
      }
    }

    template {
      metadata {
        labels = {
          App = "sre-app"
        }
      }

      spec {
        container {
          image = "fergumal/sre-project-app:latest" # Your image from Docker Hub
          name  = "sre-app-container"
          port {
            container_port = 5000 # The port your Flask app listens on inside the container
          }
        }
      }
    }
  }
}

# Define a Kubernetes Service to expose your application
resource "kubernetes_service" "sre_app_service" {
  metadata {
    name = "sre-app-service"
  }
  spec {
    selector = {
      App = "sre-app" # This must match the labels of your Deployment's pods
    }
    port {
      port        = 80   # The port the service will listen on (inside the cluster)
      target_port = 5000 # The port on the container to forward traffic to
      # node_port   = 30081 # Optional: If you want to specify a NodePort, otherwise Kubernetes picks one
    }
    type = "NodePort" # Makes the service accessible on each Node's IP at a static port.
                      # LoadBalancer type might not work easily with Docker Desktop.
  }
}

# Output the NodePort for easy access
output "app_node_port" {
  value = kubernetes_service.sre_app_service.spec[0].port[0].node_port
}
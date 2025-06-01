# Tell Terraform we are using the Docker provider
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# Configure the Docker provider to connect to your local Docker engine
provider "docker" {}

# This tells Terraform to always pull the latest version of your
# image from Docker Hub when you run the plan/apply command.
resource "docker_image" "sre_app" {
  name          = "fergumal/sre-project-app:v2"
  pull_triggers = ["${timestamp()}"]
}

# This defines the container itself
resource "docker_container" "sre_app_container" {
  # Name the container
  name  = "sre-project-app-tf"

  # Use the ID of the image we just pulled
  image = docker_image.sre_app.image_id

  # Map port 8080 on your computer to port 5000 in the container
  ports {
    internal = 5000
    external = 8081
  }
}
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "nginx" {
  name         = "nginx:alpine"
  keep_locally = false
}

resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "my-terraform-nginx"

  ports {
    internal = 80
    external = 8888
  }
}

output "container_id" {
  value = docker_container.nginx.id
}

output "nginx_url" {
  value = "http://localhost:8888"
}

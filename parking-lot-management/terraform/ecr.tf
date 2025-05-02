provider "aws" {
  region = "us-east-1"
}

resource "aws_ecr_repository" "parking_app" {
  name = "parking-app"
  force_delete = true

  image_scanning_configuration {
    scan_on_push = true
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.parking_app.repository_url
}

output "repository_url" {
  value = aws_ecr_repository.aws_ecr.repository_url
}
output "repository_name" {
    value = "${var.app_name}-${var.identifier}"
}
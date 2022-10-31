resource "aws_ecr_repository" "aws_ecr" {
  name = "${var.app_name}-${var.identifier}"
  tags = {
    Name = "${var.app_name}-ecr"
  }
  force_delete = true
}

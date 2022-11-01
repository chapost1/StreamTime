resource "aws_s3_bucket" "videos_bucket" {
  bucket        = "${var.app_name}-bucket"
  force_destroy = true
  tags = {
    Name = "${var.app_name}-s3-bucket"
  }
}

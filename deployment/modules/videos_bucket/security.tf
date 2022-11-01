resource "aws_s3_bucket_cors_configuration" "videos_bucket_cors_rule" {
  bucket = aws_s3_bucket.videos_bucket.id

  # cors_rule { # todo: allow from app
  #   allowed_headers = ["*"]
  #   allowed_methods = ["PUT", "POST"]
  #   allowed_origins = ["https://s3-website-test.hashicorp.com"]
  #   expose_headers  = ["ETag"]
  #   max_age_seconds = 3000
  # }

  cors_rule {
    allowed_methods = ["GET"]
    allowed_origins = ["*"] # todo: mark app as allowed when ui exists (instead of wildcard)
  }
}

resource "aws_s3_bucket_acl" "videos_bucket_acl" {
  bucket = aws_s3_bucket.videos_bucket.id
  acl    = "private"
}

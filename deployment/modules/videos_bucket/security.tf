resource "aws_s3_bucket_cors_configuration" "videos_bucket_cors_rule" {
  bucket = aws_s3_bucket.videos_bucket.id

  cors_rule {
    allowed_methods = ["POST", "PUT", "GET", "DELETE", "HEAD"]
    allowed_origins = ["*"] # todo: mark app as allowed when ui exists (instead of wildcard)
    allowed_headers = ["*"]
    expose_headers = [
      "Access-Control-Allow-Origin",
      "Content-Type"
    ]
  }
}

resource "aws_s3_bucket_acl" "videos_bucket_acl" {
  bucket = aws_s3_bucket.videos_bucket.id
  acl    = "private"
}

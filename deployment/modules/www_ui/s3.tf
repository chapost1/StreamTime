# S3 bucket for website.
resource "aws_s3_bucket" "www_bucket" {
  bucket = var.domain
}

resource "aws_s3_bucket_acl" "www_bucket" {
  bucket = aws_s3_bucket.www_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_policy" "allow_get_object_from_bucket" {
  bucket = aws_s3_bucket.www_bucket.id
  policy = data.aws_iam_policy_document.allow_get_object_from_bucket.json
}

data "aws_iam_policy_document" "allow_get_object_from_bucket" {
  statement {
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.www_s3_distribution_origin_access_identity.iam_arn]
    }
    effect = "Allow"
    sid    = "PublicReadGetObject"
    actions = [
      "s3:GetObject"
    ]

    resources = [
      "${aws_s3_bucket.www_bucket.arn}/*",
    ]
  }
}

resource "aws_s3_bucket_cors_configuration" "www_bucket" {
  bucket = aws_s3_bucket.www_bucket.id

  cors_rule {
    allowed_headers = ["Authorization", "Content-Length"]
    allowed_methods = ["GET", "POST"]
    allowed_origins = ["https://${var.domain}"]
    max_age_seconds = 600
  }
}

resource "aws_s3_bucket_website_configuration" "www_bucket" {
  bucket = aws_s3_bucket.www_bucket.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "error.html"
  }
}

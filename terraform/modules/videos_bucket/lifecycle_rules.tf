resource "aws_s3_bucket_lifecycle_configuration" "videos_bucket_config" {
  bucket = aws_s3_bucket.videos_bucket.bucket
  rule {
    id = "uploaded-videos"

    expiration {
      days = 1
    }

    filter {
      and {
        prefix = "${var.uploaded_videos_prefix}/"

        tags = {
          rule      = "uploaded-videos"
          autoclean = "true"
        }
      }
    }

    status = "Enabled"
  }
  rule {
    id = "unprocessed-videos"

    expiration {
      days = 1
    }

    filter {
      and {
        prefix = "${var.unprocessed_videos_prefix}/"

        tags = {
          rule      = "unprocessed-videos"
          autoclean = "true"
        }
      }
    }

    status = "Enabled"
  }

  rule {
    id = "videos"

    filter {
      and {
        prefix = "${var.videos_prefix}/"

        tags = {
          rule      = "videos"
          autoclean = "true"
        }
      }
    }

    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 60
      storage_class = "INTELLIGENT_TIERING"
    }
  }

  rule {
    id = "tmp-thumbnails"

    expiration {
      days = 1
    }

    filter {
      and {
        prefix = "${var.tmp_thumbnails_prefix}/"

        tags = {
          rule      = "tmp-thumbnails"
          autoclean = "true"
        }
      }
    }

    status = "Enabled"
  }

  rule {
    id = "thumbnails"

    status = "Enabled"

    filter {
      and {
        prefix = "${var.thumbnails_prefix}/"

        tags = {
          rule      = "thumbnails"
          autoclean = "true"
        }
      }
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 60
      storage_class = "GLACIER_IR"
    }
  }
}

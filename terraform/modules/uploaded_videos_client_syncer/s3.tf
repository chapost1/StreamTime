# A bucket to store our Connection IDs
resource "aws_s3_bucket" "videos_sync_websocket_connection_store" {
  bucket_prefix = "${var.app_name}-sync-websocket-connection"
}


resource "aws_s3_bucket_lifecycle_configuration" "videos_sync_websocket_connection_store_bucket_config" {
  bucket = aws_s3_bucket.videos_sync_websocket_connection_store.bucket
  rule {
    id = "videos-sync-websocket-connection-store"

    expiration {
      days = 1
    }

    filter {
      and {
        prefix = "/"

        tags = {
          rule      = "videos-sync-websocket-connection-store"
          autoclean = "true"
        }
      }
    }

    status = "Enabled"
  }
}

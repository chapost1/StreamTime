# A bucket to store our Connection IDs
resource "aws_s3_bucket" "videos_sync_websocket_connection_store" {
  bucket_prefix = "${var.app_name}-sync-websocket-connection"
}

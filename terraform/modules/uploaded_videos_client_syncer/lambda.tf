data "archive_file" "archive_videos_websocket_client_syncer_lambda_dir" {
  type        = "zip"
  source_dir  = "${path.module}/../../../lambdas/workers/uploaded_videos_client_syncer/code"
  output_path = "${path.module}/../../../lambdas/workers/uploaded_videos_client_syncer/code.zip"
}

// source code
resource "aws_lambda_function" "websocket_messages_lambda_processor" {
  function_name    = "${var.app_name}-uploaded-videos-client-sync-lambda"
  handler          = "app.handler"
  role             = aws_iam_role.videos_websocket_maintainer_lambda.arn
  runtime          = "python3.8"
  filename         = data.archive_file.archive_videos_websocket_client_syncer_lambda_dir.output_path
  source_code_hash = data.archive_file.archive_videos_websocket_client_syncer_lambda_dir.output_base64sha256

  timeout = 15

  environment {
    variables = {
      CONNECTION_STORE_BUCKET_NAME  = aws_s3_bucket.videos_sync_websocket_connection_store.bucket
      CONNECTION_STORE_PREFIX       = var.connection_store_prefix
      EXECUTE_API_ENDPOINT          = replace(aws_apigatewayv2_stage.websocket_lambda.invoke_url, "wss://", "https://")
      uploaded_video_feedback_event = var.uploaded_video_feedback_event
    }
  }
}

# An SNS topic we can invoke to send messages to our API Gateway connections/Websocket clients
resource "aws_sns_topic" "uploaded_videos_sync_input" {
  name = "${var.app_name}-uploaded-videos-sync-sns-topic"
}

resource "aws_sns_topic_subscription" "uploaded_videos_sync_input_to_lambda" {
  topic_arn = aws_sns_topic.uploaded_videos_sync_input.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.websocket_messages_lambda_processor.arn
}

resource "aws_lambda_permission" "videos_upload_ws_maintainer_lambda_with_sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.websocket_messages_lambda_processor.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.uploaded_videos_sync_input.arn
}

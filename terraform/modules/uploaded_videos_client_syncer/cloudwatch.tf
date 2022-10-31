# Create CloudWatch Log Groups so we can set default retentions
resource "aws_cloudwatch_log_group" "videos_sync_api_gw" {
  name              = "/aws/apigateway/${aws_apigatewayv2_api.videos_websocket_maintainer.name}"
  retention_in_days = 7
}

resource "aws_cloudwatch_log_group" "videos_sync_lambda_main" {
  name              = "/aws/lambda/${aws_lambda_function.websocket_messages_lambda_processor.function_name}"
  retention_in_days = 7
}

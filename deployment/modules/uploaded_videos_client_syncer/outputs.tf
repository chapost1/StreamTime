# Store various outputs for quick retrieval from our scripts
output "ws_url" {
  value = aws_apigatewayv2_stage.websocket_lambda.invoke_url
}

output "lambda_function_name" {
  value = aws_lambda_function.websocket_messages_lambda_processor.function_name
}

output "input_sns_topic_arn" {
  value = aws_sns_topic.uploaded_videos_sync_input.arn
}

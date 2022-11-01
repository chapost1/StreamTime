resource "aws_apigatewayv2_api" "videos_websocket_maintainer" {
  name                       = "${var.app_name}-websocket-api-gw"
  description                = "Websocket Maintained by AWS"
  protocol_type              = "WEBSOCKET"
  route_selection_expression = "$request.body.action"
}

# Use our Lambda function to service requests
resource "aws_apigatewayv2_integration" "websocket_messages_lambda_processor" {
  api_id             = aws_apigatewayv2_api.videos_websocket_maintainer.id
  integration_uri    = aws_lambda_function.websocket_messages_lambda_processor.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

# Forward special requests ($connect, $disconnect) to our Lambda function so we can manage their state
resource "aws_apigatewayv2_route" "websocket_connect" {
  api_id    = aws_apigatewayv2_api.videos_websocket_maintainer.id
  route_key = "$connect"
  target    = "integrations/${aws_apigatewayv2_integration.websocket_messages_lambda_processor.id}"
}

resource "aws_apigatewayv2_route" "websocket_disconnect" {
  api_id    = aws_apigatewayv2_api.videos_websocket_maintainer.id
  route_key = "$disconnect"
  target    = "integrations/${aws_apigatewayv2_integration.websocket_messages_lambda_processor.id}"
}

resource "aws_apigatewayv2_route" "websocket_default" {
  api_id    = aws_apigatewayv2_api.videos_websocket_maintainer.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.websocket_messages_lambda_processor.id}"
}

# A stage is required to actually "deploy" our API Gateway
resource "aws_apigatewayv2_stage" "websocket_lambda" {
  api_id      = aws_apigatewayv2_api.videos_websocket_maintainer.id
  name        = "primary"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.videos_sync_api_gw.arn
    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
    })
  }
}

# Allow the API Gateway to invoke Lambda function
resource "aws_lambda_permission" "api_gw_main_lambda_main" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.websocket_messages_lambda_processor.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.videos_websocket_maintainer.execution_arn}/*/*"
}



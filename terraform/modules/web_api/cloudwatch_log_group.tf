resource "aws_cloudwatch_log_group" "web_api_log_group" {
  name              = "/ecs/${var.app_name}/web-api"
  retention_in_days = 5

  tags = {
    Name = "${var.app_name}-cw-log-group"
  }
}

resource "aws_cloudwatch_log_stream" "web_api_log_stream" {
  name           = "${var.app_name}-web-api-log-stream"
  log_group_name = aws_cloudwatch_log_group.web_api_log_group.name
}

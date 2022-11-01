# For API Gateway Logging: https://aws.amazon.com/premiumsupport/knowledge-center/api-gateway-cloudwatch-logs/
# This is only required once per region
data "aws_iam_policy_document" "uploaded_videos_sync_cloudwatch_logging" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]
    effect = "Allow"

    principals {
      type = "Service"
      identifiers = [
        "apigateway.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "uploaded_videos_sync_cloudwatch_log_role" {
  count              = 1
  name               = "${var.app_name}-logging-uploaded-videos-sync-websocket"
  assume_role_policy = data.aws_iam_policy_document.uploaded_videos_sync_cloudwatch_logging.json
}

resource "aws_iam_role_policy_attachment" "cloudwatch_log_role" {
  count = 1

  role       = aws_iam_role.uploaded_videos_sync_cloudwatch_log_role[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

resource "aws_api_gateway_account" "uploaded_videos_sync_cloudwatch_config" {
  count               = 1
  cloudwatch_role_arn = aws_iam_role.uploaded_videos_sync_cloudwatch_log_role[0].arn
}

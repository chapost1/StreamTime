resource "aws_iam_role" "iam_for_deleted_videos_trigger_lambda" {
  name = "iam_for_deleted_videos_trigger_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

data "aws_cloudwatch_log_group" "rds_cluster_log_group" {
  name = "/aws/rds/cluster/${var.rds_cluster_identifier}/postgresql"
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.deleted_videos_trigger.function_name
  principal     = "logs.${var.region}.amazonaws.com"
  source_arn    = "${data.aws_cloudwatch_log_group.rds_cluster_log_group.arn}:*"
}

resource "aws_cloudwatch_log_subscription_filter" "rds_cluster_trigger_lambda_on_delete" {
  name            = "rds_cluster_trigger_lambda_on_delete"
  log_group_name  = data.aws_cloudwatch_log_group.rds_cluster_log_group.name
  filter_pattern  = "DELETE videos"
  destination_arn = aws_lambda_function.deleted_videos_trigger.arn
  distribution    = "Random"
}



# Lambda -> Cloudwatch
# This is to optionally manage the CloudWatch Log Group for the Lambda Function.
# If skipping this resource configuration, also add "logs:CreateLogGroup" to the IAM policy below.
resource "aws_cloudwatch_log_group" "new_video_processing_lambda_cloudwatch_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.deleted_videos_trigger.function_name}"
  retention_in_days = 14
}

resource "aws_iam_policy" "deleted_videos_trigger_lambda_cloudwatch_logging" {
  name        = "deleted_videos_trigger_lambda_cloudwatch_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "deleted_videos_trigger_lambda_cloudwatch_logs" {
  role       = aws_iam_role.iam_for_deleted_videos_trigger_lambda.name
  policy_arn = aws_iam_policy.deleted_videos_trigger_lambda_cloudwatch_logging.arn
}


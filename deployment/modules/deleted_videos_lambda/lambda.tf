data "archive_file" "python_deleted_videos_trigger_lambda_package" {
  type        = "zip"
  source_file = "${path.module}/../../../lambdas/workers/deleted_videos_trigger/app.py"
  output_path = "${path.module}/../../../lambdas/workers/deleted_videos_trigger/python.zip"
}

resource "aws_lambda_function" "deleted_videos_trigger" {
  function_name    = "deleted_videos_trigger"
  architectures    = ["x86_64"]
  filename         = data.archive_file.python_deleted_videos_trigger_lambda_package.output_path
  source_code_hash = data.archive_file.python_deleted_videos_trigger_lambda_package.output_base64sha256
  role             = aws_iam_role.iam_for_deleted_videos_trigger_lambda.arn
  handler          = "app.lambda_handler"
  runtime          = "python3.8"
  timeout          = 15

  tags = {
    Name = "${var.app_name}-deleted-videos-trigger-lambda-layer"
  }
}

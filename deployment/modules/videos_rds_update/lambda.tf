data "archive_file" "python_videos_rds_update_lambda_package" {
  type        = "zip"
  source_file = "${path.module}/../../../lambdas/workers/videos_rds_update/app.py"
  output_path = "${path.module}/../../../lambdas/workers/videos_rds_update/python.zip"
}

resource "aws_lambda_function" "videos_rds_update" {
  function_name    = "videos_rds_update"
  architectures    = ["x86_64"]
  filename         = data.archive_file.python_videos_rds_update_lambda_package.output_path
  source_code_hash = data.archive_file.python_videos_rds_update_lambda_package.output_base64sha256
  role             = aws_iam_role.iam_for_rds_videos_update_lambda.arn
  handler          = "app.lambda_handler"
  runtime          = "python3.8"
  timeout          = 15
  layers = [
    # psycopg2, source: https://github.com/keithrozario/Klayers/tree/master/deployments/python3.8
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p38-aws-psycopg2:1"
  ]


  environment {
    variables = {
      new_video_events_processing_has_been_started = var.new_video_events_processing_has_been_started
      new_video_events_processing_failure          = var.new_video_events_processing_failure
      new_video_events_moved_to_drafts             = var.new_video_events_moved_to_drafts
      rds_host                                     = var.rds_host
      rds_port                                     = var.rds_port
      rds_user                                     = var.rds_user
      rds_password                                 = var.rds_password
      rds_db_name                                  = var.rds_db_name
      rds_table_uprocessed_videos                  = var.rds_table_uprocessed_videos
      rds_table_videos                             = var.rds_table_videos
    }
  }

  tags = {
    Name = "${var.app_name}-videos-rds-update-lambda-layer"
  }

  vpc_config {
    subnet_ids         = [for s in var.private_subnet : s.id]
    security_group_ids = [aws_security_group.rds_lambda_sg.id]
  }
}

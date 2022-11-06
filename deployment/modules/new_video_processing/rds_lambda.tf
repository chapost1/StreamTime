# data "archive_file" "python_new_video_processing_lambda_package" {
#   type        = "zip"
#   source_file = "${path.module}/../../../lambdas/workers/new_video_processing/app.py"
#   output_path = "${path.module}/../../../lambdas/workers/new_video_processing/python.zip"
# }
# resource "aws_lambda_function" "new_video_processing" {
#   function_name    = "new_video_processing"
#   architectures    = ["arm64"]
#   filename         = data.archive_file.python_new_video_processing_lambda_package.output_path
#   source_code_hash = data.archive_file.python_new_video_processing_lambda_package.output_base64sha256
#   role             = aws_iam_role.iam_for_new_video_processing_lambda.arn
#   handler          = "app.lambda_handler"
#   runtime          = "python3.8"
#   timeout          = 300 # 5m
#   layers = [
#     aws_lambda_layer_version.ffmpeg_python_lambda_layer.arn,
#     # psycopg2
#     "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p38-aws-psycopg2:1"
#   ]

#   environment {
#     variables = {
#       rds_host                                            = var.rds_host
#       rds_port                                            = var.rds_port
#       rds_user                                            = var.rds_user
#       rds_password                                        = var.rds_password
#       rds_db_name                                         = var.rds_db_name
#       rds_table_uprocessed_videos                         = var.rds_table_uprocessed_videos
#       rds_table_videos                                    = var.rds_table_videos
#     }
#   }
#   tags = {
#     Name = "${var.app_name}-new-video-processing-lambda"
#   }

#   vpc_config {
#     subnet_ids         = var.private_subnet.*.id
#     security_group_ids = [aws_security_group.rds_lambda_sg.id]
#   }
# }

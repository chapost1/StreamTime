resource "aws_lambda_layer_version" "ffmpeg_python_lambda_layer" {
  filename                 = "${path.module}/../../../lambdas/layers/pyffmpeg/source/python.zip"
  layer_name               = "ffmpeg_python_lambda_layer"
  source_code_hash         = filebase64sha256("${path.module}/../../../lambdas/layers/pyffmpeg/source/python.zip")
  compatible_architectures = ["arm64"]
  compatible_runtimes      = ["python3.8"]
}

data "archive_file" "python_new_video_processing_lambda_package" {
  type        = "zip"
  source_file = "${path.module}/../../../lambdas/workers/new_video_processing/app.py"
  output_path = "${path.module}/../../../lambdas/workers/new_video_processing/python.zip"
}
resource "aws_lambda_function" "new_video_processing" {
  function_name    = "new_video_processing"
  architectures    = ["arm64"]
  filename         = data.archive_file.python_new_video_processing_lambda_package.output_path
  source_code_hash = data.archive_file.python_new_video_processing_lambda_package.output_base64sha256
  role             = aws_iam_role.iam_for_new_video_processing_lambda.arn
  handler          = "app.lambda_handler"
  runtime          = "python3.8"
  timeout          = 300 # 5m
  layers = [
    aws_lambda_layer_version.ffmpeg_python_lambda_layer.arn
  ]

  environment {
    variables = {
      image_resizer_lambda_arn                            = var.image_resizer_arn,
      s3_thumbnails_prefix                                = var.s3_thumbnails_prefix,
      s3_videos_prefix                                    = var.s3_videos_prefix,
      s3_uploaded_videos_prefix                           = var.s3_uploaded_videos_prefix,
      s3_unprocessed_videos_prefix                        = var.s3_unprocessed_videos_prefix,
      s3_thumbnails_acl                                   = var.s3_thumbnails_acl,
      s3_max_video_file_size_in_bytes                     = var.s3_max_video_file_size_in_bytes,
      new_video_processing_failure_internal_error         = var.new_video_processing_failure_internal_error
      new_video_processing_failure_max_file_size_exceeded = var.new_video_processing_failure_max_file_size_exceeded
      new_video_processing_failure_corrupted              = var.new_video_processing_failure_corrupted
      new_video_processing_failure_unsupported_video_type = var.new_video_processing_failure_unsupported_video_type
      new_video_events_processing_has_been_started        = var.new_video_events_processing_has_been_started
      new_video_events_processing_failure                 = var.new_video_events_processing_failure
      new_video_events_moved_to_drafts                    = var.new_video_events_moved_to_drafts
      uploaded_videos_client_sync_sns_topic_arn           = var.uploaded_videos_client_sync_sns_topic_arn
      uploaded_video_feedback_event                       = var.uploaded_video_feedback_event
      videos_rds_update_arn                               = var.videos_rds_update_arn
    }
  }
  tags = {
    Name = "${var.app_name}-new-video-processing-lambda"
  }
}

// invoke on s3 event
resource "aws_s3_bucket_notification" "new_video_upload" {
  bucket = var.s3_videos_bucket_id

  lambda_function {
    lambda_function_arn = aws_lambda_function.new_video_processing.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "${var.s3_uploaded_videos_prefix}/"
  }

  depends_on = [
    aws_lambda_function.new_video_processing
  ]
}

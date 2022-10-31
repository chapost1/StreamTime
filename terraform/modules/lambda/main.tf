resource "aws_iam_role" "iam_for_new_video_processing_lambda" {
  name = "iam_for_new_video_processing_lambda"

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

resource "aws_iam_role" "iam_for_image_resizer_lambda" {
  name = "iam_for_image_resizer_lambda"

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

resource "aws_lambda_permission" "video_processor_lambda_s3_invoke_permission" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.new_video_processing.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${var.s3_videos_bucket_id}"
}

resource "aws_lambda_layer_version" "ffmpeg_python_lambda_layer" {
  filename                      = "${path.module}/../../../lambdas/layers/pyffmpeg/source/python.zip"
  layer_name                    = "ffmpeg_python_lambda_layer"
  source_code_hash              = filebase64sha256("${path.module}/../../../lambdas/layers/pyffmpeg/source/python.zip")
  compatible_architectures      = ["arm64"]
  compatible_runtimes           = ["python3.8"]
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
  layers           = [
    aws_lambda_layer_version.ffmpeg_python_lambda_layer.arn
  ]
  depends_on = [
    aws_lambda_function.image_resizer
  ]
  environment {
    variables = {
      image_resizer_lambda_arn = aws_lambda_function.image_resizer.arn,
      s3_thumbnails_prefix = var.s3_thumbnails_prefix,
      s3_videos_prefix = var.s3_videos_prefix,
      s3_uploaded_videos_prefix = var.s3_uploaded_videos_prefix,
      s3_unprocessed_videos_prefix = var.s3_unprocessed_videos_prefix,
      s3_thumbnails_acl = var.s3_thumbnails_acl,
      s3_max_video_file_size_in_bytes = var.s3_max_video_file_size_in_bytes,
      new_video_processing_failure_internal_error = var.new_video_processing_failure_internal_error
      new_video_processing_failure_max_file_size_exceeded = var.new_video_processing_failure_max_file_size_exceeded
      new_video_processing_failure_corrupted = var.new_video_processing_failure_corrupted
      new_video_processing_failure_unsupported_video_type = var.new_video_processing_failure_unsupported_video_type
      dynamodb_table_invoked_uploaded_videos = var.dynamodb_table_invoked_uploaded_videos
      dynamodb_table_unprocessed_videos = var.dynamodb_table_unprocessed_videos
      dynamodb_table_drafts_videos = var.dynamodb_table_drafts_videos
      dynamodb_table_processing_has_been_failed_videos = var.dynamodb_table_processing_has_been_failed_videos
      new_video_events_processing_has_been_started = var.new_video_events_processing_has_been_started
      new_video_events_processing_failure = var.new_video_events_processing_failure
      new_video_events_moved_to_drafts = var.new_video_events_moved_to_drafts
    }
  }

  tags = {
    Name = "${var.app_name}-new-video-processing-lambda"
  }
}

// invoke
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

data "archive_file" "python_image_resizer_lambda_package" {  
  type        = "zip"  
  source_file = "${path.module}/../../../lambdas/workers/image_resizer/app.py" 
  output_path = "${path.module}/../../../lambdas/workers/image_resizer/python.zip"
}
resource "aws_lambda_function" "image_resizer" {
  function_name    = "image_resizer"
  architectures    = ["x86_64"]
  filename         = data.archive_file.python_image_resizer_lambda_package.output_path
  source_code_hash = data.archive_file.python_image_resizer_lambda_package.output_base64sha256
  role             = aws_iam_role.iam_for_image_resizer_lambda.arn
  handler          = "app.lambda_handler"
  runtime          = "python3.8"
  timeout          = 15
  layers           = [
    # PILLOW, source: https://github.com/keithrozario/Klayers/tree/master/deployments/python3.8
    "arn:aws:lambda:us-east-1:770693421928:layer:Klayers-p38-Pillow:4"
  ]

  tags = {
    Name = "${var.app_name}-image-resizer-lambda-layer"
  }
}

# lambda invoke lambda permissions

resource "aws_iam_policy" "invoke_image_resizer_lambda_policy" {
  name        = "invoke_image_resizer_lambda_policy"
  path        = "/"
  description = "IAM policy to invoke video thumbnail lambda"

  policy = jsonencode({
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
            "lambda:InvokeFunction",
            "lambda:InvokeAsync"
        ]
        "Resource": "${aws_lambda_function.image_resizer.arn}"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "new_video_processing_lambda_invoke_lambda_policy" {
  role       = aws_iam_role.iam_for_new_video_processing_lambda.name
  policy_arn = aws_iam_policy.invoke_image_resizer_lambda_policy.arn
}

# lambda s3 premissions
resource "aws_iam_policy" "lambda_s3" {
  name        = "lambda_s3"
  path        = "/"
  description = "IAM policy for s3 operations from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
            "s3:*"
      ],
      "Resource": "arn:aws:s3:::*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "new_video_processing_lambda_s3" {
  role       = aws_iam_role.iam_for_new_video_processing_lambda.name
  policy_arn = aws_iam_policy.lambda_s3.arn
}

resource "aws_iam_role_policy_attachment" "image_resizer_lambda_s3" {
  role       = aws_iam_role.iam_for_image_resizer_lambda.name
  policy_arn = aws_iam_policy.lambda_s3.arn
}

# Lambda <-> Cloudwatch
# This is to optionally manage the CloudWatch Log Group for the Lambda Function.
# If skipping this resource configuration, also add "logs:CreateLogGroup" to the IAM policy below.
resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/${aws_lambda_function.new_video_processing.function_name}"
  retention_in_days = 14
}

# See also the following AWS managed policy: AWSLambdaBasicExecutionRole
resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
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

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_for_new_video_processing_lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

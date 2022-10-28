variable "aws_access_key" {
    type        = string
    description = "AWS Access key"
}

variable "aws_secret_key" {
    type        = string
    description = "AWS Secret Key"
}

variable "aws_region" {
    type        = string
    description = "AWS Region"
}

provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}
provider "archive" {}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

locals {
    new_video_on_s3_queue = "new-video-on-s3-queue"
}

///// s3 bucket

// videos
resource "aws_s3_bucket" "videos_bucket" {
  bucket        = "svn-videos-bucket"
  force_destroy = true
}

resource "aws_s3_bucket_cors_configuration" "videos_bucket_cors_rule" {
  bucket = aws_s3_bucket.videos_bucket.id

  # cors_rule { # todo: allow from app
  #   allowed_headers = ["*"]
  #   allowed_methods = ["PUT", "POST"]
  #   allowed_origins = ["https://s3-website-test.hashicorp.com"]
  #   expose_headers  = ["ETag"]
  #   max_age_seconds = 3000
  # }

  cors_rule {
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
  }
}

resource "aws_s3_bucket_acl" "videos_bucket_acl" {
  bucket = aws_s3_bucket.videos_bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_lifecycle_configuration" "videos_bucket_config" {
  bucket = aws_s3_bucket.videos_bucket.bucket

  rule {
    id = "videos_meta_data"

    expiration {
      days = 2
    }

    filter {
      and {
        prefix = "meta/"

        tags = {
          rule      = "videos_meta_data"
          autoclean = "true"
        }
      }
    }

    status = "Enabled"
  }

  rule {
    id = "videos"

    expiration {
      days = 90
    }

    filter {
      and {
        prefix = "videos/"

        tags = {
          rule      = "videos"
          autoclean = "true"
        }
      }
    }

    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
  }

  rule {
    id = "thumbnails"

    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
  }
}


///// sqs

resource "aws_sqs_queue" "new_video_queue" {
  name = local.new_video_on_s3_queue
  message_retention_seconds = 86400
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.terraform_queue_deadletter.arn
    maxReceiveCount     = 1
  })

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": "*",
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:*:*:${local.new_video_on_s3_queue}",
      "Condition": {
        "ArnEquals": { "aws:SourceArn": "${aws_s3_bucket.videos_bucket.arn}" }
      }
    }
  ]
}
POLICY
}

resource "aws_sqs_queue" "terraform_queue_deadletter" {
  name = "terraform-deadletter-queue"
  // avoid circular dependency, aim for source queue explicitly
  redrive_allow_policy  = jsonencode({
    redrivePermission = "byQueue",
    sourceQueueArns   = ["arn:aws:sqs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${local.new_video_on_s3_queue}"]
  })  
}

# resource "aws_s3_bucket_notification" "new_video_upload" {
#   bucket = aws_s3_bucket.videos_bucket.id

#   queue {
#     queue_arn     = aws_sqs_queue.new_video_queue.arn
#     events        = ["s3:ObjectCreated:*"]
#     filter_prefix = "videos/"
#   }
# }

resource "aws_s3_bucket_notification" "new_video_upload" {
  bucket = aws_s3_bucket.videos_bucket.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.video_processor.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "videos/"
  }

  depends_on = [
    aws_s3_bucket.videos_bucket,
    aws_lambda_function.video_processor
  ]
}

///// Lambdas

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda"

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
  function_name = aws_lambda_function.video_processor.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${aws_s3_bucket.videos_bucket.id}"
}

data "archive_file" "python_video_processor_lambda_package" {  
  type        = "zip"  
  source_file = "${path.module}/../lambdas/workers/video_processor/app.py" 
  output_path = "${path.module}/../lambdas/workers/video_processor/python_video_processor.zip"
}

resource "aws_lambda_layer_version" "ffmpeg_python_lambda_layer" {
  filename            = "${path.module}/../lambdas/layers/pyffmpeg/source/python.zip"
  layer_name          = "ffmpeg_python_lambda_layer"
  source_code_hash    = filebase64sha256("${path.module}/../lambdas/layers/pyffmpeg/source/python.zip")

  compatible_runtimes = ["python3.8"]
}

resource "aws_lambda_layer_version" "pillow_python_lambda_layer" {
  filename            = "${path.module}/../lambdas/layers/pillow/source/python.zip"
  layer_name          = "pillow_python_lambda_layer"
  source_code_hash    = filebase64sha256("${path.module}/../lambdas/layers/pillow/source/python.zip")

  compatible_runtimes = ["python3.8"]
}

resource "aws_lambda_function" "video_processor" {
  function_name    = "video_processor"
  architectures    = ["arm64"]
  filename         = data.archive_file.python_video_processor_lambda_package.output_path
  source_code_hash = data.archive_file.python_video_processor_lambda_package.output_base64sha256
  role             = aws_iam_role.iam_for_lambda.arn
  handler          = "app.lambda_handler"
  runtime          = "python3.8"
  timeout          = 30
  layers           = [
    aws_lambda_layer_version.ffmpeg_python_lambda_layer.arn,
    aws_lambda_layer_version.pillow_python_lambda_layer.arn
  ]
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

resource "aws_iam_role_policy_attachment" "lambda_s3" {
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_s3.arn
}

# Lambda <-> Cloudwatch
# This is to optionally manage the CloudWatch Log Group for the Lambda Function.
# If skipping this resource configuration, also add "logs:CreateLogGroup" to the IAM policy below.
resource "aws_cloudwatch_log_group" "example" {
  name              = "/aws/lambda/${aws_lambda_function.video_processor.function_name}"
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
  role       = aws_iam_role.iam_for_lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}
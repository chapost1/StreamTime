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
    // sqs
    new_video_on_s3_queue = "new-video-on-s3-queue"
    // s3
    s3_registered_videos_prefix = "registered-videos"
    s3_unprocessed_videos_prefix = "unprocessed-videos"
    s3_unregistered_videos_prefix = "unregistered-videos"
    s3_thumbnails_prefix = "thumbnails"
    s3_tmp_thumbnails_prefix = "tmp-thumbnails"
    s3_thumbnails_acl = "public-read"
    s3_max_video_file_size_in_bytes = "2e+9" # 2GB
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
    id = "unprocessed-videos"
    
    expiration {
      days = 1
    }

    filter {
      and {
        prefix = "${local.s3_unprocessed_videos_prefix}/"

        tags = {
          rule      = "unprocessed-videos"
          autoclean = "true"
        }
      }
    }

    status = "Enabled"
  }
  rule {
    id = "unregistered-videos"
    
    expiration {
      days = 1
    }

    filter {
      and {
        prefix = "${local.s3_unregistered_videos_prefix}/"

        tags = {
          rule      = "unregistered-videos"
          autoclean = "true"
        }
      }
    }

    status = "Enabled"
  }

  rule {
    id = "registered-videos"

    filter {
      and {
        prefix = "${local.s3_registered_videos_prefix}/"

        tags = {
          rule      = "registered-videos"
          autoclean = "true"
        }
      }
    }

    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days = 60
      storage_class = "INTELLIGENT_TIERING"
    }
  }

  rule {
    id = "tmp-thumbnails"

    expiration {
      days = 1
    }

    filter {
      and {
        prefix = "${local.s3_tmp_thumbnails_prefix}/"

        tags = {
          rule      = "tmp-thumbnails"
          autoclean = "true"
        }
      }
    }

    status = "Enabled"
  }

  rule {
    id = "thumbnails"

    status = "Enabled"

    filter {
      and {
        prefix = "${local.s3_thumbnails_prefix}/"

        tags = {
          rule      = "thumbnails"
          autoclean = "true"
        }
      }
    }

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }

    transition {
      days          = 60
      storage_class = "GLACIER_IR"
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
    lambda_function_arn = aws_lambda_function.new_video_processing.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "${local.s3_unprocessed_videos_prefix}/"
  }

  depends_on = [
    aws_s3_bucket.videos_bucket,
    aws_lambda_function.new_video_processing
  ]
}

///// Lambdas

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
  source_arn    = "arn:aws:s3:::${aws_s3_bucket.videos_bucket.id}"
}

resource "aws_lambda_layer_version" "ffmpeg_python_lambda_layer" {
  filename            = "${path.module}/../lambdas/layers/pyffmpeg/source/python.zip"
  layer_name          = "ffmpeg_python_lambda_layer"
  source_code_hash    = filebase64sha256("${path.module}/../lambdas/layers/pyffmpeg/source/python.zip")

  compatible_runtimes = ["python3.8"]
}

data "archive_file" "python_new_video_processing_lambda_package" {  
  type        = "zip"  
  source_file = "${path.module}/../lambdas/workers/new_video_processing/app.py" 
  output_path = "${path.module}/../lambdas/workers/new_video_processing/python.zip"
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
      s3_thumbnails_prefix = local.s3_thumbnails_prefix,
      s3_unregistered_videos_prefix = local.s3_unregistered_videos_prefix,
      s3_unprocessed_videos_prefix = local.s3_unprocessed_videos_prefix,
      s3_thumbnails_acl = local.s3_thumbnails_acl,
      s3_max_video_file_size_in_bytes = local.s3_max_video_file_size_in_bytes
    }
  }
}

data "archive_file" "python_image_resizer_lambda_package" {  
  type        = "zip"  
  source_file = "${path.module}/../lambdas/workers/image_resizer/app.py" 
  output_path = "${path.module}/../lambdas/workers/image_resizer/python.zip"
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
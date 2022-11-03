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

resource "aws_lambda_permission" "video_processor_lambda_s3_invoke_permission" {
  statement_id  = "AllowS3Invoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.new_video_processing.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${var.s3_videos_bucket_id}"
}

resource "aws_iam_policy" "invoke_image_resizer_lambda_policy" {
  name        = "invoke_image_resizer_lambda_policy"
  path        = "/"
  description = "IAM policy to invoke video thumbnail lambda"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "lambda:InvokeFunction",
          "lambda:InvokeAsync"
        ]
        "Resource" : "${var.image_resizer_arn}"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "new_video_processing_lambda_invoke_lambda_policy" {
  role       = aws_iam_role.iam_for_new_video_processing_lambda.name
  policy_arn = aws_iam_policy.invoke_image_resizer_lambda_policy.arn
}

resource "aws_iam_policy" "lambda_s3_videos_bucket" {
  name        = "lambda_s3"
  path        = "/"
  description = "IAM policy for s3 videos bucket operations from new videos processing lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
            "s3:*"
      ],
      "Resource": "${var.s3_videos_bucket_arn}/*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "new_video_processing_lambda_s3" {
  role       = aws_iam_role.iam_for_new_video_processing_lambda.name
  policy_arn = aws_iam_policy.lambda_s3_videos_bucket.arn
}

// lambda sns premissions

resource "aws_iam_policy" "new_video_processing_lambda_sns" {
  name        = "new_video_processing_lambda_sns"
  path        = "/"
  description = "IAM policy for sns operations from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
            "SNS:Publish"
      ],
      "Resource": "${var.uploaded_videos_client_sync_sns_topic_arn}",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "new_video_processing_lambda_sns" {
  role       = aws_iam_role.iam_for_new_video_processing_lambda.name
  policy_arn = aws_iam_policy.new_video_processing_lambda_sns.arn
}

// lambda dynamodb premissions
resource "aws_iam_policy" "new_video_processing_lambda_dynamodb" {
  name        = "new_video_processing_lambda_dynamodb"
  path        = "/"
  description = "IAM policy for dynamodb operations from a lambda on specific tables"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadWriteTableItems",
      "Action": [
				"dynamodb:*"
      ],
      "Resource": [
        "${var.drafts_videos_dynamodb_table_arn}",
        "${var.unprocessed_videos_dynamodb_table_arn}"
      ],
      "Effect": "Allow"
    }
  ]
}
EOF
}
resource "aws_iam_role_policy_attachment" "new_video_processing_lambda_dynamodb" {
  role       = aws_iam_role.iam_for_new_video_processing_lambda.name
  policy_arn = aws_iam_policy.new_video_processing_lambda_dynamodb.arn
}

# Lambda <-> Cloudwatch
# This is to optionally manage the CloudWatch Log Group for the Lambda Function.
# If skipping this resource configuration, also add "logs:CreateLogGroup" to the IAM policy below.
resource "aws_cloudwatch_log_group" "new_video_processing_lambda_cloudwatch_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.new_video_processing.function_name}"
  retention_in_days = 14
}

# See also the following AWS managed policy: AWSLambdaBasicExecutionRole
resource "aws_iam_policy" "new_video_processing_lambda_cloudwatch_logging" {
  name        = "new_video_processing_lambda_cloudwatch_logging"
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

resource "aws_iam_role_policy_attachment" "new_video_processing_lambda_cloudwatch_logs" {
  role       = aws_iam_role.iam_for_new_video_processing_lambda.name
  policy_arn = aws_iam_policy.new_video_processing_lambda_cloudwatch_logging.arn
}

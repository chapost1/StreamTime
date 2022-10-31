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

resource "aws_iam_policy" "lambda_s3_global" {
  name        = "lambda_s3_global"
  path        = "/"
  description = "IAM policy for global s3 operations from image resizer lambda"

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

resource "aws_iam_role_policy_attachment" "image_resizer_lambda_s3" {
  role       = aws_iam_role.iam_for_image_resizer_lambda.name
  policy_arn = aws_iam_policy.lambda_s3_global.arn
}

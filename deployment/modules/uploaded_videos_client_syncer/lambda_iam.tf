data "aws_iam_policy_document" "videos_websocket_maintainer_lambda_fn_assume_role" {
  statement {
    actions = [
      "sts:AssumeRole",
    ]
    effect = "Allow"

    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "videos_websocket_maintainer_lambda" {
  name               = "${var.app_name}-ws-maintainer-lambda-iam-role"
  assume_role_policy = data.aws_iam_policy_document.videos_websocket_maintainer_lambda_fn_assume_role.json
}

# Allow lambda to write to CloudFront Logs
resource "aws_iam_role_policy_attachment" "videos_websocket_maintainer_lambda" {
  role       = aws_iam_role.videos_websocket_maintainer_lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# These are our permissions, we are using S3 objects to store the state of our Websockets
data "aws_iam_policy_document" "lambda_allow_rw_connection_store" {
  # Create/Read Websocket connection ID objects
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject"
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.videos_sync_websocket_connection_store.bucket}/${var.connection_store_prefix}/*",
    ]
  }
  # List all of the Websocket connection ID objects
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.videos_sync_websocket_connection_store.bucket}",
    ]
  }

  # Send a message to Websocket clients via "execute-api", a component of API Gateway
  statement {
    effect = "Allow"
    actions = [
      "execute-api:ManageConnections"
    ]
    resources = [
      "${aws_apigatewayv2_api.videos_websocket_maintainer.execution_arn}/*"
    ]
  }
}

resource "aws_iam_policy" "lambda_rw_connection_store" {
  name   = "${var.app_name}-ws-maintainer-lambda-allow-rw-connection-store"
  policy = data.aws_iam_policy_document.lambda_allow_rw_connection_store.json
}

resource "aws_iam_role_policy_attachment" "lambda_rw_connection_store" {
  policy_arn = aws_iam_policy.lambda_rw_connection_store.arn
  role       = aws_iam_role.videos_websocket_maintainer_lambda.name
}

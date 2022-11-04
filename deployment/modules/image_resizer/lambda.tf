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
  layers = [
    # PILLOW, source: https://github.com/keithrozario/Klayers/tree/master/deployments/python3.8
    "arn:aws:lambda:eu-west-1:770693421928:layer:Klayers-p38-Pillow:5"
  ]

  tags = {
    Name = "${var.app_name}-image-resizer-lambda-layer"
  }
}

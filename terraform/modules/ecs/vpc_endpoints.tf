resource "aws_vpc_endpoint" "s3" {
  vpc_id       = var.vpc_id
  service_name = "com.amazonaws.${var.aws_region}.s3"
}

resource "aws_vpc_endpoint" "dynamoDB" {
  vpc_id       = var.vpc_id
  service_name = "com.amazonaws.${var.aws_region}.dynamodb"
}

resource "aws_vpc_endpoint" "rds" {
  vpc_id       = var.vpc_id
  service_name = "com.amazonaws.${var.aws_region}.rds"
  vpc_endpoint_type = "Interface"
}

resource "aws_vpc_endpoint" "ecr_dkr" {
  vpc_id       = var.vpc_id
  service_name = "com.amazonaws.${var.aws_region}.ecr.dkr"
  vpc_endpoint_type = "Interface"
}

resource "aws_vpc_endpoint" "ecr_api" {
  vpc_id       = var.vpc_id
  service_name = "com.amazonaws.${var.aws_region}.ecr.api"
  vpc_endpoint_type = "Interface"
}

resource "aws_vpc_endpoint" "sns" {
  vpc_id       = var.vpc_id
  service_name = "com.amazonaws.${var.aws_region}.sns"
  vpc_endpoint_type = "Interface"
}

resource "aws_vpc_endpoint" "lambda" {
  vpc_id       = var.vpc_id
  service_name = "com.amazonaws.${var.aws_region}.lambda"
  vpc_endpoint_type = "Interface"
}

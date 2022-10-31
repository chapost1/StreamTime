variable "app_name" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "web_api_port" {
  type = number
}

variable "web_api_private_subnet" {
  type = any
}

variable "web_api_public_subnet" {
  type = any
}

variable "vpc_id" {
  type = string
}

variable "web_api_health_check" {
  type = string
}
variable "ecr_token_proxy_endpoint" {
  type = string
}
variable "ecr_token_password" {
  type = string
}
variable "ecr_authorization_token" {
  type = any
}
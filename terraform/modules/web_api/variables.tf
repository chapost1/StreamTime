variable "ecr_token_proxy_endpoint" {
  type = string
}
variable "ecr_token_password" {
  type = string
}
variable "ecr_authorization_token" {
  type = any
}

variable "app_name" {
  type = string
}

variable "vpc" {
  type = any
}

variable "public_subnet" {
  type = any
}

variable "private_subnet" {
  type = any
}

variable "az_count" {
  type = number
}

variable "app_port" {
  type = number
}

variable "health_check_path" {
  type = string
}

variable "app_count" {
  type = number
}

variable "aws_region" {
  type = string
}

variable "repository_name" {
  type = string
}

variable "image_tag" {
  type = string
}

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

variable "zone_domain" {
  type = string
}

variable "domain" {
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

variable "aws_access_key" {
  type = string
}

variable "aws_secret_key" {
  type = string
}

variable "videos_bucket" {
  type = string
}

variable "videos_bucket_arn" {
  type = string
}

variable "uploaded_videos_refix" {
  type = string
}

variable "repository_name" {
  type = string
}

variable "image_tag" {
  type = string
}

variable "rds_address" {
  type = string
}

variable "rds_username" {
  type = string
}

variable "rds_password" {
  type = string
}

variable "rds_port" {
  type = string
}

variable "rds_db" {
  type = string
}

variable "uploaded_videos_client_sync_ws_url" {
  type = string
}

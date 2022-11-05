variable "aws_access_key" {
  type        = string
  description = "AWS Access key"
}

variable "aws_secret_key" {
  type        = string
  description = "AWS Secret Key"
}

variable "app_name" {
  type        = string
  description = "App Name"
}

variable "domain" {
  type        = string
  description = "Registered Route53 Domain Name"
}

variable "db_name" {
  type        = string
  description = "RDS Database Name"
}

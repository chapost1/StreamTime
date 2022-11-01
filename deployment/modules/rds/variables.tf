variable "app_name" {
  type = string
}

variable "identifier" {
  type = string
}

variable "vpc_private_subnet" {
  type = any
}

variable "port" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "db_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "allow_security_groups" {
  type = any
}

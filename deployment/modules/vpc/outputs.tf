output "vpc" {
  value = aws_vpc._
}

output "private_subnet" {
  value = aws_subnet.private
}

output "public_subnet" {
  value = aws_subnet.public
}

output "cidr_block" {
  value = var.cidr_block
}

output "az_count" {
  value = var.az_count
}

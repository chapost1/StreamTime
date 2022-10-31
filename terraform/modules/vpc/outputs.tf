output "vpc" {
    value = aws_vpc.aws-vpc
}

output "private_subnet" {
    value = aws_subnet.private
}


output "public_subnet" {
    value = aws_subnet.public
}


output "cidr_block" {
    value = "10.10.0.0/16"
}
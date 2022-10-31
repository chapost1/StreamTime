output "rds_arn" {
    value = aws_db_instance._.arn
}

output "rds_endpoint" {
    value = aws_db_instance._.endpoint
}

output "rds_address" {
    value = aws_db_instance._.address
}

output "rds_id" {
    value = aws_db_instance._.id
}

output "rds_port" {
    value = aws_db_instance._.port
}

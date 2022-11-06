output "arn" {
  value = aws_lambda_function.videos_rds_update.arn
}

output "rds_lambda_sg" {
  value = aws_security_group.rds_lambda_sg.id
}

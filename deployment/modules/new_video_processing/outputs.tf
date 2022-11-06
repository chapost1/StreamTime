output "arn" {
  value = aws_lambda_function.new_video_processing.arn
}

# output "rds_lambda_sg" {
#   value = aws_security_group.rds_lambda_sg.id
# }

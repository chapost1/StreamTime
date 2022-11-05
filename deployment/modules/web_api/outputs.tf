output "web_api_hostname" {
  value = "https://${aws_route53_record.web_api.fqdn}"
}

output "web_api_ecs_sg" {
  value = aws_security_group.web_api_ecs_sg.id
}

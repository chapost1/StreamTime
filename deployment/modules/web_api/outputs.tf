output "web_api_alb_hostname" {
  value = aws_alb.web_api_alb.dns_name
}

output "web_api_ecs_sg" {
  value = aws_security_group.web_api_ecs_sg.id
}

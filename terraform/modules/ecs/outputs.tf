output "web_api_alb_dns_name" {
  value = aws_alb.web_api_application_load_balancer.dns_name
}

output "web_api_alb_hostname" {
  value = aws_alb.web_api_alb.dns_name
}

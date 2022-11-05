data "aws_route53_zone" "zone" {
  name         = var.zone_domain
  private_zone = false
}

resource "aws_acm_certificate" "web_api_certificate" {
  domain_name       = var.domain
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_dns" {
  for_each = {
    for dvo in aws_acm_certificate.web_api_certificate.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 300
  type            = each.value.type
  zone_id         = data.aws_route53_zone.zone.zone_id
}

resource "aws_acm_certificate_validation" "web_api_certificate_validation" {
  certificate_arn         = aws_acm_certificate.web_api_certificate.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_dns : record.fqdn]
}

resource "aws_route53_record" "web_api" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = var.domain
  type    = "A"

  alias {
    name                   = aws_alb.web_api_alb.dns_name
    zone_id                = aws_alb.web_api_alb.zone_id
    evaluate_target_health = true
  }
}

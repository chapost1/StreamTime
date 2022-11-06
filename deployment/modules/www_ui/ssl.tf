provider "aws" {
  alias = "acm_provider"
}


data "aws_route53_zone" "zone" {
  name         = var.zone_domain
  private_zone = false
}

resource "aws_route53_record" "www-a" {
  zone_id = data.aws_route53_zone.zone.zone_id
  name    = var.domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.www_s3_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.www_s3_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}

# SSL Certificate
resource "aws_acm_certificate" "www_ui_certificate" {
  provider          = aws.acm_provider
  domain_name       = var.domain
  validation_method = "DNS"
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_route53_record" "cert_dns" {
  for_each = {
    for dvo in aws_acm_certificate.www_ui_certificate.domain_validation_options : dvo.domain_name => {
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

resource "aws_acm_certificate_validation" "www_ui_cert_validation" {
  provider                = aws.acm_provider
  certificate_arn         = aws_acm_certificate.www_ui_certificate.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_dns : record.fqdn]
}

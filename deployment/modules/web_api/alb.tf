resource "aws_alb" "web_api_alb" {
  name            = "${var.app_name}-web-api-alb"
  subnets         = var.public_subnet.*.id
  security_groups = [aws_security_group.web_api_alb_sg.id]
}

resource "random_id" "LB" {
  keepers = {
    name        = "${var.app_name}-lb"
    port        = "${var.app_port}"
    protocol    = "HTTP"
    vpc_id      = var.vpc.id
    target_type = "ip"
  }
  byte_length = 2
}

resource "aws_alb_target_group" "web_api_tg" {
  name        = "${var.app_name}-api-tg-${random_id.LB.hex}"
  port        = var.app_port
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc.id

  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 2
    timeout             = 3
    protocol            = "HTTP"
    matcher             = "200"
    path                = var.health_check_path
    interval            = 30
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_alb_listener" "web_api_http" {
  depends_on = [
    aws_alb.web_api_alb,
    aws_alb_target_group.web_api_tg
  ]

  load_balancer_arn = aws_alb.web_api_alb.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    target_group_arn = aws_alb_target_group.web_api_tg.arn
    type             = "forward"
  }
}

resource "aws_alb_listener" "web_api_https" {
  depends_on = [
    aws_alb.web_api_alb,
    aws_alb_target_group.web_api_tg,
    aws_acm_certificate.web_api_certificate,
    aws_acm_certificate_validation.web_api_certificate_validation
  ]
  load_balancer_arn = aws_alb.web_api_alb.arn
  port              = 443
  protocol          = "HTTPS"
  certificate_arn   = aws_acm_certificate.web_api_certificate.arn
  default_action {
    target_group_arn = aws_alb_target_group.web_api_tg.arn
    type             = "forward"
  }
}

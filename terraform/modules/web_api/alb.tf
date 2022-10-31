resource "aws_alb" "web_api_alb" {
  name            = "${var.app_name}-web-api-load-balancer"
  subnets         = var.public_subnet.*.id
  security_groups = [aws_security_group.web_api_alb_sg.id]
}

resource "random_id" "LB" {
  keepers = {
    name        = "${var.app_name}-lb"
    protocol    = "HTTP"
    vpc_id      = var.vpc.id
    target_type = "ip"
  }
  byte_length = 4
}

resource "aws_alb_target_group" "web_api_tg" {
  name        = "${var.app_name}-web-api-tg-${random_id.LB.hex}"
  port        = 80
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
  load_balancer_arn = aws_alb.web_api_alb.arn
  port              = var.app_port

  default_action {
    type             = "forward"
    target_group_arn = aws_alb_target_group.web_api_tg.arn
  }
}

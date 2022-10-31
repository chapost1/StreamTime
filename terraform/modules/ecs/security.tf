resource "aws_security_group" "web_api_service_security_group" {
  vpc_id = var.vpc_id

  ingress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.web_api_load_balancer_security_group.id]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "${local.web_api_prefix}-service-sg"
  }
}

resource "aws_alb" "web_api_application_load_balancer" {
  name               = "${local.web_api_prefix}-alb"
  internal           = false
  load_balancer_type = "application"
  subnets            = var.web_api_public_subnet.*.id
  security_groups    = [aws_security_group.web_api_load_balancer_security_group.id]

  tags = {
    Name = "${local.web_api_prefix}-alb"
  }
}

resource "aws_security_group" "web_api_load_balancer_security_group" {
  vpc_id = var.vpc_id

  ingress {
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  tags = {
    Name = "${local.web_api_prefix}-sg"
  }
}

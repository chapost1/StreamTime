resource "aws_security_group" "web_api_alb_sg" {
  name        = "${var.app_name}-load-balancer-security-group"
  description = "controls access to the ALB"
  vpc_id      = var.vpc.id

  ingress {
    protocol    = "tcp"
    from_port   = 80
    to_port     = 80
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow incoming HTTP connections"
  }

  ingress {
    protocol    = "tcp"
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow incoming HTTPS connections"
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "web_api_ecs_sg" {
  name        = "${var.app_name}-ecs_tasks-security-group"
  description = "allow inbound access from the ALB only"
  vpc_id      = var.vpc.id

  ingress {
    protocol        = "tcp"
    from_port       = 80
    to_port         = 80
    security_groups = [aws_security_group.web_api_alb_sg.id]
    description     = "Allow incoming HTTP connections"
  }

  ingress {
    protocol        = "tcp"
    from_port       = 443
    to_port         = 443
    security_groups = [aws_security_group.web_api_alb_sg.id]
    description     = "Allow incoming HTTPS connections"
  }

  egress {
    protocol    = "-1"
    from_port   = 0
    to_port     = 0
    cidr_blocks = ["0.0.0.0/0"]
  }
}

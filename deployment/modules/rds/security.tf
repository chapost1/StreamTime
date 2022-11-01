resource "aws_security_group" "_" {
  name = "${local.resource_name_prefix}-rds-sg"

  description = "RDS Cluster"
  vpc_id      = var.vpc_id

  # Only db port in
  ingress {
    from_port       = var.port
    to_port         = var.port
    protocol        = "tcp"
    cidr_blocks     = ["10.10.0.0/24"]
    security_groups = var.allow_security_groups
  }

  # Allow all outbound traffic.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.resource_name_prefix}-rds-sg"
  }
}

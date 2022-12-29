locals {
  resource_name_prefix = "${var.app_name}-rds"
}

resource "aws_db_subnet_group" "_" {
  name       = "${local.resource_name_prefix}-subnet-group"
  subnet_ids = var.vpc_private_subnet.*.id

  tags = {
    Name = "${local.resource_name_prefix}-subnet-group"
  }
}

resource "random_string" "videos_rds_username" {
  length  = 4
  lower   = true
  special = false
  numeric = false
}

resource "random_string" "videos_rds_password" {
  length  = 16
  special = false
}

resource "random_id" "id" {
  byte_length = 4
}

# secret to store the password
resource "aws_secretsmanager_secret" "db_pass" {
  name = "db-pass-${random_id.id.hex}"
}

# initial value
resource "aws_secretsmanager_secret_version" "db_pass_val" {
  secret_id = aws_secretsmanager_secret.db_pass.id
  secret_string = jsonencode(
    {
      username = aws_rds_cluster.cluster.master_username
      password = random_string.videos_rds_password.result
      engine   = "postgres"
      host     = aws_rds_cluster.cluster.endpoint
    }
  )
}

# rds cluster
resource "aws_rds_cluster" "cluster" {
  cluster_identifier   = "${var.identifier}-cluster"
  engine               = "aurora-postgresql"
  engine_version       = "11.13"
  engine_mode          = "serverless"
  database_name        = var.db_name
  master_username      = random_string.videos_rds_username.result
  master_password      = random_string.videos_rds_password.result
  enable_http_endpoint = true
  skip_final_snapshot  = true
  port                 = var.port

  preferred_backup_window      = "01:30-02:00"
  preferred_maintenance_window = "Mon:03:00-Mon:05:00"
  backup_retention_period      = 1

  final_snapshot_identifier = "${var.identifier}-snapshots" # name of the final snapshot after deletion
  snapshot_identifier       = null                          # used to recover from a snapshot

  vpc_security_group_ids = [aws_security_group._.id]
  db_subnet_group_name   = aws_db_subnet_group._.name

  db_cluster_parameter_group_name = aws_rds_cluster_parameter_group.default.name

  scaling_configuration {
    min_capacity = 2.0
  }

  tags = {
    Name = "${var.identifier}"
  }
}

resource "aws_rds_cluster_parameter_group" "default" {
  name        = "rds-cluster-pg"
  family      = "aurora-postgresql11"
  description = "RDS default cluster parameter group"

  parameter {
    name  = "log_statement"
    value = "mod"
  }
}

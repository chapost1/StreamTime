resource "local_file" "aws_rds_secrets" {
  content = jsonencode({
    REGION     = var.aws_region
    SECRET_ARN = aws_secretsmanager_secret.db_pass.arn
    SECRET_ID  = aws_secretsmanager_secret.db_pass.id
    DB_NAME    = var.db_name
    DB_ARN     = aws_rds_cluster.cluster.arn
    DB_USER    = aws_rds_cluster.cluster.master_username
    DB_PASS    = random_string.videos_rds_password.result
  })
  filename = "${path.module}/db_secrets.json"

  depends_on = [
    aws_secretsmanager_secret.db_pass,
    aws_rds_cluster.cluster,
    random_string.videos_rds_password
  ]
}

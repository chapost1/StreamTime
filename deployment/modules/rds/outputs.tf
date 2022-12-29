output "rds_arn" {
  value = aws_rds_cluster.cluster.arn
}

output "rds_endpoint" {
  value = aws_rds_cluster.cluster.endpoint
}

output "rds_id" {
  value = aws_rds_cluster.cluster.id
}

output "rds_port" {
  value = aws_rds_cluster.cluster.port
}

output "rds_username" {
  value = aws_rds_cluster.cluster.master_username
}

output "rds_password" {
  value = random_string.videos_rds_password.result
}

output "db_name" {
  value = var.db_name
}

output "rds_cluster_identifier" {
  value = aws_rds_cluster.cluster.cluster_identifier
}

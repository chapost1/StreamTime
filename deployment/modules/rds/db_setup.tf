# used when mode is db_op=init
resource "null_resource" "db_setup" {
  triggers = {
    file = filesha1("${path.module}/ddl/init_id.txt")
  }
  provisioner "local-exec" {
    command = <<-EOF
			while read line; do
				echo "$line"
				aws rds-data execute-statement --resource-arn "$DB_ARN" --database  "$DB_NAME" --secret-arn "$SECRET_ARN" --sql "$line" \
                                               --region "$REGION"
			done  < <(awk 'BEGIN{RS=";\n"}{gsub(/\n/,""); if(NF>0) {print $0";"}}' ./modules/rds/ddl/init.sql)
			EOF
    environment = {
      REGION     = var.aws_region
      DB_ARN     = aws_rds_cluster.cluster.arn
      DB_NAME    = var.db_name
      SECRET_ARN = aws_secretsmanager_secret.db_pass.arn
    }
    interpreter = ["bash", "-c"]
  }
  depends_on = [
    aws_rds_cluster.cluster
  ]
}

# used when mode is db_op=patch
resource "null_resource" "db_patching" {
  triggers = {
    file = filesha1("${path.module}/ddl/patch_id.txt")
  }
  provisioner "local-exec" {
    command = <<-EOF
			while read line; do
				echo "$line"
				aws rds-data execute-statement --resource-arn "$DB_ARN" --database  "$DB_NAME" --secret-arn "$SECRET_ARN" --sql "$line" \
                                               --region "$REGION"
			done  < <(awk 'BEGIN{RS=";\n"}{gsub(/\n/,""); if(NF>0) {print $0";"}}' ./modules/rds/ddl/patch.sql)
			EOF
    environment = {
      REGION     = var.aws_region
      DB_ARN     = aws_rds_cluster.cluster.arn
      DB_NAME    = var.db_name
      SECRET_ARN = aws_secretsmanager_secret.db_pass.arn
    }
    interpreter = ["bash", "-c"]
  }
  depends_on = [
    null_resource.db_setup
  ]
}


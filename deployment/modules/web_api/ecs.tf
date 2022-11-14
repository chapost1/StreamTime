locals {
  fargate_cpu    = "256"
  fargate_memory = "512"
}

resource "aws_ecs_cluster" "web_api_cluster" {
  name = "${var.app_name}-web-api-cluster"
}

data "template_file" "web_api" {
  template = file("${path.module}/templates/image.json")

  vars = {
    env_health_check_path = "${var.health_check_path}"
    env_rds_address       = var.rds_address
    env_rds_password      = var.rds_password
    env_rds_username      = var.rds_username
    env_rds_port          = var.rds_port
    env_rds_db            = var.rds_db

    env_videos_bucket          = var.videos_bucket
    env_uploaded_videos_prefix = var.uploaded_videos_refix

    env_image_hash = random_id.ecr_image_hash.hex

    env_app_port           = tostring(var.app_port)
    env_aws_region         = var.aws_region
    env_logs_stream_prefix = "${aws_cloudwatch_log_group.web_api_log_group.name}"
    env_logs_group         = "${aws_cloudwatch_log_group.web_api_log_group.id}"
    env_image              = "${aws_ecr_repository.web_api_aws_ecr.repository_url}:${var.image_tag}"
    env_name               = "${var.app_name}-web-api"
    env_cpu                = local.fargate_cpu
    env_memory             = local.fargate_memory
  }

  depends_on = [
    aws_ecr_repository.web_api_aws_ecr
  ]
}

resource "aws_ecs_task_definition" "web_api_def" {
  family                   = "${var.app_name}-web-api-task"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = local.fargate_cpu
  memory                   = local.fargate_memory
  container_definitions    = data.template_file.web_api.rendered
}

resource "aws_ecs_service" "web_api_service" {
  name                 = "${var.app_name}-web-api-service"
  cluster              = aws_ecs_cluster.web_api_cluster.id
  task_definition      = aws_ecs_task_definition.web_api_def.arn
  desired_count        = var.app_count
  launch_type          = "FARGATE"
  force_new_deployment = true

  network_configuration {
    security_groups  = [aws_security_group.web_api_ecs_sg.id]
    subnets          = var.private_subnet.*.id
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_alb_target_group.web_api_tg.arn
    container_name   = "${var.app_name}-web-api"
    container_port   = var.app_port
  }

  depends_on = [
    aws_alb_listener.web_api_http,
    aws_iam_role_policy_attachment.ecs_task_execution_role
  ]
}

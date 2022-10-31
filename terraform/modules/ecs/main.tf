locals {
  web_api_prefix    = "${var.app_name}-web-api"
  web_api_image_tag = "latest"
  web_api_env_json_map = jsonencode([
    { name = "health_check_endpoint", valueFrom = var.web_api_health_check },
    { name = "port", valueFrom = tostring(var.web_api_port) },
  ])
}

module "ecr" {
  source     = "../ecr"
  app_name   = var.app_name
  identifier = "web-api"
}

resource "aws_iam_role" "web_api_ecs_task_execution_role" {
  name               = "${local.web_api_prefix}-execution-task-role"
  assume_role_policy = data.aws_iam_policy_document.web_api_ecs_assume_role_policy.json
  tags = {
    Name = "${local.web_api_prefix}-ecs-task-execution-iam-role"
  }
}

data "aws_iam_policy_document" "web_api_ecs_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}
# Allow ECS to access ECR
resource "aws_iam_role_policy_attachment" "web_api_ecs_task_execution_role_policy" {
  role       = aws_iam_role.web_api_ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2ContainerServiceforEC2Role"
}

# Allow ECS to access S3
resource "aws_iam_policy" "web_api_ecs_task_use_s3" {
  name        = "web_api_ecs_task_use_s3"
  path        = "/"
  description = "IAM policy to s3 full access"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
            "s3:*"
      ],
      "Resource": "arn:aws:s3:::*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "web_api_s3_policy_attaching" {
  role       = aws_iam_role.web_api_ecs_task_execution_role.name
  policy_arn = aws_iam_policy.web_api_ecs_task_use_s3.arn
}

# Allow ECS to access RDS
resource "aws_iam_policy" "web_api_ecs_task_use_rds" {
  name        = "web_api_ecs_task_use_rds"
  path        = "/"
  description = "IAM policy to rds full access"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
            "rds:CreateDBInstance",
            "rds:ModifyDBInstance",
            "rds:CreateDBSnapshot"
      ],
      "Resource": "*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "web_api_rds_policy_attaching" {
  role       = aws_iam_role.web_api_ecs_task_execution_role.name
  policy_arn = aws_iam_policy.web_api_ecs_task_use_rds.arn
}

# Allow ECS to access dynamodb
resource "aws_iam_policy" "web_api_ecs_task_use_dynamodb" {
  name        = "web_api_ecs_task_use_dynamodb"
  path        = "/"
  description = "IAM policy to dynamodb full access"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
            "dynamodb:*"
      ],
      "Resource": "arn:aws:dynamodb:::*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "web_api_dynamodb_policy_attaching" {
  role       = aws_iam_role.web_api_ecs_task_execution_role.name
  policy_arn = aws_iam_policy.web_api_ecs_task_use_dynamodb.arn
}

resource "aws_ecs_cluster" "web-api-aws-ecs-cluster" {
  name = "${local.web_api_prefix}-cluster"
  tags = {
    Name = "${local.web_api_prefix}-ecs-cluster"
  }
}

# add containers logs to CW 
resource "aws_cloudwatch_log_group" "web-api-log-group" {
  name = "${local.web_api_prefix}-logs"

  tags = {
    Name = "${local.web_api_prefix}"
  }
}

resource "aws_ecs_task_definition" "web_api_ecs_task" {
  family = "${local.web_api_prefix}-task"
  // see this: https://stackoverflow.com/questions/64113109/take-ecs-task-definition-environment-variables-from-terraform-input-variables
  container_definitions = <<DEFINITION
  [
    {
      "name": "${local.web_api_prefix}-container",
      "image": "${module.ecr.repository_url}:${local.web_api_image_tag}",
      "entryPoint": [],
      "environment": ${local.web_api_env_json_map},
      "essential": true,
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "${aws_cloudwatch_log_group.web-api-log-group.id}",
          "awslogs-region": "${var.aws_region}",
          "awslogs-stream-prefix": "${local.web_api_prefix}"
        }
      },
      "portMappings": [
        {
          "containerPort": ${tostring(var.web_api_port)},
          "hostPort": ${tostring(var.web_api_port)}
        }
      ],
      "cpu": 256,
      "memory": 512,
      "networkMode": "awsvpc"
    }
  ]
  DEFINITION

  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  memory                   = "512"
  cpu                      = "256"
  execution_role_arn       = aws_iam_role.web_api_ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.web_api_ecs_task_execution_role.arn

  tags = {
    Name = "${local.web_api_prefix}-ecs-td"
  }
}

data "aws_ecs_task_definition" "web_api_main" {
  task_definition = aws_ecs_task_definition.web_api_ecs_task.family
}

resource "aws_ecs_service" "web-api-aws-ecs-service" {
  name                 = "${local.web_api_prefix}-ecs-service"
  cluster              = aws_ecs_cluster.web-api-aws-ecs-cluster.id
  task_definition      = "${aws_ecs_task_definition.web_api_ecs_task.family}:${max(aws_ecs_task_definition.web_api_ecs_task.revision, data.aws_ecs_task_definition.web_api_main.revision)}"
  launch_type          = "FARGATE"
  scheduling_strategy  = "REPLICA"
  desired_count        = 1
  force_new_deployment = true

  network_configuration {
    subnets          = var.web_api_private_subnet.*.id
    assign_public_ip = false
    security_groups = [
      aws_security_group.web_api_service_security_group.id,
      aws_security_group.web_api_service_security_group.id
    ]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.web_api_target_group.arn
    container_name   = "${local.web_api_prefix}-container"
    container_port   = var.web_api_port
  }

  depends_on = [aws_lb_listener.web_api_listener]
}

resource "aws_lb_target_group" "web_api_target_group" {
  name        = "${local.web_api_prefix}-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = var.vpc_id

  health_check {
    healthy_threshold   = "3"
    interval            = "300"
    protocol            = "HTTP"
    matcher             = "200"
    timeout             = "3"
    path                = "/${var.web_api_health_check}"
    unhealthy_threshold = "2"
  }

  tags = {
    Name = "${local.web_api_prefix}-lb-tg"
  }
}

resource "aws_lb_listener" "web_api_listener" {
  load_balancer_arn = aws_alb.web_api_application_load_balancer.id
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.web_api_target_group.id
  }
}


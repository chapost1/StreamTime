resource "aws_appautoscaling_target" "web_api_ecs_target" {
  max_capacity       = 3
  min_capacity       = 2
  resource_id        = "service/${aws_ecs_cluster.web-api-aws-ecs-cluster.name}/${aws_ecs_service.web-api-aws-ecs-service.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "web_api_ecs_policy_memory" {
  name               = "${local.web_api_prefix}-memory-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.web_api_ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.web_api_ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.web_api_ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageMemoryUtilization"
    }

    target_value = 75
  }
}

resource "aws_appautoscaling_policy" "ecs_policy_cpu" {
  name               = "${local.web_api_prefix}-cpu-autoscaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.web_api_ecs_target.resource_id
  scalable_dimension = aws_appautoscaling_target.web_api_ecs_target.scalable_dimension
  service_namespace  = aws_appautoscaling_target.web_api_ecs_target.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }

    target_value = 70
  }
}

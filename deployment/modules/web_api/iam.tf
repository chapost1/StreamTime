data "aws_iam_policy_document" "ecs_task_execution_role" {
  version = "2012-10-17"

  statement {
    sid     = ""
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name               = "${var.app_name}-web-api-execution-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_role.json
}

resource "aws_iam_role_policy_attachment" "ecs_task_execution_role" {
  role       = aws_iam_role.ecs_task_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


resource "aws_iam_role" "ecs_task_role" {
  name               = "${var.app_name}-web-api-task-role"
  assume_role_policy = data.aws_iam_policy_document.ecs_task_execution_role.json
}

resource "aws_iam_policy" "ecs_access_s3_videos_bucket" {
  name        = "ecs_access_s3_videos_bucket"
  path        = "/"
  description = "IAM policy to let ecs access videos bucket on s3"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
            "s3:*"
      ],
      "Resource": "${var.videos_bucket_arn}/*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs_access_s3_videos_bucket" {
  role       = aws_iam_role.ecs_task_role.name
  policy_arn = aws_iam_policy.ecs_access_s3_videos_bucket.arn
}

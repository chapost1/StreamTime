///// sqs


/// videos queue
# resource "aws_sqs_queue" "new_video_queue" {
#   name = var.new_video_on_s3_queue_name
#   message_retention_seconds = 86400
#   redrive_policy = jsonencode({
#     deadLetterTargetArn = aws_sqs_queue.terraform_queue_deadletter.arn
#     maxReceiveCount     = 1
#   })

#   policy = <<POLICY
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": "*",
#       "Action": "sqs:SendMessage",
#       "Resource": "arn:aws:sqs:*:*:${var.new_video_on_s3_queue_name}",
#       "Condition": {
#         "ArnEquals": { "aws:SourceArn": "${var.s3_videos_bucket_arn}" }
#       }
#     }
#   ]
# }
# POLICY
# }

# resource "aws_sqs_queue" "terraform_queue_deadletter" {
#   name = "terraform-deadletter-queue"
#   // avoid circular dependency, aim for source queue explicitly
#   redrive_allow_policy  = jsonencode({
#     redrivePermission = "byQueue",
#     sourceQueueArns   = ["arn:aws:sqs:${var.aws_region_name}:${var.aws_account_id}:${var.new_video_on_s3_queue_name}"]
#   })  
# }

# resource "aws_s3_bucket_notification" "new_video_upload" {
#   bucket = var.s3_videos_bucket_id

#   queue {
#     queue_arn     = aws_sqs_queue.new_video_queue.arn
#     events        = ["s3:ObjectCreated:*"]
#     filter_prefix = "videos/"
#   }
# }
provider "aws" {
  region     = local.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

provider "archive" {}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_ecr_authorization_token" "token" {}

locals {
  // provider
  aws_region = "us-east-1"
  // general
  app_name = "svn-videos"
  // sqs
  new_video_on_s3_queue_name = "new-video-on-s3-queue"
  // s3
  s3_videos_prefix                = "videos"
  s3_uploaded_videos_prefix       = "uploaded-videos"
  s3_unprocessed_videos_prefix    = "unprocessed-videos"
  s3_thumbnails_prefix            = "thumbnails"
  s3_tmp_thumbnails_prefix        = "tmp-thumbnails"
  s3_thumbnails_acl               = "public-read"
  s3_max_video_file_size_in_bytes = "2e+9" # 2GB
  // new_video_processing failures
  new_video_processing_failure_internal_error         = "Internal error, please try again later"
  new_video_processing_failure_max_file_size_exceeded = "Maximum file size exceeded"
  new_video_processing_failure_corrupted              = "Corrupted/Invalid file"
  new_video_processing_failure_unsupported_video_type = "Unsupported video type"
  // new_video_processing events
  new_video_events_processing_has_been_started = "new_video_events_processing_has_been_started"
  new_video_events_processing_failure          = "new_video_events_processing_failure"
  new_video_events_moved_to_drafts             = "new_video_events_moved_to_drafts"
  // dynamoDB tables
  dynamodb_table_invoked_uploaded_videos           = "invoked_uploaded_videos"
  dynamodb_table_unprocessed_videos                = "unprocessed_videos"
  dynamodb_table_drafts_videos                     = "drafts_videos"
  dynamodb_table_processing_has_been_failed_videos = "processing_has_been_failed_videos"
  // rds
  videos_rds_username = "admin"
  videos_rds_port     = "3306"
  // web_api
  web_api_port              = 80
  web_api_health_check_path = "/health_check"
  web_api_app_count         = 2
}

resource "random_string" "videos_rds_password" {
  length  = 16
  special = false
}

///// s3 bucket
module "s3" {
  source                    = "./modules/s3"
  app_name                  = local.app_name
  uploaded_videos_prefix    = local.s3_uploaded_videos_prefix
  unprocessed_videos_prefix = local.s3_unprocessed_videos_prefix
  videos_prefix             = local.s3_videos_prefix
  thumbnails_prefix         = local.s3_thumbnails_prefix
  tmp_thumbnails_prefix     = local.s3_tmp_thumbnails_prefix
}

# ///// sqs
# module "sqs" {
#   source                     = "./modules/sqs"
#   new_video_on_s3_queue_name = local.new_video_on_s3_queue_name
#   s3_videos_bucket_arn       = module.s3.videos_bucket.arn
#   s3_videos_bucket_id        = module.s3.videos_bucket.id
#   aws_region_name            = data.aws_region.current.name
#   aws_account_id             = data.aws_caller_identity.current.account_id
# }

///// lambda
module "lambda" {
  source                                              = "./modules/lambda"
  app_name                                            = local.app_name
  s3_videos_bucket_id                                 = module.s3.videos_bucket.id
  s3_thumbnails_prefix                                = local.s3_thumbnails_prefix
  s3_videos_prefix                                    = local.s3_videos_prefix
  s3_uploaded_videos_prefix                           = local.s3_uploaded_videos_prefix
  s3_unprocessed_videos_prefix                        = local.s3_unprocessed_videos_prefix
  s3_thumbnails_acl                                   = local.s3_thumbnails_acl
  s3_max_video_file_size_in_bytes                     = local.s3_max_video_file_size_in_bytes
  new_video_processing_failure_internal_error         = local.new_video_processing_failure_internal_error
  new_video_processing_failure_max_file_size_exceeded = local.new_video_processing_failure_max_file_size_exceeded
  new_video_processing_failure_corrupted              = local.new_video_processing_failure_corrupted
  new_video_processing_failure_unsupported_video_type = local.new_video_processing_failure_unsupported_video_type
  dynamodb_table_invoked_uploaded_videos              = local.dynamodb_table_invoked_uploaded_videos
  dynamodb_table_unprocessed_videos                   = local.dynamodb_table_unprocessed_videos
  dynamodb_table_drafts_videos                        = local.dynamodb_table_drafts_videos
  dynamodb_table_processing_has_been_failed_videos    = local.dynamodb_table_processing_has_been_failed_videos
  new_video_events_processing_has_been_started        = local.new_video_events_processing_has_been_started
  new_video_events_processing_failure                 = local.new_video_events_processing_failure
  new_video_events_moved_to_drafts                    = local.new_video_events_moved_to_drafts

  depends_on = [
    module.s3.videos_bucket,
  ]
}

module "vpc" {
  source = "./modules/vpc"

  app_name = local.app_name

  cidr_block = "172.16.0.0/16"
  az_count   = 2
}

module "web_api" {
  source = "./modules/web_api"

  app_name                 = local.app_name
  aws_region               = local.aws_region
  ecr_token_proxy_endpoint = data.aws_ecr_authorization_token.token.proxy_endpoint
  ecr_token_password       = data.aws_ecr_authorization_token.token.password
  ecr_authorization_token  = data.aws_ecr_authorization_token.token
  vpc                      = module.vpc.vpc
  public_subnet            = module.vpc.public_subnet
  private_subnet           = module.vpc.private_subnet
  az_count                 = module.vpc.az_count
  app_port                 = local.web_api_port
  health_check_path        = local.web_api_health_check_path
  app_count                = local.web_api_app_count
  repository_name          = "${local.app_name}-web-api"
  image_tag                = "latest"
}


# module "rds" {
#   source            = "./modules/rds"
#   app_name          = local.app_name
#   engine            = "mysql"
#   engine_version    = "8.0.30"
#   instance_class    = "db.t2.small"
#   allocated_storage = 10
#   storage_encrypted = true
#   db_name           = "svnDB"
#   username          = local.videos_rds_username
#   password          = random_string.videos_rds_password.result

#   vpc_id                  = module.vpc.vpc.id
#   vpc_private_subnet      = module.vpc.private_subnet
#   port                    = local.videos_rds_port
#   maintenance_window      = "Mon:03:00-Mon:05:00"
#   backup_window           = "01:30-02:00"
#   backup_retention_period = 1
#   publicly_accessible     = false

#   auto_minor_version_upgrade = false

#   final_snapshot_identifier = "videos-rds-db-snapshots" # name of the final snapshot after deletion
#   snapshot_identifier       = null                      # used to recover from a snapshot
#   skip_final_snapshot       = false

#   performance_insights_enabled = false
# }

# module "ecs" {
#   source                   = "./modules/ecs"
#   app_name                 = local.app_name
#   aws_region               = local.aws_region
#   web_api_port             = local.web_api_port
#   vpc_id                   = module.vpc.vpc.id
#   web_api_private_subnet   = module.vpc.private_subnet
#   web_api_public_subnet    = module.vpc.public_subnet
#   web_api_health_check     = local.web_api_health_check
#   ecr_token_proxy_endpoint = data.aws_ecr_authorization_token.token.proxy_endpoint
#   ecr_token_password       = data.aws_ecr_authorization_token.token.password
#   ecr_authorization_token  = data.aws_ecr_authorization_token.token
# }

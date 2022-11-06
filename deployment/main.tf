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
  aws_region = "eu-west-1"
  // general
  app_name = var.app_name
  // registered domain
  domain = var.domain
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
  # rds
  rds_table_uprocessed_videos = "unprocessed_videos"
  rds_table_videos            = "videos"
  // web_api
  web_api_port              = 80
  web_api_health_check_path = "/health_check"
  web_api_app_count         = 2
  web_api_domain            = "${local.app_name}-web-api.${local.domain}"
  // videos sync websocket
  uploaded_videos_client_syncer_connection_store_prefix = "active-connections"
  uploaded_video_feedback_event                         = "uploaded_video_feedback"
}

module "videos_bucket" {
  source                    = "./modules/videos_bucket"
  app_name                  = local.app_name
  uploaded_videos_prefix    = local.s3_uploaded_videos_prefix
  unprocessed_videos_prefix = local.s3_unprocessed_videos_prefix
  videos_prefix             = local.s3_videos_prefix
  thumbnails_prefix         = local.s3_thumbnails_prefix
  tmp_thumbnails_prefix     = local.s3_tmp_thumbnails_prefix
}

module "uploaded_videos_client_syncer" {
  source = "./modules/uploaded_videos_client_syncer"

  app_name                      = local.app_name
  connection_store_prefix       = local.uploaded_videos_client_syncer_connection_store_prefix
  uploaded_video_feedback_event = local.uploaded_video_feedback_event
}

module "image_resizer" {
  source   = "./modules/image_resizer"
  app_name = local.app_name
  depends_on = [
    module.videos_bucket
  ]
}

module "new_video_processing" {
  source = "./modules/new_video_processing"

  app_name          = local.app_name
  image_resizer_arn = module.image_resizer.arn

  s3_videos_bucket_id                                 = module.videos_bucket.videos_bucket.id
  s3_videos_bucket_arn                                = module.videos_bucket.videos_bucket.arn
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

  new_video_events_processing_has_been_started = local.new_video_events_processing_has_been_started
  new_video_events_processing_failure          = local.new_video_events_processing_failure
  new_video_events_moved_to_drafts             = local.new_video_events_moved_to_drafts

  uploaded_videos_client_sync_sns_topic_arn = module.uploaded_videos_client_syncer.input_sns_topic_arn
  uploaded_video_feedback_event             = local.uploaded_video_feedback_event

  rds_host                    = module.rds.rds_endpoint
  rds_port                    = module.rds.rds_port
  rds_user                    = module.rds.rds_username
  rds_password                = module.rds.rds_password
  rds_db_name                 = module.rds.db_name
  rds_table_uprocessed_videos = local.rds_table_uprocessed_videos
  rds_table_videos            = local.rds_table_videos

  vpc            = module.vpc.vpc
  private_subnet = module.vpc.private_subnet

  depends_on = [
    module.videos_bucket.videos_bucket,
    module.image_resizer.image_resizer_arn,
    module.uploaded_videos_client_syncer.input_sns_topic_arn,
    module.rds.rds_endpoint
  ]
}

module "vpc" {
  source = "./modules/vpc"

  app_name = local.app_name

  cidr_block = "172.16.0.0/16"
  az_count   = 2
}

module "rds" {
  source     = "./modules/rds"
  app_name   = local.app_name
  identifier = "videos-rds-db"
  db_name    = var.db_name
  port       = "5432"

  aws_region            = local.aws_region
  vpc_id                = module.vpc.vpc.id
  vpc_private_subnet    = module.vpc.private_subnet
  allow_security_groups = [module.web_api.web_api_ecs_sg, module.new_video_processing.rds_lambda_sg]

  depends_on = [
    module.vpc.vpc
  ]
}

module "web_api" {
  source = "./modules/web_api"

  app_name                 = local.app_name
  zone_domain              = local.domain
  domain                   = local.web_api_domain
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

  rds_address  = module.rds.rds_endpoint
  rds_password = module.rds.rds_password
  rds_username = module.rds.rds_username
  rds_port     = module.rds.rds_port
  rds_db       = module.rds.db_name

  uploaded_videos_client_sync_ws_url = module.uploaded_videos_client_syncer.ws_url

  depends_on = [
    module.uploaded_videos_client_syncer.ws_url,
    module.uploaded_videos_client_syncer.input_sns_topic_arn
  ]
}

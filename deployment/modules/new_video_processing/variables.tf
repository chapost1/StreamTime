variable "app_name" {
  type = string
}

variable "image_resizer_arn" {
  type = string
}

variable "videos_rds_update_arn" {
  type = string
}

variable "s3_videos_bucket_id" {
  type = string
}

variable "s3_videos_bucket_arn" {
  type = string
}

variable "s3_thumbnails_prefix" {
  type = string
}

variable "s3_videos_prefix" {
  type = string
}

variable "s3_uploaded_videos_prefix" {
  type = string
}

variable "s3_unprocessed_videos_prefix" {
  type = string
}

variable "s3_thumbnails_acl" {
  type = string
}
variable "s3_max_video_file_size_in_bytes" {
  type = string
}

variable "allowed_video_types_to_extension" {
  type = string
}

variable "new_video_processing_failure_internal_error" {
  type = string
}
variable "new_video_processing_failure_max_file_size_exceeded" {
  type = string
}
variable "new_video_processing_failure_corrupted" {
  type = string
}
variable "new_video_processing_failure_unsupported_video_type" {
  type = string
}

variable "new_video_events_processing_has_been_started" {
  type = string
}
variable "new_video_events_processing_failure" {
  type = string
}
variable "new_video_events_moved_to_drafts" {
  type = string
}

variable "uploaded_videos_client_sync_sns_topic_arn" {
  type = string
}

variable "uploaded_video_feedback_event" {
  type = string
}

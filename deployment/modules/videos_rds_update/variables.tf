variable "app_name" {
  type = string
}

variable "vpc" {
  type = any
}

variable "private_subnet" {
  type = any
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

variable "rds_host" {
  type = string
}

variable "rds_port" {
  type = string
}

variable "rds_user" {
  type = string
}

variable "rds_password" {
  type = string
}

variable "rds_db_name" {
  type = string
}

variable "rds_table_uprocessed_videos" {
  type = string
}

variable "rds_table_videos" {
  type = string
}

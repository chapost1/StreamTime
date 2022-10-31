variable "app_name" {
  type = string
}
variable "vpc_private_subnet" {
  type = any
}
variable "allocated_storage" {
  type = string
}
variable "backup_retention_period" {
  type = string
}
variable "backup_window" {
  type = string
}
variable "maintenance_window" {
  type = string
}
variable "engine" {
  type = string
}
variable "engine_version" {
  type = string
}
variable "instance_class" {
  type = string
}
variable "db_name" {
  type = string
}
variable "username" {
  type = string
}
variable "password" {
  type = string
}
variable "vpc_id" {
  type = string
}
variable "port" {
  type = string
}
variable "publicly_accessible" {
  type = string
}
variable "storage_encrypted" {
  type = string
}
variable "auto_minor_version_upgrade" {
  type = string
}
variable "final_snapshot_identifier" {
  type = string
}
variable "snapshot_identifier" {
  type = string
}
variable "skip_final_snapshot" {
  type = string
}
variable "performance_insights_enabled" {
  type = string
}

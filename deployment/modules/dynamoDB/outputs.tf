output "unprocessed_videos_dynamodb_table_arn" {
  value = aws_dynamodb_table.processing_has_been_started.arn
}

output "drafts_videos_dynamodb_table_arn" {
  value = aws_dynamodb_table.drafts.arn
}

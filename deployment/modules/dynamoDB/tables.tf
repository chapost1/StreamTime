resource "aws_dynamodb_table" "processing_has_been_started" {
  name         = var.unprocessed_videos_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"
  range_key    = "upload_time"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "upload_time"
    type = "S"
  }

  ttl {
    attribute_name = "time_to_exist"
    enabled        = true
  }

  tags = {
    Name = "${var.unprocessed_videos_table_name}-dynamodb-table"
  }
}

resource "aws_dynamodb_table" "drafts" {
  name         = var.drafts_videos_table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"
  range_key    = "upload_time"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "upload_time"
    type = "S"
  }

  tags = {
    Name = "${var.drafts_videos_table_name}-dynamodb-table"
  }
}

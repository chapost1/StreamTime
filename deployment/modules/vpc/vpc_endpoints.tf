resource "aws_vpc_endpoint" "s3" {
  vpc_id = aws_vpc._.id
  service_name = "com.amazonaws.${var.region}.s3"

  route_table_ids = [aws_vpc._.main_route_table_id]
}
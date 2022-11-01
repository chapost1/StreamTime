
resource "aws_internet_gateway" "web_api_igw" {
  vpc_id = var.vpc.id
}

// for web api
resource "aws_route" "vpc_internet_access" {
  route_table_id         = var.vpc.main_route_table_id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.web_api_igw.id
}

resource "aws_eip" "web_api_eip" {
  count      = var.az_count
  vpc        = true
  depends_on = [aws_internet_gateway.web_api_igw]
}

resource "aws_nat_gateway" "web_api_natgw" {
  count         = var.az_count
  subnet_id     = element(var.public_subnet.*.id, count.index)
  allocation_id = element(aws_eip.web_api_eip.*.id, count.index)
}

resource "aws_route_table" "private" {
  count  = var.az_count
  vpc_id = var.vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = element(aws_nat_gateway.web_api_natgw.*.id, count.index)
  }
}

locals {
    availability_zones = ["us-east-1a", "us-east-1b"]

    public_subnets = ["10.10.100.0/24", "10.10.101.0/24"]

    private_subnets = ["10.10.0.0/24", "10.10.1.0/24"]
}

resource "aws_internet_gateway" "aws-igw" {
  vpc_id = aws_vpc.aws-vpc.id
  tags = {
    Name = "${var.app_name}-igw"
  }
}

resource "aws_subnet" "private" {
  vpc_id            = aws_vpc.aws-vpc.id
  count             = length(local.private_subnets)
  cidr_block        = element(local.private_subnets, count.index)
  availability_zone = element(local.availability_zones, count.index)

  tags = {
    Name = "${var.app_name}-private-subnet-${count.index + 1}"
  }
}

resource "aws_subnet" "public" {
  vpc_id                  = aws_vpc.aws-vpc.id
  cidr_block              = element(local.public_subnets, count.index)
  availability_zone       = element(local.availability_zones, count.index)
  count                   = length(local.public_subnets)
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.app_name}-public-subnet-${count.index + 1}"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.aws-vpc.id

  tags = {
    Name = "${var.app_name}-routing-table-public"
  }
}

resource "aws_route" "public" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.aws-igw.id
}

resource "aws_route_table_association" "public" {
  count          = length(local.public_subnets)
  subnet_id      = element(aws_subnet.public.*.id, count.index)
  route_table_id = aws_route_table.public.id
}

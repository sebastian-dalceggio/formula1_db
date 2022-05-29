resource "aws_subnet" "subnet-one" {
    cidr_block = "${cidrsubnet(aws_vpc.vpc-main.cidr_block, 3, 1)}"
    vpc_id = "${aws_vpc.vpc-main.id}"
    availability_zone = var.availability_zone
}

# Attach the internet gateway to the vpc
resource "aws_route_table" "route-table-main" {
    vpc_id = "${aws_vpc.vpc-main.id}"
    # All traffic to the internet gateway
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = "${aws_internet_gateway.gw-main.id}"
    }
    tags = {
        Name = "route-table-main"
    }
}

# Associate between the subnet and the route table
resource "aws_route_table_association" "subnet-association" {
    subnet_id      = "${aws_subnet.subnet-one.id}"
    route_table_id = "${aws_route_table.route-table-main.id}"
}
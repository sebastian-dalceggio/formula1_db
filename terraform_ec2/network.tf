resource "aws_vpc" "vpc-main" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
    tags = {
      Name = "vpc-main"
    }
}

# Public IP
resource "aws_eip" "eip-ubuntu-1" {
    instance = "${aws_instance.ubuntu-1.id}"
    vpc      = true
}
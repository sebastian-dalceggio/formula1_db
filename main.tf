provider "aws" {
    region = "us-east-1"
    access_key = ""
    secret_key = ""
    token = ""
}

resource "aws_vpc" "test-env" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
    tags = {
      Name = "test-env"
    }
}

resource "aws_route_table" "route-table-test-env" {
    vpc_id = "${aws_vpc.test-env.id}"
    route {
      cidr_block = "0.0.0.0/0"
      gateway_id = "${aws_internet_gateway.test-env-gw.id}"
    }
    tags = {
      Name = "test-env-route-table"
    }
}
resource "aws_route_table_association" "subnet-association" {
  subnet_id      = "${aws_subnet.subnet-uno.id}"
  route_table_id = "${aws_route_table.route-table-test-env.id}"
}
resource "aws_internet_gateway" "test-env-gw" {
    vpc_id = "${aws_vpc.test-env.id}"
    tags = {
      Name = "test-env-gw"
    }
}
resource "aws_subnet" "subnet-uno" {
  cidr_block = "${cidrsubnet(aws_vpc.test-env.cidr_block, 3, 1)}"
  vpc_id = "${aws_vpc.test-env.id}"
  availability_zone = "us-east-1a"
}

resource "aws_security_group" "ingress-all-test" {
name = "allow-all-sg"
vpc_id = "${aws_vpc.test-env.id}"
ingress {
    cidr_blocks = [
      "0.0.0.0/0"
    ]
    from_port = 22
    to_port = 22
    protocol = "tcp"
  }
// Terraform removes the default rule
egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
 }
}
resource "aws_instance" "ubuntu-1" {
  ami = "ami-0c4f7023847b90238"
  instance_type = "t2.micro"
  availability_zone = "us-east-1a"
  key_name = "vockey"
  tags = {
      Name = "ubuntu-1"
  }
  security_groups = ["${aws_security_group.ingress-all-test.id}"]
  subnet_id = "${aws_subnet.subnet-uno.id}"

  user_data =   <<-EOF
                #!/bin/bash
                sudo apt-get update -y
                sudo apt-get install \
                ca-certificates \
                curl \
                gnupg \
                postgresql-client-common \
                postgresql-client-12 \
                lsb-release -y
                sudo apt install docker-compose -y
                mkdir /home/ubuntu/app
                cd /home/ubuntu/app
                sudo git clone https://github.com/sebastian-dalceggio/formula1_db
                cd formula1_db
                sudo bash create_and_run.sh
                EOF
}

resource "aws_eip" "ip-test-env" {
    instance = "${aws_instance.ubuntu-1.id}"
    vpc      = true
}

output "public_ip" {
  value = aws_instance.ubuntu-1.public_ip
}
resource "aws_instance" "ubuntu-1" {
    ami = "ami-0c4f7023847b90238"
    instance_type = "t2.micro"
    availability_zone = var.availability_zone
    key_name = var.key_name
    tags = {
        Name = "ubuntu-1"
    }
    security_groups = ["${aws_security_group.main-sg.id}"]
    subnet_id = "${aws_subnet.subnet-one.id}"

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
resource "aws_security_group" "main-sg" {
    name = "main-sg"
    vpc_id = "${aws_vpc.vpc-main.id}"

    # Accepts connections from all IPs on port 22 -> SSH
    ingress {
        cidr_blocks = ["0.0.0.0/0"]
        from_port = 22
        to_port = 22
        protocol = "tcp"
    }
    # Allow all outgoing traffic (Terraform removes the default rule)
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}
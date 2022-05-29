#https://medium.com/@hmalgewatta/setting-up-an-aws-ec2-instance-with-ssh-access-using-terraform-c336c812322f

output "public_ip" {
    value = aws_instance.ubuntu-1.public_ip
}
provider "aws" {
  region = "us-east-1"
}

resource "tls_private_key" "parking_key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "aws_key_pair" "generated_key" {
  key_name   = "parking-lot-key"
  public_key = tls_private_key.parking_key.public_key_openssh
}

resource "local_file" "private_key" {
  content  = tls_private_key.parking_key.private_key_pem
  filename = "${path.module}/parking-lot-key.pem"
}

resource "aws_instance" "parking_server" {
  ami           = "ami-0c2b8ca1dad447f8a"
  instance_type = "t2.micro"
  key_name      = aws_key_pair.generated_key.key_name

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install python3 git -y
              pip3 install flask
              git clone https://github.com/aviferdman/Cloud-Computing.git
              cd parking-lot-management/app
              python3 parking_system.py &
            EOF

  tags = {
    Name = "ParkingLotServer"
  }
}

output "instance_public_ip" {
  value = aws_instance.parking_server.public_ip
}

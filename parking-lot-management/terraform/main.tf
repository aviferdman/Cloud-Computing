provider "aws" {
  region = "us-east-1"
}

# VPC
resource "aws_vpc" "parking_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "parking-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "parking_igw" {
  vpc_id = aws_vpc.parking_vpc.id

  tags = {
    Name = "parking-igw"
  }
}

# Public Subnet
resource "aws_subnet" "parking_subnet" {
  vpc_id                  = aws_vpc.parking_vpc.id
  cidr_block              = "10.0.1.0/24"
  map_public_ip_on_launch = true
  availability_zone       = "us-east-1a"

  tags = {
    Name = "parking-subnet"
  }
}

# Route Table
resource "aws_route_table" "parking_rt" {
  vpc_id = aws_vpc.parking_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.parking_igw.id
  }

  tags = {
    Name = "parking-rt"
  }
}

# Route Table Association
resource "aws_route_table_association" "parking_rta" {
  subnet_id      = aws_subnet.parking_subnet.id
  route_table_id = aws_route_table.parking_rt.id
}

# Security Group
resource "aws_security_group" "parking_sg" {
  name        = "parking_sg"
  description = "Security group for parking lot server"
  vpc_id      = aws_vpc.parking_vpc.id

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow Flask application traffic"
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow SSH access"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic"
  }

  tags = {
    Name = "parking-sg"
  }
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
  subnet_id     = aws_subnet.parking_subnet.id
  vpc_security_group_ids = [aws_security_group.parking_sg.id]

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

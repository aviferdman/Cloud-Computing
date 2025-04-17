#!/bin/bash
sudo yum update -y
sudo yum install python3 git -y
pip3 install flask
git clone https://github.com/aviferdman/Cloud-Computing.git
cd parking-lot-management/app
python3 parking_system.py &

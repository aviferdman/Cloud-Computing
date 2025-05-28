# Parking Lot Management System

A simple cloud-based API for tracking vehicle entry/exit and calculating parking fees.

---

## Usage

### API Endpoints:

- **POST /entry?plate=123-123-123&parkingLot=1**  
  Returns a ticket ID.

- **POST /exit?ticketId={ticketId}**  
  Returns the plate, parked time in minutes, parking lot ID, and fee.

# Usage with Deployed Instance

After deploying the EC2 instance with Terraform, you can use the instance_public_ip output to interact with the API:

1. Wait 3-5 minutes after terraform deployment completes for the instance to fully initialize.
2. Use the instance_public_ip from terraform output in your requests:

Example API calls (replace {IP} with your instance_public_ip):
```bash
# Vehicle Entry
http://{IP}:5000/entry?plate=12345&parkingLot=12345

# Vehicle Exit
http://{IP}:5000/exit?ticketId=6fc28b9d-bc89-44e6-9460-ddfa89ede016
```

Note: If you receive connection errors, wait a few more minutes as the instance might still be initializing.

---

## Local Deployment:

1. Install Python 3.
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the server:
    ```bash
    python app/parking_system.py
    ```

---
## Linux 

## Zero-Touch Containerized Deployment

Deploy the application as a containerized service using AWS ECR and EC2 with minimal manual intervention:

1. **Prerequisites**:
   - Docker installed locally
   - AWS CLI configured with appropriate permissions
   - Terraform installed

2. **Create ECR Repository**:
    ```bash
    cd terraform
    terraform init
    terraform apply -target=aws_ecr_repository.parking_app
    ```
   Note the ECR repository URL from the output.

3. **Build and Push Docker Image**:
    ```bash
    cd ../deploy
    sudo ./deploy.sh
    ```

4. **Deploy EC2 Instance**:
    ```bash
    cd ../terraform
    terraform apply
    ```

## Windows 

## Zero-Touch Containerized Deployment

Deploy the application as a containerized service using AWS ECR and EC2 with minimal manual intervention:

1. **Prerequisites**:
   - Docker installed locally
   - AWS CLI configured with appropriate permissions
   - Terraform installed
   - WSL installed

2. **Create ECR Repository**:
    ```bash
    wsl 
    cd terraform
    terraform init
    terraform apply -target=aws_ecr_repository.parking_app
    ```
   Note the ECR repository URL from the output.

3. **Build and Push Docker Image**:
    ```bash
    cd ../deploy
    sudo ./deploy.sh
    ```

4. **Deploy EC2 Instance**:
    ```bash
    cd ../terraform
    terraform apply
    ```
Your containerized application will be running on the EC2 instance's public IP at port 5000.

---

## Clean Up

To remove all AWS resources:
```bash
cd terraform
terraform destroy
```

---

## Security Notice

- Never commit `terraform/parking-lot-key.pem` to GitHub.
- AWS keys must be configured securely.
- Keep your ECR repository credentials secure.

---
## Testing
```bash
    cd /app
    pytest test_parking_system_integration.py
    pytest test_parking_system_unit_tests.py
```

---

# Common Issues and Solutions

## 1. Docker Build Error in WSL

If you encounter this error when running `sudo ./deploy.sh`:
```bash
ERROR [internal] load metadata for docker.io/library/python:3.9-slim
```

### Solution:

1. **Fix Docker Credentials**:
   ```bash
   # Open Docker config file
   nano ~/.docker/config.json
   ```

   Remove any `credsStore` entry. The file should look like either:
   ```json
   {
     "auths": {
       "https://index.docker.io/v1/": {}
     }
   }
   ```
   Or:
   ```json
   {
     "auths": {
       "946122991383.dkr.ecr.us-east-1.amazonaws.com": {}
     }
   }
   ```

   To save in nano:
   - Press `Ctrl + O` to write changes
   - Press `Enter` to confirm
   - Press `Ctrl + X` to exit

2. **Retry Deployment**:
   ```bash
   sudo ./deploy.sh
   ```

## 2. Docker Command Not Found

If you encounter this error when running `./deploy.sh`:
```bash
./deploy.sh: line 13: docker: command not found
```

### Solution:

1. **Enable WSL Integration in Docker Desktop**:
   - Open Docker Desktop
   - Go to Settings
   - Navigate to Resources → WSL Integration
   - Check "Enable integration with my default WSL distro"
   - Under "Enable integration with additional distros", ensure "Ubuntu-18.04" is checked
   - Click Apply & Restart
   - Wait for Docker Desktop to restart completely

2. **Retry Deployment**:
   ```bash
   sudo ./deploy.sh
   ```

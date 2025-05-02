# Parking Lot Management System

A simple cloud-based API for tracking vehicle entry/exit and calculating parking fees.

---

## Usage

### API Endpoints:

- **POST /entry?plate=123-123-123&parkingLot=1**  
  Returns a ticket ID.

- **POST /exit?ticketId={ticketId}**  
  Returns the plate, parked time in minutes, parking lot ID, and fee.

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

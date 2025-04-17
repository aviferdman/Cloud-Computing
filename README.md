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

## AWS EC2 Deployment (Zero-Touch)

1. Install Terraform: https://developer.hashicorp.com/terraform/downloads  
2. Configure AWS credentials (`aws configure`).
3. Deploy with:
    ```bash
    cd terraform
    terraform init
    terraform apply -auto-approve
    ```

Your server's IP will be shown when it finishes.

---

## Security Notice

- Never commit `terraform/parking-lot-key.pem` to GitHub.
- AWS keys must be configured securely.

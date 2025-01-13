# Deployment and Template Generation Scripts

This folder contains two Python scripts, `deploy_infrastructure.py` and `generate_template.py`, designed to manage the deployment of AWS infrastructure and generate CloudFormation templates for your MLOps pipeline.

---

## **Scripts Overview**

### **1. `deploy_infrastructure.py`**

#### **Purpose**
This script automates the deployment and updating of AWS resources using CloudFormation and manages the deployment of Lambda function code stored in S3.

#### **Key Features**
- Deploys or updates a CloudFormation stack.
- Updates AWS Lambda functions using code stored in an S3 bucket.
- Uses configurations defined in `configs/config.yaml`.

#### **Usage**
1. Ensure your AWS credentials are configured locally or using environment variables.
2. Update the `configs/config.yaml` file with the following details:
   - CloudFormation stack name, template file, and parameters.
   - S3 bucket and Lambda function details.
3. Run the script:
   ```bash
   python deploy_infrastructure.py

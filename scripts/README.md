# Deployment and Template Generation Scripts


This repository provides a robust framework to set up and manage an end-to-end Machine Learning Operations (MLOps) pipeline on AWS. Below is a detailed guide to using the `deploy.sh` and `generate_template.py` scripts included in this repository.

## Overview
The two main scripts in this repository are:

1. **`generate_template.py`**: Dynamically generates and updates CloudFormation templates and Lambda scripts based on configurations provided in `config/config.yaml`.
2. **`deploy.sh`**: Automates the end-to-end process of generating templates, pushing changes to GitHub, and deploying the AWS CloudFormation stack.

---

## Prerequisites

Ensure you have the following tools and resources configured before using the scripts:

1. **AWS CLI**:
   - Installed and configured with appropriate IAM permissions.

2. **GitHub CLI**:
   - Installed and authenticated to interact with your GitHub repository.

3. **Python**:
   - Installed with dependencies listed in `requirements.txt`.

4. **Configuration File**:
   - Ensure `config/config.yaml` is correctly populated with all necessary configurations.

---

## File Descriptions

### **`generate_template.py`**

This script reads configurations from `config/config.yaml` and updates the following components:

- **CloudFormation Templates**:
  - Located in `infra/cloudformation/pipeline.yaml`.
- **Lambda Functions**:
  - Updates all Lambda-related files in the `lambda/` directory.
- **CI/CD Pipeline Configurations**:
  - Updates `ci-cd_codepipeline/pipeline.yaml` to align with user-defined settings.

#### Usage

Run the script using the following command:

```bash
python scripts/generate_template.py
```

Upon execution, the script:
1. Reads and parses `config.yaml`.
2. Updates the relevant template files and scripts.
3. Prepares the repository for deployment.

---

### **`deploy.sh`**

The `deploy.sh` script simplifies the deployment process by automating key tasks:

#### Key Steps

1. **Generate CloudFormation Template**:
   Invokes `generate_template.py` to create or update templates.

2. **Push Updates to GitHub**:
   - Creates a new branch with a timestamp (`updated@YYYYMMDD_HHMMSS`).
   - Commits and pushes the changes to the GitHub repository.
   - Optionally creates a pull request using the GitHub CLI.

3. **Deploy CloudFormation Stack**:
   - Uses `aws cloudformation deploy` to deploy the updated CloudFormation template.

#### Usage

Run the script using the following command:

```bash
bash scripts/deploy.sh
```

---

## Example Workflow

1. Clone the repository:

   ```bash
   git clone https://github.com/FirdowsRahaman/aws-end-to-end-mlops-pipeline.git
   cd aws-end-to-end-mlops-pipeline
   ```

2. Generate the CloudFormation template:

   ```bash
   python scripts/generate_template.py
   ```

3. Execute the deployment script:

   ```bash
   bash scripts/deploy.sh
   ```

4. Verify the CloudFormation stack deployment via the AWS Management Console.

---

## Notes

- **Configuration**:
  Ensure that `config/config.yaml` is correctly set up to reflect your specific requirements.

- **IAM Permissions**:
  The AWS CLI user must have permissions to manage CloudFormation stacks, Lambda functions, ECR repositories, EventBridge rules, and SageMaker resources.

For further details, refer to the repository documentation or contact the repository maintainer.

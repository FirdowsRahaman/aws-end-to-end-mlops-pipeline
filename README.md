# AWS End-to-End MLOps Pipeline

This repository provides an implementation of an **End-to-End MLOps Pipeline** using various AWS services like **SageMaker**, **Lambda**, **EventBridge**, **ECR**, **CodePipeline**, and **S3**. The pipeline automates the process of code deployment, model training, evaluation, and deployment. It also supports continuous retraining based on new data or code updates from GitHub.

## Overview

The pipeline includes the following steps:

1. **GitHub Push**: A push to the GitHub repository triggers the pipeline.
2. **CodePipeline**: Fetches code from GitHub, builds a Docker image, and deploys the Lambda function.
3. **ECR Image Push**: The pipeline deploys Docker images to AWS ECR, which triggers the EventBridge rule.
4. **Lambda Function**: The Lambda function is triggered by the EventBridge rule to preprocess data, train a model, and store the model artifacts in **S3**.
5. **Model Registration**: After training, the model is registered in **SageMaker Model Registry** for versioning.
6. **Model Evaluation**: A custom Python script is used to evaluate the model, and the best model is deployed to a SageMaker endpoint.
7. **Lambda Endpoint Consumption**: The Lambda function invokes the deployed model endpoint for inference.
8. **Continuous Retraining**: If new data is added to S3 or code is updated in GitHub, the model retrains automatically.

## Folder Structure

```bash

aws-end-to-end-mlops-pipeline/
│
├── ci_cd/                # CI/CD configurations
│   ├── codepipeline/     # AWS CodePipeline configurations
│   ├── github_actions/   # GitHub Actions workflows
│   └── scripts/          # Custom scripts for CI/CD
│
├── config/               # Configuration files
│   ├── aws/              # AWS-specific configurations (e.g., IAM, S3 paths)
│   ├── hyperparameters/  # Hyperparameter configuration files
│   └── pipeline.yaml     # Main pipeline configuration
│
├── data/                 # Raw and processed data
│   ├── processed/        # Processed data
│   └── raw/              # Raw data
│
├── docs/                 # Documentation
│   ├── architecture/     # Architecture diagrams
│   ├── setup.md          # Setup instructions
│   └── usage.md          # How to use the pipeline
│
├── infra/                # Infrastructure as Code (IaC)
│   ├── cdk/              # AWS CDK scripts
│   ├── cloudformation/   # CloudFormation templates
│   └── terraform/        # Terraform scripts for provisioning
│
├── lambdas/              # AWS Lambda functions
│   ├── function1/        # Example Lambda function 1
│   └── function2/        # Example Lambda function 2
│
├── models/               # Saved models
│   ├── artifacts/        # Intermediate artifacts (e.g., checkpoints)
│   └── trained/          # Trained models
│
├── monitoring/           # Monitoring and logging configurations
│   ├── dashboards/       # Visualization (e.g., CloudWatch or Grafana setups)
│   └── scripts/          # Custom scripts for monitoring
│
├── notebooks/            # Jupyter notebooks for experimentation
│
├── pipelines/            # Definitions of ML pipelines
│   ├── inference_pipeline.py # Inference pipeline
│   └── training_pipeline.py  # Training pipeline
│
├── src/                  # Source code for the pipeline
│   ├── evaluation/       # Model evaluation scripts
│   ├── preprocessing/    # Data preprocessing scripts
│   ├── training/         # Model training scripts
│   ├── deployment/       # Deployment scripts (e.g., Lambda, API Gateway)
│   └── utils/            # Utility functions and common scripts
│
├── tests/                # Unit and integration tests
│
├── LICENSE               # Project license
├── README.md             # Project overview and instructions
├── requirements.txt      # Python dependencies
└── .gitignore            # Ignored files and directories

```

## Architecture

### Components
1. **GitHub**: The source repository containing your model code and Lambda function.
2. **AWS CodePipeline**: Automates the process of building the Docker image, deploying Lambda functions, and orchestrating other AWS services.
3. **AWS CodeBuild**: Used to build the Docker image for Lambda and model training.
4. **Amazon ECR**: Stores Docker images used for Lambda and training jobs.
5. **AWS Lambda**: The core service that triggers model training, evaluation, and deployment.
6. **Amazon S3**: Stores the training data, model artifacts, and Lambda code.
7. **Amazon SageMaker**: Preprocesses the data, trains the model, and registers the model in the **Model Registry**.
8. **AWS EventBridge**: Triggers the Lambda function when a new image is pushed to ECR.
9. **SageMaker Model Registry**: Used to store model versions and track the best performing model.
    
## Pipeline Flow

1. **Code Changes (GitHub)**:
    - Whenever there is a push to the GitHub repository, it triggers **AWS CodePipeline**.
    - The pipeline fetches the latest code and builds the Docker image using **AWS CodeBuild**.

2. **Docker Image Build & Deployment**:
    - **CodeBuild** compiles the Docker image, stores it in **Amazon ECR**, and triggers the EventBridge rule.

3. **EventBridge Trigger**:
    - When a new image is pushed to ECR, **EventBridge** triggers the **Lambda** function.

4. **Lambda Execution**:
    - The Lambda function invokes **Amazon SageMaker** to run the model preprocessing and training jobs.
    - After training, the model is saved to **S3** and registered in the **SageMaker Model Registry**.

5. **Model Evaluation**:
    - The model is evaluated based on a custom Python script.
    - If the model meets the required accuracy threshold, it is deployed to **SageMaker Endpoint** for serving predictions.

6. **Model Deployment**:
    - The best model is deployed and exposed via a **SageMaker endpoint**.
    - **Lambda** is used to interact with the endpoint for inference.

7. **Continuous Retraining**:
    - If new data is added to **S3** or code is updated in **GitHub**, the pipeline automatically retrains the model.

## Requirements

Before using this repository, ensure that you have the following:

- AWS Account with the required IAM roles for Lambda, SageMaker, CodePipeline, CodeBuild, EventBridge, ECR, and S3.
- GitHub repository with the code to be deployed, including model training scripts and Lambda functions.
- Docker installed locally for testing (optional).

## Steps to Deploy

### 1. Set Up Your AWS Environment
- Ensure you have the required IAM roles and permissions to allow **CodePipeline**, **CodeBuild**, **Lambda**, and **SageMaker** to interact with other AWS services.
- Create an **S3 bucket** for storing artifacts, model data, and Lambda code.

### 2. Clone the Repository

```bash
git clone https://github.com/FirdowsRahaman/aws-end-to-end-mlops-pipeline.git
cd aws-end-to-end-mlops-pipeline
```

### 3. Update the CloudFormation Template
Edit the cloudformation.yml file to specify your parameters:

- GitHubRepoName: Your GitHub repository name.
- GitHubBranchName: The branch you want to track (usually main).
- GitHubTokenSecret: The Secrets Manager ARN for the GitHub OAuth token.
- S3BucketName: The name of your S3 bucket to store artifacts and model data.
- ECRRepoName: The name of your ECR repository for Docker images.
- LambdaRoleArn: The ARN of the IAM role that Lambda will assume.

### 4. Deploy CloudFormation Stack
Deploy the CloudFormation stack that sets up the infrastructure for the pipeline:

```bash
aws cloudformation create-stack --stack-name mlops-pipeline --template-body file://cloudformation.yml --capabilities CAPABILITY_IAM
```

### 5. Push Code to GitHub
- Push your code (including the model training and Lambda functions) to your GitHub repository. This will trigger the pipeline and start the deployment process.
  
### 6. Monitor the Pipeline
- Monitor the progress of the CodePipeline through the AWS Console. You can track each stage of the pipeline, including Source, Build, and Deploy.

### 7. Retraining Trigger
- The pipeline supports continuous retraining. If you add new data to S3 or update the code in GitHub, the pipeline will retrain the model and deploy the new version automatically.

## Lambda Function Details
### Lambda Trigger Function
The Lambda function invoked by EventBridge performs the following tasks:

1. Preprocessing: Calls SageMaker to process the data.
2. Training: Trains the model on the processed data.
3. Model Evaluation: Evaluates the model using a custom Python script.
4. Model Deployment: If the model meets the accuracy threshold, it is deployed to a SageMaker endpoint for serving predictions.
   
You can update the Lambda function code and deployment package as needed from the GitHub repository.

## Conclusion
This repository helps you set up an end-to-end MLOps pipeline using AWS services, including automatic retraining and deployment. By leveraging AWS CodePipeline, Lambda, SageMaker, and other AWS services, you can automate the model training and deployment process and ensure a continuous flow of updates based on new data or code changes.

For further customizations, refer to the CloudFormation templates and the Lambda function code.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

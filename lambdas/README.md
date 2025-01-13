# SageMaker Training and Deployment Pipeline

This repository contains AWS Lambda functions that automate the SageMaker training, evaluation, model registration, deployment, and retraining processes. The pipeline is designed to use Amazon Elastic Container Registry (ECR), SageMaker, and S3 to streamline the model lifecycle from training to deployment.

## Pipeline Overview

The pipeline consists of several stages, each managed by AWS Lambda functions. These functions automate the following steps:

1. **Trigger SageMaker Training**: Initiates a SageMaker training job using a Docker image stored in ECR.
2. **Evaluate Model**: Evaluates the trained model based on performance metrics.
3. **Register Model**: Registers the trained model in the SageMaker Model Registry if evaluation passes.
4. **Deploy Model**: Deploys the model to a SageMaker endpoint for real-time inference.
5. **Retrain Model**: Triggers retraining whenever new data is added to an S3 bucket.

## Lambda Functions

### 1. **`trigger_model_training`**
This Lambda function triggers a SageMaker training job using a Docker image from ECR. It receives an event with the image URI from ECR and starts the training job.

- **Input**: ECR image URI from an EventBridge event.
- **Output**: Response confirming the training job initiation.

### 2. **`evaluate_model_function`**
Once the training job completes, this Lambda function evaluates the trained model. The model is evaluated using a custom evaluation script, and the evaluation results are saved to an S3 location.

- **Input**: Model artifact from training and evaluation data.
- **Output**: Response confirming the start of the evaluation.

### 3. **`register_model_in_registry`**
If the model passes evaluation, this function registers the model in the SageMaker Model Registry for versioning and tracking.

- **Input**: Model artifact and model name.
- **Output**: Response confirming successful model registration.

### 4. **`deploy_sagemaker_model`**
This Lambda function deploys the model to a SageMaker endpoint for serving real-time predictions.

- **Input**: Model name.
- **Output**: Response confirming successful model deployment to the endpoint.

### 5. **`retrain_model_on_new_data`**
Whenever new data is uploaded to an S3 bucket, this function triggers a retraining job to ensure the model is updated with the latest data.

- **Input**: S3 event notification indicating new data.
- **Output**: Response confirming retraining job initiation.

## Architecture

The pipeline is triggered by events from various sources:
- **ECR**: When a Docker image is pushed to Amazon Elastic Container Registry (ECR), an event triggers the **`trigger_model_training`** function.
- **S3**: When new data is uploaded to S3, the **`retrain_model_on_new_data`** function is triggered.
- **EventBridge**: Events generated from other actions, like model training completion, can trigger further actions in the pipeline.

The flow of events ensures that the model is continually trained, evaluated, and deployed as needed.

## Environment Setup

### Prerequisites
- **IAM Role**: Ensure that the Lambda functions have the necessary permissions to interact with SageMaker, ECR, S3, and other AWS services.
- **Environment Variables**: Set up the following environment variables in the Lambda function configuration:
  - `SAGEMAKER_ROLE`: The ARN of the IAM role for SageMaker operations.
  - `S3_TRAINING_DATA_URI`: The S3 URI for the training data.
  - `S3_OUTPUT_PATH`: The S3 path to store the output of training jobs.
  - `EVALUATION_DATA_URI`: The S3 URI for the evaluation data.
  - `S3_EVALUATION_RESULTS_URI`: The S3 path for storing evaluation results.
  - `MODEL_REGISTRY_NAME`: The name of the SageMaker model registry.
  - `MODEL_IMAGE_URI`: The URI for the Docker image used for training.

### Steps to Deploy

1. **Create the necessary IAM roles**:
   - Create an IAM role for SageMaker to manage model training, evaluation, and deployment.
   - Assign the role to your Lambda functions with appropriate policies.

2. **Set up environment variables**:
   - Configure the required environment variables in the AWS Lambda function settings as mentioned above.

3. **Push Docker image to ECR**:
   - Ensure the Docker image for training is pushed to ECR. You can use the AWS CLI or SDKs to automate this process.

4. **Configure EventBridge for ECR events**:
   - Set up an EventBridge rule to trigger the **`trigger_model_training`** function when a new image is pushed to ECR.

5. **Upload data to S3**:
   - Upload your training and evaluation data to the designated S3 buckets to trigger the retraining process.

6. **Deploy the Lambda functions**:
   - Deploy the Lambda functions using the AWS Lambda console, AWS SAM, or AWS CloudFormation.
   - Attach the correct permissions to allow Lambda to invoke SageMaker and interact with ECR and S3.

## Example Workflow

1. **Step 1**: Push a Docker image to ECR.
2. **Step 2**: EventBridge triggers **`trigger_model_training`**.
3. **Step 3**: SageMaker training job is initiated using the Docker image from ECR.
4. **Step 4**: Once training completes, **`evaluate_model_function`** is triggered to evaluate the model.
5. **Step 5**: If evaluation passes, **`register_model_in_registry`** registers the model in the SageMaker Model Registry.
6. **Step 6**: **`deploy_sagemaker_model`** deploys the model to a SageMaker endpoint for real-time predictions.
7. **Step 7**: New data uploaded to S3 triggers **`retrain_model_on_new_data`**, retraining the model with the updated data.

## Conclusion

This setup automates the end-to-end machine learning pipeline using AWS services, ensuring that your models are always up-to-date and available for real-time predictions. By leveraging Lambda, SageMaker, and EventBridge, you can streamline the training, evaluation, and deployment processes while keeping your models fresh with the latest data.

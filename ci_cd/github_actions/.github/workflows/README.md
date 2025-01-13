# MLOps Pipeline with GitHub Actions, ECR, Lambda, and SageMaker

This repository contains an automated MLOps pipeline that integrates various AWS services such as **ECR (Elastic Container Registry)**, **Lambda**, **SageMaker**, and **EventBridge** to manage model training, evaluation, registration, deployment, and retraining. The pipeline is triggered by code changes, new Docker images, or new data added to S3, automating the machine learning lifecycle.

## Table of Contents
- [Overview](#overview)
- [Process Flow](#process-flow)
- [Pipeline Stages](#pipeline-stages)
  - [Source Stage](#source-stage)
  - [Build Stage](#build-stage)
  - [Deploy to ECR](#deploy-to-ecr)
  - [Start SageMaker Training](#start-sagemaker-training)
  - [Evaluate Model](#evaluate-model)
  - [Register Model](#register-model)
  - [Deploy Model](#deploy-model)
  - [Retrain Model](#retrain-model)
- [EventBridge Integration](#eventbridge-integration)
- [Lambda Functions](#lambda-functions)
- [IAM Roles](#iam-roles)
- [Setup and Configuration](#setup-and-configuration)
- [CI/CD Pipeline with GitHub Actions](#ci-cd-pipeline-with-github-actions)

## Overview

This pipeline automates the entire machine learning lifecycle:
1. **Code Fetch**: Fetches the latest code from a GitHub repository.
2. **Build**: Builds the Docker image containing the training model using AWS CodeBuild.
3. **Deploy**: Pushes the built Docker image to Amazon ECR (Elastic Container Registry).
4. **Trigger Training**: Once the image is pushed to ECR, an **EventBridge** rule triggers the Lambda function to start a SageMaker training job.
5. **Model Evaluation**: After training, another Lambda function evaluates the trained model's performance.
6. **Model Registration**: If the evaluation passes, the model is registered in the SageMaker Model Registry.
7. **Model Deployment**: The model is deployed to a SageMaker endpoint for real-time inference.
8. **Retraining**: If new data is added to S3, a Lambda function triggers model retraining.

## Process Flow

1. **Code Fetch**: The pipeline fetches the latest code from the GitHub repository using the GitHub Actions workflow.
2. **Build Docker Image**: In the Build stage, AWS CodeBuild creates a Docker image that contains the model training code and dependencies.
3. **Push to ECR**: The image is pushed to Amazon ECR (Elastic Container Registry).
4. **Trigger Training**: When a new Docker image is pushed to ECR, **EventBridge** triggers the Lambda function `trigger_model_training` to initiate the SageMaker training job.
5. **Model Evaluation**: After training, another Lambda function evaluates the model's performance based on predefined metrics.
6. **Model Registration**: If the evaluation is successful, the `register_model_in_registry` Lambda function registers the model in the SageMaker Model Registry.
7. **Model Deployment**: After registration, the model is deployed to a SageMaker endpoint using the `deploy_sagemaker_model` Lambda function.
8. **Retraining**: When new data is added to S3, a Lambda function triggers retraining of the model.

## Pipeline Stages

### Source Stage
- **Description**: Fetches the latest code from a GitHub repository.
- **Action**: `GitHubSource`
- **Tools**: GitHub, OAuth Token

### Build Stage
- **Description**: Builds the Docker image containing the model code.
- **Action**: `BuildDockerImage`
- **Tools**: AWS CodeBuild

### Deploy to ECR
- **Description**: Pushes the Docker image to Amazon ECR.
- **Action**: `PushDockerImageToECR`
- **Tools**: Amazon ECR

### Start SageMaker Training
- **Description**: Triggers the SageMaker training job when a new Docker image is pushed to ECR.
- **Action**: `StartTrainingJob`
- **Tools**: AWS Lambda, SageMaker

### Evaluate Model
- **Description**: Evaluates the trained model after the training job completes.
- **Action**: `ModelEvaluationLambda`
- **Tools**: AWS Lambda, SageMaker Metrics

### Register Model
- **Description**: Registers the model in SageMaker Model Registry if it passes evaluation.
- **Action**: `RegisterModelInRegistry`
- **Tools**: AWS Lambda, SageMaker Model Registry

### Deploy Model
- **Description**: Deploys the registered model to a SageMaker endpoint for real-time predictions.
- **Action**: `DeployToEndpoint`
- **Tools**: AWS Lambda, SageMaker Endpoint

### Retrain Model
- **Description**: Retrains the model when new data is added to S3.
- **Action**: `TriggerRetraining`
- **Tools**: AWS Lambda, S3

## EventBridge Integration

- **Description**: EventBridge listens for ECR image push events and triggers the `trigger_model_training` Lambda function.
- **Event Pattern**: Listens for the `ECR Image Push` event from ECR.
- **EventBridge Rule**: The rule is set to trigger the Lambda function whenever a new image is pushed to the specified ECR repository.
- **Target Lambda**: The rule targets the Lambda function that starts the SageMaker training job.

## Lambda Functions

The following Lambda functions are part of the pipeline:

- **trigger_model_training**: Starts a SageMaker training job using the Docker image from ECR.
- **evaluate_model_function**: Evaluates the trained model based on performance metrics.
- **register_model_in_registry**: Registers the model in SageMaker Model Registry if evaluation passes.
- **deploy_sagemaker_model**: Deploys the model to a SageMaker endpoint.
- **retrain_model_on_new_data**: Retrains the model when new data is added to S3.

## IAM Roles

- The Lambda functions require specific IAM roles with appropriate permissions to interact with services like **SageMaker**, **ECR**, and **S3**. Ensure that the Lambda functions are assigned IAM roles with sufficient permissions to perform their tasks.

## Setup and Configuration

1. **GitHub Repository**: Ensure the GitHub repository containing your model code is available and accessible.
2. **CodeBuild Project**: Set up an AWS CodeBuild project to build the Docker image.
3. **Amazon ECR**: Set up an ECR repository to store the Docker images.
4. **SageMaker**: Set up SageMaker to handle model training, evaluation, and deployment.
5. **EventBridge Rule**: Configure an EventBridge rule to listen for image pushes in ECR and trigger the training Lambda.
6. **Lambda Functions**: Deploy the Lambda functions and assign them the correct IAM roles.

## CI/CD Pipeline with GitHub Actions

The CI/CD pipeline automates the deployment process using GitHub Actions. Below is an overview of the actions performed in the pipeline:

- **Code Fetch**: The pipeline fetches the latest code from the GitHub repository.
- **Docker Build**: Builds the Docker image for training.
- **Push to ECR**: Pushes the Docker image to Amazon ECR.
- **Trigger Lambda**: EventBridge triggers the Lambda function to start SageMaker training when a new image is pushed to ECR.
- **Model Evaluation**: Lambda evaluates the model after training.
- **Model Registration**: The model is registered in SageMaker Model Registry.
- **Model Deployment**: The model is deployed to SageMaker Endpoint for inference.

## Conclusion

This GitHub Actions-based pipeline automates the ML lifecycle and integrates various AWS services, making model training, evaluation, and deployment more efficient. The pipeline can automatically retrain models when new data is added, ensuring continuous improvement of the model.

For more detailed setup instructions, refer to the AWS documentation for each service used in this pipeline.


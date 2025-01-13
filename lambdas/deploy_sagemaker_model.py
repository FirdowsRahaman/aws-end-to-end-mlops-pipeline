import boto3
import json
import os

sagemaker_client = boto3.client('sagemaker')
sm_runtime_client = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    """
    Lambda function to deploy a trained model to a SageMaker endpoint.
    Expects the following environment variables:
    - MODEL_NAME: Name of the model artifact in S3 (excluding S3 path).
    - MODEL_BUCKET: S3 bucket where the model artifact is stored.
    - INSTANCE_TYPE: Instance type for the endpoint (e.g., ml.m5.large).
    - ENDPOINT_NAME: Desired name of the SageMaker endpoint.
    """
    # Environment variables
    model_name = os.getenv('MODEL_NAME')
    model_bucket = os.getenv('MODEL_BUCKET')
    instance_type = os.getenv('INSTANCE_TYPE', 'ml.m5.large')
    endpoint_name = os.getenv('ENDPOINT_NAME', 'sagemaker-endpoint')

    # Check if required environment variables are provided
    if not all([model_name, model_bucket]):
        raise ValueError("MODEL_NAME and MODEL_BUCKET environment variables must be set.")

    model_data_url = f"s3://{model_bucket}/{model_name}"
    print(f"Model data URL: {model_data_url}")

    # Step 1: Create Model
    model_config = {
        'ModelName': model_name,
        'PrimaryContainer': {
            'Image': '123456789012.dkr.ecr.us-east-1.amazonaws.com/sagemaker-inference:latest', # Replace with your ECR image URI
            'ModelDataUrl': model_data_url,
        },
        'ExecutionRoleArn': 'arn:aws:iam::123456789012:role/service-role/AmazonSageMaker-ExecutionRole', # Replace with your IAM role ARN
    }
    print(f"Creating SageMaker model with configuration: {model_config}")
    try:
        sagemaker_client.create_model(**model_config)
    except Exception as e:
        raise RuntimeError(f"Error creating SageMaker model: {e}")

    # Step 2: Create Endpoint Configuration
    endpoint_config_name = f"{endpoint_name}-config"
    endpoint_config = {
        'EndpointConfigName': endpoint_config_name,
        'ProductionVariants': [
            {
                'VariantName': 'AllTraffic',
                'ModelName': model_name,
                'InstanceType': instance_type,
                'InitialInstanceCount': 1,
            }
        ]
    }
    print(f"Creating endpoint configuration: {endpoint_config}")
    try:
        sagemaker_client.create_endpoint_config(**endpoint_config)
    except Exception as e:
        raise RuntimeError(f"Error creating endpoint configuration: {e}")

    # Step 3: Create Endpoint
    print(f"Creating endpoint {endpoint_name}")
    try:
        sagemaker_client.create_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name
        )
    except Exception as e:
        raise RuntimeError(f"Error creating SageMaker endpoint: {e}")

    print(f"Successfully created SageMaker endpoint: {endpoint_name}")
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Model deployment started successfully.',
            'endpoint_name': endpoint_name,
        })
    }


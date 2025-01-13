import os
import json
import boto3
from botocore.exceptions import ClientError

# Initialize the SageMaker client
sagemaker_client = boto3.client('sagemaker')

def lambda_handler(event, context):
    """
    Lambda function to trigger a SageMaker training job.
    """
    # Log the incoming event for debugging
    print("Received event:", json.dumps(event, indent=2))

    # Extract the training job name and configuration
    training_job_name = f"training-job-{int(context.aws_request_id[:8], 16)}"  # Unique job name
    training_config_s3 = os.getenv('TRAINING_CONFIG_S3')
    
    if not training_config_s3:
        raise ValueError("TRAINING_CONFIG_S3 environment variable is not set.")

    # Fetch training job configuration from S3
    s3_client = boto3.client('s3')
    bucket, key = training_config_s3.replace("s3://", "").split("/", 1)
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        training_config = json.loads(response['Body'].read().decode('utf-8'))
        print("Training configuration fetched successfully.")
    except ClientError as e:
        print(f"Error fetching training configuration: {e}")
        raise

    # Update training job name in configuration
    training_config['TrainingJobName'] = training_job_name

    try:
        # Trigger the SageMaker training job
        response = sagemaker_client.create_training_job(**training_config)
        print(f"Training job {training_job_name} started successfully.")
    except ClientError as e:
        print(f"Error starting training job: {e}")
        raise

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Training job {training_job_name} triggered successfully.",
            "training_job_name": training_job_name
        })
    }


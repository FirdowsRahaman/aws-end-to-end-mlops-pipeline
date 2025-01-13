import boto3
import json
import os

def lambda_handler(event, context):
    sagemaker_client = boto3.client('sagemaker')
    
    # Extract ECR image URI from event
    image_uri = event['detail']['responseElements']['imageUri']
    
    # Specify SageMaker training job parameters
    training_job_name = f"training-job-{image_uri.split('/')[-1]}"
    
    # Define the SageMaker training job parameters
    training_job_params = {
        'TrainingJobName': training_job_name,
        'AlgorithmSpecification': {
            'TrainingImage': image_uri,
            'TrainingInputMode': 'File'
        },
        'RoleArn': os.environ['SAGEMAKER_ROLE'],  # SageMaker role ARN
        'InputDataConfig': [
            {
                'DataSource': {
                    'S3DataSource': {
                        'S3Uri': os.environ['S3_TRAINING_DATA_URI'],
                        'S3DataType': 'S3Prefix'
                    }
                },
                'TargetAttributeName': 'target'  # specify the target for training
            }
        ],
        'OutputDataConfig': {
            'S3OutputPath': os.environ['S3_OUTPUT_PATH']
        },
        'ResourceConfig': {
            'InstanceType': 'ml.m5.large',  # Training instance type
            'InstanceCount': 1,
            'VolumeSizeInGB': 50
        },
        'StoppingCondition': {
            'MaxRuntimeInSeconds': 3600
        }
    }

    # Start the SageMaker training job
    response = sagemaker_client.create_training_job(**training_job_params)

    return {
        'statusCode': 200,
        'body': json.dumps('Training job started successfully', default=str)
    }

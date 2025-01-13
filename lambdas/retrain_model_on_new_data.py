import boto3
import json
import os

def lambda_handler(event, context):
    sagemaker_client = boto3.client('sagemaker')

    # Extract the new data location from the event
    new_data_uri = event['Records'][0]['s3']['bucket']['name'] + '/' + event['Records'][0]['s3']['object']['key']

    # Start the model retraining job with the new data
    training_job_name = f"retrain-job-{new_data_uri.split('/')[-1]}"

    # Define the retraining parameters
    retraining_job_params = {
        'TrainingJobName': training_job_name,
        'AlgorithmSpecification': {
            'TrainingImage': os.environ['SAGEMAKER_IMAGE_URI'],
            'TrainingInputMode': 'File'
        },
        'RoleArn': os.environ['SAGEMAKER_ROLE'],
        'InputDataConfig': [
            {
                'DataSource': {
                    'S3DataSource': {
                        'S3Uri': f"s3://{new_data_uri}",
                        'S3DataType': 'S3Prefix'
                    }
                },
                'TargetAttributeName': 'target'
            }
        ],
        'OutputDataConfig': {
            'S3OutputPath': os.environ['S3_OUTPUT_PATH']
        },
        'ResourceConfig': {
            'InstanceType': 'ml.m5.large',
            'InstanceCount': 1,
            'VolumeSizeInGB': 50
        },
        'StoppingCondition': {
            'MaxRuntimeInSeconds': 3600
        }
    }
    
    # Start the retraining job
    response = sagemaker_client.create_training_job(**retraining_job_params)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Model retraining started successfully', default=str)
    }

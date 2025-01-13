import boto3
import json
import os

def lambda_handler(event, context):
    sagemaker_client = boto3.client('sagemaker')
    
    model_artifact = event['model_artifact']
    evaluation_data_uri = os.environ['EVALUATION_DATA_URI']
    
    # Specify the evaluation script in the container
    evaluation_script = '/opt/ml/code/evaluate.py'
    
    # Define the SageMaker model evaluation parameters
    evaluation_job_name = f"evaluation-job-{model_artifact.split('/')[-1]}"
    
    # Create a SageMaker model evaluation job
    response = sagemaker_client.create_processing_job(
        ProcessingJobName=evaluation_job_name,
        AppSpecification={
            'ImageUri': model_artifact,
            'ContainerEntrypoint': [evaluation_script],
        },
        ProcessingResources={
            'ClusterConfig': {
                'InstanceType': 'ml.m5.large',
                'InstanceCount': 1
            }
        },
        ProcessingInputConfig=[
            {
                'InputName': 'evaluation_data',
                'S3Input': {
                    'S3Uri': evaluation_data_uri,
                    'LocalPath': '/opt/ml/processing/input/data'
                }
            }
        ],
        ProcessingOutputConfig={
            'Outputs': [
                {
                    'OutputName': 'evaluation_results',
                    'S3Output': {
                        'S3Uri': os.environ['S3_EVALUATION_RESULTS_URI'],
                        'LocalPath': '/opt/ml/processing/output'
                    }
                }
            ]
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Model evaluation started successfully', default=str)
    }

import boto3
import json
import os

def lambda_handler(event, context):
    sagemaker_client = boto3.client('sagemaker')

    model_artifact = event['model_artifact']
    model_name = event['model_name']
    
    # Define the model registration parameters
    model_registry_name = os.environ['MODEL_REGISTRY_NAME']
    
    response = sagemaker_client.create_model(
        ModelName=model_name,
        PrimaryContainer={
            'Image': os.environ['MODEL_IMAGE_URI'],
            'ModelDataUrl': model_artifact
        },
        ExecutionRoleArn=os.environ['SAGEMAKER_ROLE']
    )
    
    # Register the model in the SageMaker Model Registry
    response = sagemaker_client.add_model_package(
        ModelPackageGroupName=model_registry_name,
        ModelPackageDescription="Model evaluated and ready for deployment",
        ModelDataUrl=model_artifact
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Model {model_name} registered successfully', default=str)
    }

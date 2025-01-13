import boto3
import json
import os

def lambda_handler(event, context):
    sagemaker_client = boto3.client('sagemaker')

    model_name = event['model_name']
    
    # Define the endpoint name
    endpoint_name = f"endpoint-{model_name}"

    # Deploy the model to a SageMaker endpoint
    response = sagemaker_client.create_endpoint(
        EndpointName=endpoint_name,
        EndpointConfigName=f"{model_name}-endpoint-config",
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Model deployed to endpoint {endpoint_name}', default=str)
    }

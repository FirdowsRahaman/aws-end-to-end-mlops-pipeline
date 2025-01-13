
import boto3
import json
import os
import tensorflow as tf
from botocore.exceptions import NoCredentialsError

# SageMaker and S3 clients
sagemaker_client = boto3.client('sagemaker')
s3_client = boto3.client('s3')

# Configuration
MODEL_BUCKET = os.environ.get("MODEL_BUCKET")
MODEL_KEY = os.environ.get("MODEL_KEY")
EVAL_DATA_BUCKET = os.environ.get("EVAL_DATA_BUCKET")
EVAL_DATA_KEY = os.environ.get("EVAL_DATA_KEY")
MODEL_ACCURACY_THRESHOLD = float(os.environ.get("MODEL_ACCURACY_THRESHOLD", "0.85"))
ENDPOINT_NAME = os.environ.get("ENDPOINT_NAME", "image-classification-endpoint")
ROLE_ARN = os.environ.get("ROLE_ARN")  # SageMaker execution role ARN


def download_from_s3(bucket, key, local_path):
    """Download a file from S3."""
    s3_client.download_file(bucket, key, local_path)
    print(f"Downloaded {key} from bucket {bucket} to {local_path}")


def evaluate_model(model_path, data_path):
    """Evaluate the model and return the accuracy."""
    # Load the model
    model = tf.keras.models.load_model(model_path)

    # Load the evaluation dataset
    eval_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        data_path,
        image_size=(224, 224),
        batch_size=32
    )

    # Evaluate the model
    _, accuracy = model.evaluate(eval_dataset, verbose=2)
    print(f"Model accuracy: {accuracy}")
    return accuracy


def deploy_model_to_sagemaker(model_path, endpoint_name, role_arn):
    """Deploy the model to SageMaker."""
    # Create the model in SageMaker
    model_name = f"{endpoint_name}-{int(time.time())}"
    container = {
        'Image': '763104351884.dkr.ecr.us-west-2.amazonaws.com/tensorflow-inference:2.9-cpu',  # Update region if needed
        'ModelDataUrl': f"s3://{MODEL_BUCKET}/{MODEL_KEY}",
        'Environment': {
            'SAGEMAKER_REGION': boto3.Session().region_name,
        }
    }
    sagemaker_client.create_model(
        ModelName=model_name,
        PrimaryContainer=container,
        ExecutionRoleArn=role_arn
    )
    print(f"Created SageMaker model: {model_name}")

    # Create or update the endpoint configuration
    endpoint_config_name = f"{endpoint_name}-config-{int(time.time())}"
    sagemaker_client.create_endpoint_config(
        EndpointConfigName=endpoint_config_name,
        ProductionVariants=[{
            'VariantName': 'AllTraffic',
            'ModelName': model_name,
            'InstanceType': 'ml.m5.large',
            'InitialInstanceCount': 1
        }]
    )
    print(f"Created endpoint configuration: {endpoint_config_name}")

    # Create or update the endpoint
    try:
        sagemaker_client.create_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name
        )
        print(f"Created endpoint: {endpoint_name}")
    except sagemaker_client.exceptions.ResourceInUse:
        sagemaker_client.update_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=endpoint_config_name
        )
        print(f"Updated endpoint: {endpoint_name}")


def handler(event, context):
    """Lambda function handler."""
    try:
        # Paths for local files
        model_local_path = "/tmp/model"
        eval_data_local_path = "/tmp/eval_data"

        # Download model and evaluation data from S3
        download_from_s3(MODEL_BUCKET, MODEL_KEY, model_local_path)
        download_from_s3(EVAL_DATA_BUCKET, EVAL_DATA_KEY, eval_data_local_path)

        # Evaluate the model
        accuracy = evaluate_model(model_local_path, eval_data_local_path)

        # Check if the model accuracy exceeds the threshold
        if accuracy >= MODEL_ACCURACY_THRESHOLD:
            print("Model accuracy meets the threshold, deploying to SageMaker...")
            deploy_model_to_sagemaker(model_local_path, ENDPOINT_NAME, ROLE_ARN)
        else:
            print(f"Model accuracy {accuracy} does not meet the threshold {MODEL_ACCURACY_THRESHOLD}. Not deploying.")

    except NoCredentialsError as e:
        print("AWS credentials not found.")
        raise e
    except Exception as e:
        print(f"Error in Lambda function: {str(e)}")
        raise e


if __name__ == "__main__":
    # Test locally
    handler({}, {})

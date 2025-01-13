
import boto3
import yaml
import os

# Load Configuration File
def load_config(file_path="../configs/config.yaml"):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Deploy CloudFormation Stack
def deploy_stack(cloudformation_client, stack_name, template_file, parameters, capabilities):
    with open(template_file, 'r') as file:
        template_body = file.read()

    try:
        cloudformation_client.describe_stacks(StackName=stack_name)
        print(f"Stack {stack_name} exists. Updating...")
        cloudformation_client.update_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=parameters,
            Capabilities=capabilities
        )
    except cloudformation_client.exceptions.ClientError as e:
        if "does not exist" in str(e):
            print(f"Creating stack {stack_name}...")
            cloudformation_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_body,
                Parameters=parameters,
                Capabilities=capabilities
            )
        else:
            print(f"Error deploying stack: {e}")

# Update Lambda Code
def update_lambda_code(lambda_client, function_name, s3_bucket, s3_key):
    try:
        lambda_client.update_function_code(
            FunctionName=function_name,
            S3Bucket=s3_bucket,
            S3Key=s3_key
        )
        print(f"Lambda {function_name} updated successfully.")
    except Exception as e:
        print(f"Failed to update Lambda {function_name}: {e}")

# Main Execution
def main():
    config = load_config()
    region = config['region']
    stack_name = config['stack_name']

    cloudformation_client = boto3.client('cloudformation', region_name=region)
    lambda_client = boto3.client('lambda', region_name=region)

    template_file = os.path.join("../infra/cloudformation", config['cloudformation']['template_file'])
    capabilities = config['cloudformation']['capabilities']
    parameters = [
        {
            'ParameterKey': param['name'],
            'ParameterValue': param['value']
        }
        for param in config['cloudformation']['parameters']
    ]

    deploy_stack(cloudformation_client, stack_name, template_file, parameters, capabilities)

    for function in config['lambda']['functions']:
        update_lambda_code(
            lambda_client,
            function['name'],
            config['s3']['base_bucket'],
            f"lambda/{function['name']}.zip"
        )

if __name__ == "__main__":
    main()

import yaml
import os

# Load Configuration File
def load_config(file_path="../configs/config.yaml"):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def generate_cloudformation_template(config, output_path="../infra/cloudformation/generated_pipeline.yaml"):
    template = {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Resources": {}
    }

    # Add Lambda Functions to Template
    for function in config['lambda']['functions']:
        template['Resources'][function['name']] = {
            "Type": "AWS::Lambda::Function",
            "Properties": {
                "FunctionName": function['name'],
                "Description": function['description'],
                "Handler": function['handler'],
                "Role": function['role'],
                "Runtime": function['runtime'],
                "Timeout": function['timeout'],
                "MemorySize": function['memory_size'],
                "Code": {
                    "S3Bucket": config['s3']['base_bucket'],
                    "S3Key": f"lambda/{function['name']}.zip"
                }
            }
        }

    # Save Template to File
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        yaml.dump(template, file, default_flow_style=False)
    print(f"CloudFormation template generated at {output_path}")

if __name__ == "__main__":
    config = load_config()
    generate_cloudformation_template(config)


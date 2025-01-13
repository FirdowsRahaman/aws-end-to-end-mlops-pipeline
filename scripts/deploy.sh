#!/bin/bash

# Step 1: Generate the CloudFormation Template
echo "Generating CloudFormation template..."
python scripts/generate_template.py

# Step 2: Deploy the Stack
echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file infra/cloudformation/generated_pipeline.yaml \
    --stack-name ${STACK_NAME:-my-stack} \
    --capabilities CAPABILITY_NAMED_IAM

echo "Deployment completed!"

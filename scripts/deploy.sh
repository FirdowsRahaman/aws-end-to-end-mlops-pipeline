#!/bin/bash

# Step 1: Generate the CloudFormation Template
echo "Generating CloudFormation template..."
python scripts/generate_template.py

# Step 3: Push Updated Configurations to GitHub
echo "Pushing Updated Configurations to GitHub..."
# Generate timestamp and branch name
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BRANCH_NAME="updated@$TIMESTAMP"

# Create new branch and switch to it
git checkout -b $BRANCH_NAME

# Stage and commit changes
git add .
git commit -m "Updated configurations from config.yaml"

# Push the branch to GitHub
git push origin $BRANCH_NAME

# Optionally create a pull request (requires GitHub CLI)
gh pr create --title "Update from config.yaml ($TIMESTAMP)" --body "Automated updates based on config.yaml" --base main --head $BRANCH_NAME


# Step 2: Deploy the Stack
echo "Deploying CloudFormation stack..."
aws cloudformation deploy \
    --template-file infra/cloudformation/generated_pipeline.yaml \
    --stack-name ${STACK_NAME:-my-stack} \
    --capabilities CAPABILITY_NAMED_IAM

echo "Deployment completed!"

#!/bin/bash

########################################
# Prepare content for workshop
########################################
zip -r all_content.zip ./* -x "./.venv/*" "*/node_modules/*" "*/dist/*" "./cdk.out/*" "*/python/*" "*/.angular/*" "./temp/*" "*/__pycache__/*"


########################################
# UserData prepare workshop
########################################
# Create workshop folder inside AMI
echo "Create workshop folder inside AMI"
cd /home/
mkdir -p workshop
cd /home/workshop
pwd

# Install NodeJS
echo "Install NodeJS"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm install --lts

# Install CDK CLI
echo "Install CDK"
npm install -g aws-cdk

# Install Angular CLI
echo "Install Angular CLI"
npm install -g @angular/cli
ng completion

# Install Make
echo "Install Make"
yum install -y make


# Download content from S3 bucket (CDK content source files)
# Important: the "AssetsBucketName" and "AssetsBucketPrefix" must be set...
echo "Download content from S3 bucket (CDK content source files)"
aws s3api get-object \
    --bucket "${AssetsBucketName}" \
    --key "${AssetsBucketPrefix}/all_content.zip" \
    "/home/workshop/all_content.zip"

unzip /home/workshop/all_content.zip -d /home/workshop/


# Activate Python3 virtual environment
echo "Activate Python3 virtual environment"
python3 -m venv .venv
source .venv/bin/activate

# Install poetry
pip install poetry

# Install Python dependencies for CDK Deploy
poetry install

# Deploy CDK solution
echo "Deploy CDK solution"
cdk bootstrap
export DEPLOYMENT_ENVIRONMENT=prod
export AWS_DEFAULT_REGION=us-east-1
cdk deploy --require-approval never --all


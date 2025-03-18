# Built-in imports
import os

# External imports
from aws_cdk import (
    aws_s3,
    aws_s3_deployment,
    RemovalPolicy,
    Stack,
)
from constructs import Construct


class FrontendBackendStack(Stack):
    """
    Class to create the FrontendAPI resources.
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        main_resources_name: str,
        app_config: dict[str],
        **kwargs,
    ) -> None:
        """
        :param scope (Construct): Parent of this stack, usually an 'App' or a 'Stage', but could be any construct.
        :param construct_id (str): The construct ID of this stack (same as aws-cdk Stack 'construct_id').
        :param main_resources_name (str): The main unique identified of this stack.
        :param app_config (dict[str]): Dictionary with relevant configuration values for the stack.
        """
        super().__init__(scope, construct_id, **kwargs)

        # Input parameters
        self.construct_id = construct_id
        self.main_resources_name = main_resources_name
        self.app_config = app_config
        self.deployment_environment = self.app_config["deployment_environment"]
        self.bedrock_llm_model_id = self.app_config["bedrock_llm_model_id"]
        self.agents_version = self.app_config["agents_version"]  # For major updates

        # Main methods for the deployment
        self.create_s3_buckets()
        self.upload_objects_to_s3()

    def create_s3_buckets(self):
        """
        Method to create the S3 bucket that will host the frontend files.
        """
        self.bucket_frontend = aws_s3.Bucket(
            self,
            "S3-Bucket-Frontend",
            # # Intentionally leave as random name to avoid duplicates in Workshops...
            # bucket_name=f"{self.main_resources_name}-frontend-{self.account}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            enforce_ssl=True,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
        )

    def upload_objects_to_s3(self):
        """
        Method to upload object/files to S3 bucket at deployment.
        """
        PATH_TO_S3_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "frontend",
            "dist",
            "demos-gen-ai",
            "browser",
        )

        aws_s3_deployment.BucketDeployment(
            self,
            "S3Deployment1",
            sources=[aws_s3_deployment.Source.asset(PATH_TO_S3_FOLDER)],
            destination_bucket=self.bucket_frontend,
        )

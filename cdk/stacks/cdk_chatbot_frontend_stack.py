# Built-in imports
import os

# External imports
# External imports
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_cloudfront,
    aws_cloudfront_origins,
    aws_s3,
    aws_s3_deployment,
    RemovalPolicy,
    Duration,
)
from constructs import Construct


class ChatbotFrontendStack(Stack):
    """
    Class to create the FrontendAPI resources with S3, S3 Deploy and Cloudfront.
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
        self.configure_cloudfront_distribution()

        # Generate Cloudformation outputs
        self.generate_cloudformation_outputs()

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

    def configure_cloudfront_distribution(self):
        """
        Method to configure the CloudFront distribution for the frontend.
        """
        cloudfront_origin_access_identity = aws_cloudfront.OriginAccessIdentity(
            self,
            "CloudFrontOriginAccessIdentity",
            comment=f"Origin Access Identity for the s3 frontend for {self.main_resources_name}",
        )
        self.bucket_frontend.grant_read(cloudfront_origin_access_identity)

        # TODO: enhance with better security headers (such as strictTransport, xss, etc)

        self.cloudfront_distribution = aws_cloudfront.Distribution(
            self,
            "CloudFrontDistribution",
            comment=f"CloudFront Distribution for the s3 frontend for {self.main_resources_name}",
            default_behavior=aws_cloudfront.BehaviorOptions(
                origin=aws_cloudfront_origins.S3Origin(
                    self.bucket_frontend,
                    origin_access_identity=cloudfront_origin_access_identity,
                ),
                viewer_protocol_policy=aws_cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            default_root_object="index.html",
            error_responses=[
                aws_cloudfront.ErrorResponse(
                    http_status=404,
                    ttl=Duration.seconds(1),
                    response_page_path="/index.html",
                )
            ],
            enabled=True,
        )

    def generate_cloudformation_outputs(self) -> None:
        """
        Method to add the relevant CloudFormation outputs.
        """

        CfnOutput(
            self,
            "DeploymentEnvironment",
            value=self.app_config["deployment_environment"],
            description="Deployment environment",
        )

        CfnOutput(
            self,
            "CloudFrontDistributionDomainNam",
            value=self.cloudfront_distribution.domain_name,
            description="CloudFront Distribution Domain Name",
        )

# Built-in imports
import os

# External imports
from aws_cdk import (
    Duration,
    aws_bedrock,
    aws_dynamodb,
    aws_iam,
    aws_lambda,
    aws_opensearchserverless as oss,
    aws_ssm,
    aws_s3,
    aws_s3_deployment as s3d,
    aws_apigateway as aws_apigw,
    custom_resources as cr,
    CfnOutput,
    RemovalPolicy,
    Stack,
    Tags,
)
from constructs import Construct


class ChatbotBackendStack(Stack):
    """
    Class to create the ChatbotAPI resources, which includes the API Gateway,
    Lambda Functions, DynamoDB Table and required chatbot infrastructure.
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
        self.create_dynamodb_table()
        self.create_s3_buckets()
        self.create_lambda_layers()
        self.create_lambda_functions()
        self.create_bedrock_child_agents()
        self.create_rest_api()
        self.configure_rest_api()

        # Generate CloudFormation outputs
        self.generate_cloudformation_outputs()

    def create_dynamodb_table(self):
        """
        Create DynamoDB table for storing the conversations.
        """
        self.dynamodb_table = aws_dynamodb.Table(
            self,
            "DynamoDB-Table-Chatbot",
            table_name=self.app_config["table_name"],
            partition_key=aws_dynamodb.Attribute(
                name="PK", type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="SK", type=aws_dynamodb.AttributeType.STRING
            ),
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )
        Tags.of(self.dynamodb_table).add("Name", self.app_config["table_name"])

    def create_s3_buckets(self) -> None:
        """
        Create S3 buckets for the Generative-AI Assets.
        """
        self.bucket_additional_assets = aws_s3.Bucket(
            self,
            "S3-Bucket-ExtraAssets",
            bucket_name=f"{self.main_resources_name}-extra-assets-{self.account}",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            enforce_ssl=True,
            block_public_access=aws_s3.BlockPublicAccess.BLOCK_ALL,
        )
        Tags.of(self.bucket_additional_assets).add(
            "Name", f"{self.main_resources_name}-extra-assets-{self.account}"
        )

    def create_lambda_layers(self) -> None:
        """
        Create the Lambda layers that are necessary for the additional runtime
        dependencies of the Lambda Functions.
        """

        # Layer for "LambdaPowerTools" (for logging, traces, observability, etc)
        self.lambda_layer_powertools = aws_lambda.LayerVersion.from_layer_version_arn(
            self,
            "Layer-PowerTools",
            layer_version_arn=f"arn:aws:lambda:{self.region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:71",
        )

        # Layer for "common" Python requirements (fastapi, mangum, pydantic, ...)
        self.lambda_layer_common = aws_lambda.LayerVersion(
            self,
            "Layer-Common",
            layer_version_name=f"{self.main_resources_name}-CommonLayer-{self.deployment_environment}",
            code=aws_lambda.Code.from_asset("lambda-layers/common/modules"),
            compatible_runtimes=[
                aws_lambda.Runtime.PYTHON_3_11,
            ],
            description="Lambda Layer for Python with <common> library",
            removal_policy=RemovalPolicy.DESTROY,
            compatible_architectures=[aws_lambda.Architecture.X86_64],
        )

    def create_lambda_functions(self) -> None:
        """
        Create the Lambda Functions for the solution.
        """
        # Get relative path for folder that contains Lambda function source
        # ! Note--> we must obtain parent dirs to create path (that"s why there is "os.path.dirname()")
        PATH_TO_LAMBDA_FUNCTION_FOLDER = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "backend",
        )

        # ----- LAMBDAS FOR THE API COMPONENT -----
        # Lambda Function for Chatbot input messages
        self.lambda_chatbot_api = aws_lambda.Function(
            self,
            "Lambda-Chatbot-API",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="api/v1/main.handler",
            function_name=f"{self.main_resources_name}-chatbot-api",
            code=aws_lambda.Code.from_asset(PATH_TO_LAMBDA_FUNCTION_FOLDER),
            timeout=Duration.seconds(20),
            memory_size=512,
            environment={
                "ENVIRONMENT": self.app_config["deployment_environment"],
                "LOG_LEVEL": self.app_config["log_level"],
                "DYNAMODB_TABLE": self.dynamodb_table.table_name,
                "BASE_BANK": self.app_config["base_bank"],
                "BOT_NAME": self.app_config["bot_name"],
            },
            layers=[
                self.lambda_layer_powertools,
                self.lambda_layer_common,
            ],
        )
        self.dynamodb_table.grant_read_write_data(self.lambda_chatbot_api)
        self.lambda_chatbot_api.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonSSMReadOnlyAccess",
            ),
        )
        self.lambda_chatbot_api.role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonBedrockFullAccess",
            ),
        )

        # ----- LAMBDAS FOR THE GEN-AI COMPONENT -----
        # Lambda Function for the Bedrock Agent Group (fetch recipes)
        self.bedrock_agent_lambda_role = aws_iam.Role(
            self,
            "BedrockAgentLambdaRole",
            assumed_by=aws_iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Role for Bedrock Agent Lambda",
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSLambdaBasicExecutionRole",
                ),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonBedrockFullAccess",
                ),
                aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonDynamoDBFullAccess",
                ),
            ],
        )
        # Add additional IAM actions for the bedrock agent
        self.bedrock_agent_lambda_role.add_to_policy(
            aws_iam.PolicyStatement(
                effect=aws_iam.Effect.ALLOW,
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelEndpoint",
                    "bedrock:InvokeModelEndpointAsync",
                    "iam:PassRole",
                ],
                resources=["*"],
            )
        )

        # Lambda for the Action Group (used for Bedrock Agents)
        # Note: Single Lambda for all Action Groups for now...
        self.lambda_action_groups = aws_lambda.Function(
            self,
            "Lambda-AG-Generic",
            runtime=aws_lambda.Runtime.PYTHON_3_11,
            handler="bedrock_agent/lambda_function.lambda_handler",
            function_name=f"{self.main_resources_name}-bedrock-action-groups",
            code=aws_lambda.Code.from_asset(PATH_TO_LAMBDA_FUNCTION_FOLDER),
            timeout=Duration.seconds(60),
            memory_size=512,
            environment={
                "ENVIRONMENT": self.app_config["deployment_environment"],
                "LOG_LEVEL": self.app_config["log_level"],
                "TABLE_NAME": self.app_config["agents_data_table_name"],
                "BASE_BANK": self.app_config["base_bank"],
                "BOT_NAME": self.app_config["bot_name"],
            },
            role=self.bedrock_agent_lambda_role,
        )

        # Add permissions to the Lambda functions resource policies.
        # The resource-based policy is to allow an AWS service to invoke your function.
        self.lambda_action_groups.add_permission(
            "AllowBedrockInvoke1",
            principal=aws_iam.ServicePrincipal("bedrock.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_arn=f"arn:aws:bedrock:{self.region}:{self.account}:agent/*",
        )

    def create_bedrock_child_agents(self):
        """
        Method to create the Bedrock Agents at the lowest hierarchy level (child agents).
        """

        # ------------------------------------
        # Bedrock child agent 1 (CRUD Products)
        # ------------------------------------
        agent_1_instructions = """
        You are a specialized agent in financial products. Is able to run CRUD operations towards the user products such as <FetchUserProducts> or <CreateCredit>.

        1. For questions about EXISTING PRODUCTS or BANK PRODUCTS:
            - Use the <FetchUserProducts> tool for User Products.
            - Obtain the 'from_number' from the user's input.

        2. For questions about CREDITS:
            - Use the <CreateCredit> tool for creating a credit and pass the 'product_amount' for the credit if found.
            - Obtain the 'from_number' from the user's input.
        """
        self.bedrock_agent_1 = aws_bedrock.CfnAgent(
            self,
            f"BedrockAgent{self.agents_version}CRUDProducts",
            agent_name=f"{self.main_resources_name}-agent-{self.agents_version}-financial-products",
            agent_resource_role_arn=self.bedrock_agent_lambda_role.role_arn,
            description="Agent specialized in financial products. Is able to run CRUD operations towards the user products such as <FetchUserProducts> or <CreateCredit>.",
            foundation_model=self.bedrock_llm_model_id,
            instruction=agent_1_instructions,
            auto_prepare=True,
            action_groups=[
                aws_bedrock.CfnAgent.AgentActionGroupProperty(
                    action_group_name="FetchUserProducts",
                    description="A function that is able to fetch the user products from the database from an input from_number and from_number.",
                    action_group_executor=aws_bedrock.CfnAgent.ActionGroupExecutorProperty(
                        lambda_=self.lambda_action_groups.function_arn,
                    ),
                    function_schema=aws_bedrock.CfnAgent.FunctionSchemaProperty(
                        functions=[
                            aws_bedrock.CfnAgent.FunctionProperty(
                                name="FetchUserProducts",
                                # the properties below are optional
                                description="Function to fetch the user products based on the input input from_number",
                                parameters={
                                    "from_number": aws_bedrock.CfnAgent.ParameterDetailProperty(
                                        type="string",
                                        description="from_number to fetch the user products",
                                        required=True,
                                    ),
                                },
                            )
                        ]
                    ),
                ),
                aws_bedrock.CfnAgent.AgentActionGroupProperty(
                    action_group_name="CreateCredit",
                    description="A function that is able to create credits from an input 'from_number' and 'product_amount'.",
                    action_group_executor=aws_bedrock.CfnAgent.ActionGroupExecutorProperty(
                        lambda_=self.lambda_action_groups.function_arn,
                    ),
                    function_schema=aws_bedrock.CfnAgent.FunctionSchemaProperty(
                        functions=[
                            aws_bedrock.CfnAgent.FunctionProperty(
                                name="CreateCredit",
                                # the properties below are optional
                                description="Function to create credits based on the 'from_number' and 'product_amount'.",
                                parameters={
                                    "from_number": aws_bedrock.CfnAgent.ParameterDetailProperty(
                                        type="string",
                                        description="from_number to create the credit",
                                        required=True,
                                    ),
                                    "product_amount": aws_bedrock.CfnAgent.ParameterDetailProperty(
                                        type="string",
                                        description="product_amount to create the credit",
                                        required=False,
                                    ),
                                },
                            )
                        ]
                    ),
                ),
            ],
        )

        # ------------------------------------
        # Bedrock child agent 2 (Certificates)
        # ------------------------------------
        agent_2_instructions = """
        You are a specialized agent in Bank Certificates. Is able to generate PDF certificates with <GenerateCertificates>.",
        """
        self.bedrock_agent_2 = aws_bedrock.CfnAgent(
            self,
            f"BedrockAgent{self.agents_version}Certificates",
            agent_name=f"{self.main_resources_name}-agent-{self.agents_version}-certificates",
            agent_resource_role_arn=self.bedrock_agent_lambda_role.role_arn,
            description="Agent specialized in certificates. Is able to generate PDF certificates with <GenerateCertificates>.",
            foundation_model=self.bedrock_llm_model_id,
            instruction=agent_2_instructions,
            auto_prepare=True,
            action_groups=[
                aws_bedrock.CfnAgent.AgentActionGroupProperty(
                    action_group_name="GenerateCertificates",
                    description="A function that is able to generate the user certificates from an input from_number.",
                    action_group_executor=aws_bedrock.CfnAgent.ActionGroupExecutorProperty(
                        lambda_=self.lambda_action_groups.function_arn,
                    ),
                    function_schema=aws_bedrock.CfnAgent.FunctionSchemaProperty(
                        functions=[
                            aws_bedrock.CfnAgent.FunctionProperty(
                                name="GenerateCertificates",
                                # the properties below are optional
                                description="Function to generate user certificates or bank certificates based on the input from_number",
                                parameters={
                                    "from_number": aws_bedrock.CfnAgent.ParameterDetailProperty(
                                        type="string",
                                        description="from_number to generate user certificates",
                                        required=True,
                                    ),
                                },
                            )
                        ]
                    ),
                ),
            ],
        )

        # ------------------------------------
        # Bedrock child agent 2 (Bank Rewards)
        # ------------------------------------
        agent_3_instructions = """
        You are a specialized agent in Bank Rewards. Is able to get user rewards with <GetBankRewards>.",
        """
        self.bedrock_agent_2 = aws_bedrock.CfnAgent(
            self,
            f"BedrockAgent{self.agents_version}BankRewards",
            agent_name=f"{self.main_resources_name}-agent-{self.agents_version}-bank-rewards",
            agent_resource_role_arn=self.bedrock_agent_lambda_role.role_arn,
            description="Agent specialized in bank rewards. Is able to get user rewards with <GetBankRewards>.",
            foundation_model=self.bedrock_llm_model_id,
            instruction=agent_3_instructions,
            auto_prepare=True,
            action_groups=[
                aws_bedrock.CfnAgent.AgentActionGroupProperty(
                    action_group_name="GetBankRewards",
                    description="A function that is able to get Colombian Points or bank rewards from an input from_number.",
                    action_group_executor=aws_bedrock.CfnAgent.ActionGroupExecutorProperty(
                        lambda_=self.lambda_action_groups.function_arn,
                    ),
                    function_schema=aws_bedrock.CfnAgent.FunctionSchemaProperty(
                        functions=[
                            aws_bedrock.CfnAgent.FunctionProperty(
                                name="GetBankRewards",
                                # the properties below are optional
                                description="Function to get Colombian Points or bank rewards based on the input from_number",
                                parameters={
                                    "from_number": aws_bedrock.CfnAgent.ParameterDetailProperty(
                                        type="string",
                                        description="from_number to get Colombian Points or bank rewards",
                                        required=True,
                                    ),
                                },
                            )
                        ]
                    ),
                ),
                # aws_bedrock.CfnAgent.AgentActionGroupProperty(
                #     action_group_name="FetchMarketInsights",
                #     description="A function that is able to fetch the latest market insights knowing the <risk_level> for the user.",
                #     action_group_executor=aws_bedrock.CfnAgent.ActionGroupExecutorProperty(
                #         lambda_=self.lambda_action_group_market_insights.function_arn,
                #     ),
                #     function_schema=aws_bedrock.CfnAgent.FunctionSchemaProperty(
                #         functions=[
                #             aws_bedrock.CfnAgent.FunctionProperty(
                #                 name="FetchMarketInsights",
                #                 # the properties below are optional
                #                 description="Function that is able to fetch the latest market insights knowing the <risk_level> for the user.",
                #                 parameters={
                #                     "risk_level": aws_bedrock.CfnAgent.ParameterDetailProperty(
                #                         type="string",
                #                         description="Risk level to fetch the market insights",
                #                         required=True,
                #                     ),
                #                 },
                #             )
                #         ]
                #     ),
                # ),
                # aws_bedrock.CfnAgent.AgentActionGroupProperty(
                #     action_group_name="StartTransaction",
                #     description="A function that is able to start a transaction for the user with the 'from_number', 'receiver_key' and 'amount' inputs.",
                #     action_group_executor=aws_bedrock.CfnAgent.ActionGroupExecutorProperty(
                #         lambda_=self.lambda_action_group_transactions.function_arn,
                #     ),
                #     function_schema=aws_bedrock.CfnAgent.FunctionSchemaProperty(
                #         functions=[
                #             aws_bedrock.CfnAgent.FunctionProperty(
                #                 name="StartTransaction",
                #                 # the properties below are optional
                #                 description="Function that is able to start a transaction for the user with the 'from_number', 'receiver_key' and 'amount' inputs.",
                #                 parameters={
                #                     "from_number": aws_bedrock.CfnAgent.ParameterDetailProperty(
                #                         type="string",
                #                         description="from_number for the transaction",
                #                         required=True,
                #                     ),
                #                     "receiver_key": aws_bedrock.CfnAgent.ParameterDetailProperty(
                #                         type="string",
                #                         description="receiver_key for the transaction",
                #                         required=True,
                #                     ),
                #                     "amount": aws_bedrock.CfnAgent.ParameterDetailProperty(
                #                         type="string",
                #                         description="amount for the transaction",
                #                         required=True,
                #                     ),
                #                 },
                #             )
                #         ]
                #     ),
                # ),
                # aws_bedrock.CfnAgent.AgentActionGroupProperty(
                #     action_group_name="ConfirmTransaction",
                #     description="A function that is able to confirm a transaction for the user with the 'from_number', 'receiver_key' and 'amount' inputs.",
                #     action_group_executor=aws_bedrock.CfnAgent.ActionGroupExecutorProperty(
                #         lambda_=self.lambda_action_group_transactions.function_arn,
                #     ),
                #     function_schema=aws_bedrock.CfnAgent.FunctionSchemaProperty(
                #         functions=[
                #             aws_bedrock.CfnAgent.FunctionProperty(
                #                 name="ConfirmTransaction",
                #                 # the properties below are optional
                #                 description="Function that is able to confirm a transaction for the user with the 'from_number', 'receiver_key' and 'amount' inputs.",
                #                 parameters={
                #                     "from_number": aws_bedrock.CfnAgent.ParameterDetailProperty(
                #                         type="string",
                #                         description="from_number for the transaction",
                #                         required=True,
                #                     ),
                #                     "receiver_key": aws_bedrock.CfnAgent.ParameterDetailProperty(
                #                         type="string",
                #                         description="receiver_key for the transaction",
                #                         required=True,
                #                     ),
                #                     "amount": aws_bedrock.CfnAgent.ParameterDetailProperty(
                #                         type="string",
                #                         description="amount for the transaction",
                #                         required=True,
                #                     ),
                #                 },
                #             )
                #         ]
                #     ),
                # ),
                # aws_bedrock.CfnAgent.AgentActionGroupProperty(
                #     action_group_name="ConnectWithAssistant",
                #     description="A function that is able to connect with an assistant in case that an advanced request occurs. Uses from input the 'from_number'.",
                #     action_group_executor=aws_bedrock.CfnAgent.ActionGroupExecutorProperty(
                #         lambda_=self.lambda_action_group_connect_with_assistant.function_arn,
                #     ),
                #     function_schema=aws_bedrock.CfnAgent.FunctionSchemaProperty(
                #         functions=[
                #             aws_bedrock.CfnAgent.FunctionProperty(
                #                 name="ConnectWithAssistant",
                #                 # the properties below are optional
                #                 description="Function that is able to connect with an assistant in case that an advanced request occurs. Uses from input the 'from_number'.",
                #                 parameters={
                #                     "from_number": aws_bedrock.CfnAgent.ParameterDetailProperty(
                #                         type="string",
                #                         description="from_number of the user",
                #                         required=True,
                #                     ),
                #                 },
                #             )
                #         ]
                #     ),
                # ),
                # aws_bedrock.CfnAgent.AgentActionGroupProperty(
                #     action_group_name="GetExtraInformation",
                #     description="A function that is able to connect with an assistant in case that an advanced request occurs. Uses from input the 'from_number'.",
                #     action_group_executor=aws_bedrock.CfnAgent.ActionGroupExecutorProperty(
                #         lambda_=self.lambda_action_group_get_extra_information.function_arn,
                #     ),
                #     function_schema=aws_bedrock.CfnAgent.FunctionSchemaProperty(
                #         functions=[
                #             aws_bedrock.CfnAgent.FunctionProperty(
                #                 name="GetExtraInformation",
                #                 # the properties below are optional
                #                 description="Function that is able to get additional information for the user based on the Bank's KBs.",
                #                 parameters={
                #                     "requested_information": aws_bedrock.CfnAgent.ParameterDetailProperty(
                #                         type="string",
                #                         description="The extra 'requested_information' from the user.",
                #                         required=True,
                #                     ),
                #                 },
                #             )
                #         ]
                #     ),
                # ),
            ],
        )

        # Create SSM Parameters for the agent alias to use in the Lambda functions
        # Note: intentionally don't set it as part of the WORKSHOP MANUAL steps
        aws_ssm.StringParameter(
            self,
            "SSMAgentAlias",
            parameter_name=f"/{self.deployment_environment}/{self.main_resources_name}/bedrock-agent-alias-id",
            string_value="REPLACE_ME_WITH_SUPERVISOR_AGENT_ALIAS_ID",
        )
        aws_ssm.StringParameter(
            self,
            "SSMAgentId",
            parameter_name=f"/{self.deployment_environment}/{self.main_resources_name}/bedrock-agent-id",
            string_value="REPLACE_ME_WITH_SUPERVISOR_AGENT_ID",
        )

    def create_rest_api(self):
        """
        Method to create the REST-API Gateway for exposing the chatbot
        functionalities.
        """

        # API Method Options for the REST-API Gateway
        # TODO: Currently public, as validation happens in the Lambda Function for now
        self.api_method_options_public = aws_apigw.MethodOptions(
            api_key_required=False,
            authorization_type=aws_apigw.AuthorizationType.NONE,
        )

        # TODO: Add domain_name with custom DNS
        # TODO: Enable custom models and schema validations
        rest_api_name = self.app_config["api_gw_name"]
        self.api = aws_apigw.LambdaRestApi(
            self,
            "RESTAPI",
            rest_api_name=rest_api_name,
            description=f"REST API Gateway for {self.main_resources_name} in {self.deployment_environment} environment",
            handler=self.lambda_chatbot_api,
            deploy_options=aws_apigw.StageOptions(
                stage_name=self.deployment_environment,
                description=f"REST API for {self.main_resources_name}",
                metrics_enabled=True,
            ),
            default_cors_preflight_options=aws_apigw.CorsOptions(
                allow_origins=aws_apigw.Cors.ALL_ORIGINS,
                allow_methods=["GET", "POST"],
                allow_headers=["*"],
            ),
            default_method_options=self.api_method_options_public,
            endpoint_types=[aws_apigw.EndpointType.REGIONAL],
            cloud_watch_role=False,
            proxy=False,  # Proxy disabled to have more control
        )

    def configure_rest_api(self):
        """
        Method to configure the REST-API Gateway with resources and methods.
        """

        # Define REST-API resources
        root_resource_api = self.api.root.add_resource("api")
        root_resource_v1 = root_resource_api.add_resource("v1")

        # Endpoints for automatic Swagger docs (no auth required)
        root_resource_docs = root_resource_v1.add_resource("docs")
        root_resource_docs_proxy = root_resource_docs.add_resource("{path}")

        # Endpoints for the main functionalities
        root_resource_invokemodel = root_resource_v1.add_resource("invokemodel")

        # Define all API-Lambda integrations for the API methods
        api_lambda_integration_chatbot = aws_apigw.LambdaIntegration(
            self.lambda_chatbot_api
        )

        # API-Path: "/api/v1/invokemodel"
        root_resource_invokemodel.add_method("GET", api_lambda_integration_chatbot)
        root_resource_invokemodel.add_method("POST", api_lambda_integration_chatbot)

        # API-Path: "/api/v1/docs"
        root_resource_docs.add_method("GET", api_lambda_integration_chatbot)

        # API-Path: "/api/v1/docs/openapi.json
        root_resource_docs_proxy.add_method("GET", api_lambda_integration_chatbot)

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
            "APIDocs",
            value=f"https://{self.api.rest_api_id}.execute-api.{self.region}.amazonaws.com/{self.deployment_environment}/api/v1/docs",
            description="API endpoint Docs",
        )

        CfnOutput(
            self,
            "APIChatbot",
            value=f"https://{self.api.rest_api_id}.execute-api.{self.region}.amazonaws.com/{self.deployment_environment}/api/v1/webhook",
            description="API endpoint Chatbot",
        )

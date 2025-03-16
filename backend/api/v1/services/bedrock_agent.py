# Built-in imports
import os
import boto3

# Own imports
from common.logger import custom_logger


BASE_BANK = os.environ.get("BASE_BANK", "RufusBank")
ENVIRONMENT = os.environ.get("ENVIRONMENT")

logger = custom_logger()

# Create a bedrock runtime client
bedrock_agent_runtime_client = boto3.client("bedrock-agent-runtime")
ssm_client = boto3.client("ssm")


def get_ssm_parameter(parameter_name):
    """
    Fetches the parameter value from SSM Parameter Store.
    """
    response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
    return response["Parameter"]["Value"]


def call_bedrock_agent(
    input_text: str, unique_session_id: str = "TmpBedrockSession"
) -> str:
    """
    Function that based on the values of these 2 SSM Parameter Store Parameters:
        </{ENVIRONMENT}/{BASE_BANK}/bedrock-agent-alias-id>
        </{ENVIRONMENT}/{BASE_BANK}/bedrock-agent-id>
    Is able to invoke Bedrock Agents and fetch the text response dynamically with retries and
    error handling.
    """

    # TODO: Update to use PowerTools SSM Params for optimization
    AGENT_ALIAS_ID = get_ssm_parameter(
        f"/{ENVIRONMENT}/{BASE_BANK}/bedrock-agent-alias-id"
    )
    AGENT_ALIAS_ID = AGENT_ALIAS_ID.split("|")[-1]
    AGENT_ID = get_ssm_parameter(f"/{ENVIRONMENT}/{BASE_BANK}/bedrock-agent-id")

    # Validation for workshop (before parameter is replaced...) MANUAL ACTION REQUIRED...
    if AGENT_ALIAS_ID.startswith("REPLACE_ME_WITH"):
        text_response = "Please replace the SSM parameters value for AGENT_ALIAS_ID"
        logger.warning(text_response)
        return text_response

    # Add error handling and retries
    total_retries = 4
    retries = 0

    while retries < total_retries:
        response_message = bedrock_agent_runtime_client.invoke_agent(
            agentAliasId=AGENT_ALIAS_ID,
            agentId=AGENT_ID,
            enableTrace=False,
            inputText=input_text,
            sessionId=unique_session_id,
        )

        if response_message:  # Check if response is not empty
            break
        retries += 1
        if retries < total_retries:
            logger.info(f"Retrying... Attempt {retries + 1}/{total_retries}")
        else:
            logger.error("Maximum retries reached. No valid response received.")
            response_message = (
                "Hubo un pequeño problema. Por favor repite el mensaje..."
            )

    logger.info(response_message)

    stream = response_message.get("completion")
    text_response = ""
    if stream:
        for event in stream:
            chunk = event.get("chunk")
            logger.info("-----")
            text_response += chunk.get("bytes").decode()
    logger.info(text_response)
    # TODO: Add better error handling and validations/checks

    return text_response

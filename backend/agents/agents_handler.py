# NOTE: This is a MVP code for demo purposes only. Enhance it to make it production-grade.

# Own imports
from common.logger import custom_logger
from agents.bank_certificates.entrypoint import action_group_generate_certificates
from agents.bank_rewards.entrypoint import action_group_get_rewards
from agents.crud_user_products.entrypoint import (
    action_group_fetch_user_products,
    action_group_create_credit,
)


logger = custom_logger()


def lambda_handler(event, context):
    tool = event["actionGroup"]
    _function = event["function"]
    parameters = event.get("parameters", [])

    logger.info(f"PARAMETERS ARE: {parameters}")
    logger.info(f"ACTION GROUP IS: {tool}")

    # TODO: enhance this If-Statement approach to a dynamic one...
    if tool == "GenerateCertificates" or tool == "<GenerateCertificates>":
        results = action_group_generate_certificates(parameters)
    elif tool == "GetBankRewards" or tool == "<GetBankRewards>":
        results = action_group_get_rewards(parameters)
    elif tool == "FetchUserProducts" or tool == "<FetchUserProducts>":
        results = action_group_fetch_user_products(parameters)
    elif tool == "CreateCredit" or tool == "<CreateCredit>":
        results = action_group_create_credit(parameters)
    else:
        raise ValueError(f"Action Group <{tool}> not supported.")

    # Convert the list of events to a string to be able to return it in the response as a string
    response_body = {"TEXT": {"body": str(results)}}

    action_response = {
        "actionGroup": tool,
        "function": _function,
        "functionResponse": {"responseBody": response_body},
    }

    function_response = {
        "response": action_response,
        "messageVersion": event["messageVersion"],
    }
    logger.info("Response: {}".format(function_response))

    return function_response

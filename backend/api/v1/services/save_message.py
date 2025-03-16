# Helpers to save input/output messages to DynamoDB table...
# Built-in imports
import os
from datetime import datetime, timezone

# Own imports
from common.logger import custom_logger
from common.helpers.dynamodb_helper import DynamoDBHelper

logger = custom_logger()

# Initialize DynamoDB Helper
DYNAMODB_TABLE = os.environ["DYNAMODB_TABLE"]
ENDPOINT_URL = os.environ.get("ENDPOINT_URL")  # Used for local testing
dynamodb_helper = DynamoDBHelper(table_name=DYNAMODB_TABLE, endpoint_url=ENDPOINT_URL)


def save_message(from_number, message, correlation_id, message_io_type):

    if not from_number:
        from_number = "123456789"  # Future default number based on unique ID (such as UserAgent and IP)
    created_at = datetime.now(timezone.utc).isoformat()

    try:
        # Save the input message in DynamoDB
        message_item = {
            "PK": f"NUMBER#{from_number}",
            "SK": f"MESSAGE#{created_at}",
            "from_number": from_number,
            "created_at": created_at,
            "text": message,
            "type": "text",
            "message_io_type": message_io_type,  # input/output
            "correlation_id": correlation_id,
        }
        logger.info(
            str(message_item),
            message_details="Successfully created TextMessageModel instance",
        )
        result = dynamodb_helper.put_item(message_item)
        logger.debug(result, message_details="DynamoDB put_item() result")
        return result
    except Exception as e:
        logger.error(f"Error in save_message(): {e}")
        raise e

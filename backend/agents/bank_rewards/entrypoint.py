# NOTE: This is a MVP code for demo purposes only. Enhance it to make it production-grade.
# Built-in imports
import os

# Own imports
from common.logger import custom_logger
from common.helpers.dynamodb_helper import DynamoDBHelper


TABLE_NAME = os.environ["TABLE_NAME"]  # Mandatory to pass table name as env var


logger = custom_logger()
dynamodb_helper = DynamoDBHelper(table_name=TABLE_NAME)


def action_group_get_rewards(parameters):
    # Extract user_id from parameters
    user_id = None
    for param in parameters:
        if param["name"] == "from_number":
            from_number = param["value"]
            user_id = param["value"]  # User ID is also the from_number for now...

    rewards = dynamodb_helper.query_by_pk_and_sk_begins_with(
        partition_key=f"USER#{user_id}",
        sort_key_portion="REWARDS#",
    )

    logger.debug(f"rewards: {rewards}")

    return rewards

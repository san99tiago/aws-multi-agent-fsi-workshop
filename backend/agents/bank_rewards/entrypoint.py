# NOTE: This is a MVP code for demo purposes only. Enhance it to make it production-grade.
# Copyright 2025 Amazon Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
    user_id = "123456789"  # Intentionally set default number for workshop
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

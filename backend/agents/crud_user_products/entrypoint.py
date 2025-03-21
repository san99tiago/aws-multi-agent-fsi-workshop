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


def action_group_fetch_user_products(parameters):
    # Extract user_id from parameters
    user_id = "123456789"  # Intentionally set default number for workshop
    for param in parameters:
        if param["name"] == "from_number":
            user_id = param["value"]  # User ID is also the from_number for now...

    all_user_products = dynamodb_helper.query_by_pk_and_sk_begins_with(
        partition_key=f"USER#{user_id}",
        sort_key_portion="PRODUCT#",
    )
    logger.info(f"all_user_products: {all_user_products}")
    return all_user_products


def action_group_create_credit(parameters):
    # Extract user_id from parameters
    user_id = "123456789"  # Intentionally set default number for workshop
    for param in parameters:
        if param["name"] == "from_number":
            user_id = param["value"]  # User ID is also the from_number for now...
        if param["name"] == "product_amount":
            product_amount = param["value"]

    # ------------------------------
    # 1) CREDIT PROCESS...
    # ------------------------------

    # Get Current Balance of Credit
    credit_product = dynamodb_helper.get_item_by_pk_and_sk(
        partition_key=f"USER#{user_id}",
        sort_key="PRODUCT#03",  # Always leveraging ID 03 for credits (for now...)
    )
    logger.debug(f"credit_product: {credit_product}")

    try:
        total_credit = credit_product.get("total_amount", {})["S"]
        logger.info(f"Total credit balance: {total_credit}")

        # Update Credit Balance
        new_total_credit = float(total_credit) + float(product_amount)
        logger.info(f"New total credit: {new_total_credit}")
        dynamodb_helper.put_item(
            data={
                "PK": f"USER#{user_id}",
                "SK": "PRODUCT#03",
                "product_name": "Credit",
                "total_amount": str(new_total_credit),
            }
        )
        logger.info(f"New total credit balance: {new_total_credit}")

    except Exception as e:
        logger.error(f"Error getting bank credit data: {e}")
        return "Product <Credit> had a problem, one of our advanced agents will call you soon! Be aware!"

    # ------------------------------
    # 2) SAVINGS ACCOUNT PROCESS...
    # ------------------------------

    # Get Current Balance of Savings Account
    savings_product = dynamodb_helper.get_item_by_pk_and_sk(
        partition_key=f"USER#{user_id}",
        sort_key="PRODUCT#01",
    )
    logger.debug(f"savings_product: {savings_product}")
    try:
        logger.info(f"Bank account data: {savings_product}")
        total_balance = savings_product.get("total_amount", {})["S"]
        logger.info(f"Total balance: {total_balance}")

        # Update Savings Account Balance
        new_total_balance = float(total_balance) + float(product_amount)
        logger.info(f"New total balance: {new_total_balance}")
        dynamodb_helper.put_item(
            data={
                "PK": f"USER#{user_id}",
                "SK": "PRODUCT#01",
                "product_name": savings_product["product_name"]["S"],
                "last_digits": savings_product["last_digits"]["S"],
                "details": savings_product["details"]["S"],
                "status": savings_product["status"]["S"],
                "total_amount": str(new_total_balance),
            }
        )
        logger.info(f"New total balance: {new_total_balance}")

    except Exception as e:
        logger.error(f"Error getting bank account data: {e}")
        return "Product <Credit> had a problem, one of our advanced agents will call you soon! Be aware!"

    return (
        f"Product <Credit> created successfully with total amount of {product_amount}!"
    )

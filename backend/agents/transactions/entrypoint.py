# NOTE: This is a super-MVP code for testing. Still has a lot of gaps to solve/fix. Do not use in prod.
# Copyright 2025 Amazon Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# Built-in imports
import os
import time
import uuid


# Own imports
from agents.transactions.generate_transaction_receipt import (
    create_transaction_receipt_image,
)
from agents.transactions.s3_helper import upload_image_to_s3
from common.logger import custom_logger
from common.helpers.dynamodb_helper import DynamoDBHelper

TABLE_NAME = os.environ["TABLE_NAME"]  # Mandatory to pass table name as env var
BUCKET_NAME = os.environ["BUCKET_NAME"]  # Mandatory to pass S3 Bucket name as env var
BASE_BANK = os.environ.get("BASE_BANK", "DemoBank")


logger = custom_logger()

dynamodb_helper_agents_data = DynamoDBHelper(table_name=TABLE_NAME)


def action_group_start_transaction(parameters):
    # Extract user_id from parameters
    user_id = "123456789"  # Intentionally set default number for workshop
    for param in parameters:
        if param["name"] == "from_number":
            user_id = param["value"]  # User ID is also the from_number for now...
        if param["name"] == "receiver_key":
            receiver_key = param["value"]
        if param["name"] == "amount":
            amount = param["value"]

    # Validate if we have enough money for the transaction...
    bank_account_data = dynamodb_helper_agents_data.get_item_by_pk_and_sk(
        partition_key=f"USER#{user_id}",
        sort_key="PRODUCT#01",  # Note: Savings account always first product for now...
    )

    bank_account_balance = float(
        bank_account_data.get("total_amount", {}).get("S", "0")
    )

    # Check if enough money available... if not, cancel transaction...
    if bank_account_balance < float(amount):
        logger.error(
            f"Insufficient funds for transaction. \n - from_user: {user_id}\n - receiver: {receiver_key}\n - amount: {amount}"
        )

        bank_error_message = {
            "RufusBank": f"La transacción no fue posible - Detalles: tu saldo actual en la cuenta es insuficiente, pues tienes {bank_account_balance} COP.\n Propuesta: si te gustaría abrir el crédito pre-aprobado? responde: 'abrir crédito pre-aprobado'.",
        }

        return bank_error_message[BASE_BANK]

    message = f"Transaction started successfully for: \n - from_user: {user_id}\n - receiver: {receiver_key}\n - amount: {amount}"
    logger.info(message)

    return message


def action_group_confirm_transaction(parameters):
    # Extract user_id from parameters
    user_id = "123456789"  # Intentionally set default number for workshop
    for param in parameters:
        if param["name"] == "from_number":
            user_id = param["value"]  # User ID is also the from_number for now...
        if param["name"] == "receiver_key":
            receiver_key = param["value"]
        if param["name"] == "amount":
            amount = param["value"]

    # Create confirmed transaction (inject DynamoDB Item)
    dynamodb_helper_agents_data.put_item(
        data={
            "PK": f"USER#{user_id}",
            "SK": f"TRANSACTION#{int(time.time())}",
            "sender_key": user_id,
            "receiver_key": receiver_key,
            "amount": amount,
        }
    )

    # Update Savings Account Balance
    # Get Current Balance of Savings Account
    savings_product = dynamodb_helper_agents_data.get_item_by_pk_and_sk(
        partition_key=f"USER#{user_id}",
        sort_key="PRODUCT#01",
    )
    logger.debug(f"savings_product: {savings_product}")
    try:
        logger.info(f"Bank account data: {savings_product}")
        total_balance = savings_product.get("total_amount", {})["S"]
        logger.info(f"Total balance: {total_balance}")

        # Update Savings Account Balance
        new_total_balance = float(total_balance) - float(amount)
        logger.info(f"New total balance: {new_total_balance}")
        dynamodb_helper_agents_data.put_item(
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

    message = f"Transaction confirmed successfully for: \n - from_user: {user_id}\n - receiver: {receiver_key}\n - amount: {amount}"
    logger.info(message)

    # Send Transaction receipt (IMAGE) As part of the final process
    image_local_path = create_transaction_receipt_image(
        from_number=user_id,
        receiver_key=receiver_key,
        amount=amount,
    )
    logger.info(f"Image created and saved locally as {image_local_path}")

    # Upload the local certificate to an S3 bucket and generate public URL for 10 mins
    image_receipt_presigned_url = upload_image_to_s3(
        bucket_name=BUCKET_NAME,
        file_path=image_local_path,
        object_name=f"images/{str(uuid.uuid4())}/bank_receipt.png",
    )

    logger.debug(
        image_receipt_presigned_url,
        message_details="Image receipt URL",
    )

    return image_receipt_presigned_url

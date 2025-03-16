# CUSTOM RESOURCE SCRIPT TO LOAD SAMPLE DATA TO DYNAMODB FOR WORKSHOP
from __future__ import print_function
import os
import boto3

# Lib taken from:
# --> https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-lambda-function-code-cfnresponsemodule.html
import cfnresponse


# IMPORTANT: Replace these with your own phones!!!
PHONE_NUMBER_1 = "123456789"  # Demo number (intentional for Workshop)
DYNAMODB_TABLE_NAME = os.environ["DYNAMODB_TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def load_data():
    items = [
        # LOAD DEMO USER PROFILES...
        {
            "PK": f"USER#{PHONE_NUMBER_1}",
            "SK": "PROFILE#",
            "first_name": "Amigo",
            "last_name": "User",
            "email": "amigo@example.com",
            "phone_number": f"{PHONE_NUMBER_1}",
            "address": "123 Main St, Anytown, COL",
        },
        {
            "PK": "USERNAME#santigrc",
            "SK": "MAPPINGS#",
            "phone": PHONE_NUMBER_1,
        },
        # LOAD DEMO USER PRODUCTS...
        {
            "PK": f"USER#{PHONE_NUMBER_1}",
            "SK": "PRODUCT#01",
            "product_name": "Bank Account",
            "last_digits": "1111",
            "details": "Savings Account",
            "status": "ACTIVE",
            "total_amount": "500000",
        },
        {
            "PK": f"USER#{PHONE_NUMBER_1}",
            "SK": "PRODUCT#02",
            "product_name": "Credit Card",
            "last_digits": "2222",
            "details": "Visa",
            "status": "BLOCKED",
        },
        {
            "PK": f"USER#{PHONE_NUMBER_1}",
            "SK": "PRODUCT#03",
            "product_name": "Credit",
            "last_digits": "3333",
            "details": "Credit",
            "status": "ACTIVE",
            "total_amount": "100000",
        },
        # LOAD DEMO REWARDS
        {
            "PK": f"USER#{PHONE_NUMBER_1}",
            "SK": "REWARDS#",
            "product_name": "Puntos Colombia",
            "last_digits": "N/A",
            "details": "You have 1500 Puntos Colombia. Puntos Colombia are redeemable rewards to use on everyday tasks",
            "status": "ACTIVE",
        },
    ]

    # Load data to DynamoDB
    for item in items:
        print(f"Loading item: {item}")
        result = table.put_item(Item=item)
        print(f"Result: {result} \n")

    return {
        "response": "ok",
        "table_name": DYNAMODB_TABLE_NAME,
    }


def handler(event, context):
    """Lambda Handler for the Custom Resource."""
    print(f"Input custom-resource event is: {event}")

    action = event["RequestType"]

    try:
        print(f"action is: {action}")
        data_response_dict = {}

        if action == "Create" or action == "Update":
            data_response_dict = load_data()

        cfnresponse.send(
            event,
            context,
            cfnresponse.SUCCESS,
            data_response_dict,
        )
    except Exception as e:
        cfnresponse.send(
            event,
            context,
            cfnresponse.FAILED,
            {
                "Data": str(e),
            },
        )

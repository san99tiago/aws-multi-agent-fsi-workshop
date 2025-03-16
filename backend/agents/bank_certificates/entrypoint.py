# NOTE: This is a MVP code for demo purposes only. Enhance it to make it production-grade.
# Built-in imports
import os
import uuid


# Own imports
from common.logger import custom_logger
from common.helpers.dynamodb_helper import DynamoDBHelper
from agents.bank_certificates.generate_certificates import generate_certificate_pdf
from agents.bank_certificates.s3_helper import upload_pdf_to_s3


BASE_BANK = os.environ.get("BASE_BANK", "RufusBank")
TABLE_NAME = os.environ["TABLE_NAME"]  # Mandatory to pass table name as env var
BUCKET_NAME = os.environ["BUCKET_NAME"]  # Mandatory to pass table name as env var


logger = custom_logger()
dynamodb_helper = DynamoDBHelper(table_name=TABLE_NAME)


def action_group_generate_certificates(parameters):
    # Extract user_id from parameters
    user_id = None
    for param in parameters:
        if param["name"] == "from_number":
            from_number = param["value"]
            user_id = param["value"]  # User ID is also the from_number for now...

    all_user_products = dynamodb_helper.query_by_pk_and_sk_begins_with(
        partition_key=f"USER#{user_id}",
        sort_key_portion="PRODUCT#",
    )

    logger.debug(f"all_user_products: {all_user_products}")

    # Generate the PDF file and save it locally
    certificate_local_path = generate_certificate_pdf(
        product_list=all_user_products,
        location="Medellin, Colombia",
    )

    logger.debug(f"certificate_local_path: {certificate_local_path}")

    # Upload the local certificate to an S3 bucket and generate public URL for 10 mins
    certificate_url = upload_pdf_to_s3(
        bucket_name=BUCKET_NAME,
        file_path=certificate_local_path,
        object_name=f"certificates/{str(uuid.uuid4())}/bank_certificate.pdf",
    )

    # TODO: Update to a PRESIGNED-URL!!!

    logger.info(f"Certificate URL: {certificate_url}")
    return f"Certificate generated successfully for {BASE_BANK} client at {certificate_url}!"

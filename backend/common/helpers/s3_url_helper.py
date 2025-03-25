import os
import mimetypes
import boto3

# Own imports
from common.logger import custom_logger

logger = custom_logger()
s3_client = boto3.client("s3")


def generate_presigned_url(bucket_name, object_name=None, expiration=6000) -> str:
    """
    Generates an URL for an S3 bucket and generates a temporary public URL.

    :param bucket_name: The name of the S3 bucket.
    :param object_name: The S3 object name. If None, file_path's basename is used.
    :param expiration: Time in seconds for the pre-signed URL to remain valid.
    :return: The pre-signed URL or an error message.
    """
    try:
        logger.info(f"Generating pre-signed URL for S3 object = {object_name}")

        # Generate a pre-signed URL
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_name},
            ExpiresIn=expiration,
        )
        logger.debug(f"Pre-signed URL generated: {presigned_url}")
        return presigned_url
    except Exception as e:
        logger.error(f"Error generating pre-signed URL: {e}")
        return f"An unexpected error occurred: {e}"

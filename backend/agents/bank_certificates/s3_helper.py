import os
import boto3

# Own imports
from common.logger import custom_logger


logger = custom_logger()
s3_client = boto3.client("s3")


def upload_pdf_to_s3(bucket_name, file_path, object_name=None, expiration=600) -> str:
    """
    Uploads a PDF to an S3 bucket and generates a temporary public URL.

    :param bucket_name: The name of the S3 bucket.
    :param file_path: Path to the PDF file to upload.
    :param object_name: The S3 object name. If None, file_path's basename is used.
    :param expiration: Time in seconds for the pre-signed URL to remain valid.
    :return: The response for the s3 upload object action.
    """
    try:

        # If no object name is provided, use the file name
        if object_name is None:
            object_name = os.path.basename(file_path)

        # Upload the file
        response = s3_client.upload_file(file_path, bucket_name, object_name)
        logger.info(f"File uploaded successfully to {bucket_name}/{object_name}")
        logger.debug(f"Response for s3 client upload: {response}")
        return response

    except FileNotFoundError:
        return "Error: The specified file was not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"


# Local tests/validations
if __name__ == "__main__":

    # Example usage
    bucket_name = "san99tiago-manual-tests-430118815432"
    file_path = "./temp/certificate.pdf"

    # Call the function to upload the file and generate the URL
    response = upload_pdf_to_s3(bucket_name, file_path)
    print(response)

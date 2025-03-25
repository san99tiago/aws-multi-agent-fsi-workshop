# Built-in imports
from uuid import uuid4
import re
import os

# External imports
from fastapi import APIRouter, Request

# Own imports
from common.logger import custom_logger
from common.helpers.s3_url_helper import generate_presigned_url
from api.v1.services.bedrock_agent import call_bedrock_agent
from api.v1.services.save_message import save_message


router = APIRouter()
logger = custom_logger()


BUCKET_NAME = os.environ["BUCKET_NAME"]  # Mandatory to pass S3 Bucket name as env var


@router.get("/invokemodel", tags=["Chatbot"])
async def get_chatbot_invokemodel():
    return {"status": "ok", "message": "endpoint ready"}


@router.post("/invokemodel", tags=["Chatbot"])
async def post_chatbot_invokemodel(
    request: Request,  # Only for initial debugging purposes
    input_body: dict,
):
    try:
        correlation_id = str(uuid4())
        logger.append_keys(correlation_id=correlation_id)
        logger.info(input_body, message_details="Received body in post_invokemodel()")

        # Validate input message
        message = input_body.get("input")
        from_number = input_body.get("from_number")
        if not message:
            logger.warning("Input message <input> is required")
            result = {
                "type": "text",
                "success": "true",
                "response": "Please provide input.",
            }
            return result

        # Save input message to storage layer
        save_message_result_input = save_message(
            from_number=from_number,
            message=message,
            message_io_type="input",
            correlation_id=correlation_id,
        )
        logger.debug(save_message_result_input)

        # Process the message via invoking Bedrock Agent!!!
        first_name = "Amigo"
        text = (
            f"<REQUEST>"
            f"input: {message}\n"
            f"from_number: {from_number}\n"
            f"first_name: {first_name}\n"
            f"Answer in same language as input. Use UTF-8 format."
            f"</REQUEST>"
        )

        # Execute Bedrock Agent SDK/API Call
        logger.info(f"Input message to LLM is: {str(text)}")
        response_message = call_bedrock_agent(str(text), from_number)
        logger.info(f"Output message from LLM: {response_message}")

        # Extract the document ID (will be formatted between hashtags)
        match = re.search(r"##([\w\d]+)##", response_message)
        document_id = match.group(1) if match else ""
        logger.info(f"Document ID: {document_id}")

        # For responses that are images of pdfs, intercept the response
        # ... and send back only the presigned URL
        if document_id.startswith("IMG"):
            logger.debug("Document ID corresponds to an image")

            # Generate presigned-url for the document
            presigned_url = generate_presigned_url(
                bucket_name=BUCKET_NAME,
                object_name=f"images/{document_id}/bank_receipt.png",
            )

            result = {
                "type": "image",
                "success": "true",
                "response": presigned_url,
            }
            return result
        elif document_id.startswith("PDF"):
            # Generate presigned-url for the document
            presigned_url = generate_presigned_url(
                bucket_name=BUCKET_NAME,
                object_name=f"certificates/{document_id}/bank_certificate.pdf",
            )

            result = {
                "type": "pdf",
                "success": "true",
                "response": presigned_url,
            }
            return result

        # Save output message to storage layer
        save_message_result_output = save_message(
            from_number=from_number,
            message=response_message,
            message_io_type="output",
            correlation_id=correlation_id,
        )
        logger.debug(save_message_result_output)

        result = {
            "type": "text",
            "success": "true",
            "response": response_message,
        }
        logger.info("Finished post_invokemodel() successfully")

        return result

    except Exception as e:
        logger.error(f"Error in post_invokemodel(): {e}")
        raise e

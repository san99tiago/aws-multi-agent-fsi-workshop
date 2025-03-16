###############################################################################
# Entrypoint for the Chatbot API Endpoint
###############################################################################

# Built-in imports
import os

# External imports
from mangum import Mangum
from fastapi import FastAPI

# Own imports
from api.v1.routers import invokemodel

# Environment used to dynamically load the FastAPI docs with stages
ENVIRONMENT = os.environ.get("ENVIRONMENT")
API_PREFIX = "/api/v1"


app = FastAPI(
    title="Chatbot API",
    description="Custom built API to interact with the Chatbot",
    version="v1",
    root_path=f"/{ENVIRONMENT}" if ENVIRONMENT else None,
    docs_url="/api/v1/docs",
    openapi_url="/api/v1/docs/openapi.json",
)


app.include_router(invokemodel.router, prefix=API_PREFIX)

# This is the Lambda Function's entrypoint (handler)
handler = Mangum(app)

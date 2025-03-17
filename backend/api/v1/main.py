###############################################################################
# Entrypoint for the Chatbot API Endpoint
###############################################################################

# Built-in imports
import os

# External imports
from mangum import Mangum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# Required to allow CORS for the API (for local development and external frontends)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(invokemodel.router, prefix=API_PREFIX)

# This is the Lambda Function's entrypoint (handler)
handler = Mangum(app)

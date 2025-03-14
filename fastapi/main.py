# fast_api_app/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.staticfiles import StaticFiles
import os
import django
import logging

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Import routers
from fast_api_app.routers import institutions, datasets, data_files

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Data Platform API",
    description="API for managing institutional datasets and data files",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(institutions.router, prefix="/api/v1")
app.include_router(datasets.router, prefix="/api/v1")
app.include_router(data_files.router, prefix="/api/v1")
#
# # Mount static_files files
# app.mount("/static_files", StaticFiles(directory="static_files"), name="static_files")
#
#
# @app.get("/", include_in_schema=False)
# async def root():
#     """
#     Root endpoint redirects to API documentation
#     """
#     return {"message": "Welcome to Data Platform API", "docs_url": "/docs"}
#
#
# @app.get("/health", include_in_schema=False)
# async def health_check():
#     """
#     Health check endpoint for monitoring
#     """
#     return {"status": "healthy"}
#
#
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run("fast_api_app.main:app", host="0.0.0.0", port=8000, reload=True)
#
# # fast_api_app/dependencies.py
# from fastapi import Header, HTTPException, Depends
# from typing import Optional
# import os
# import logging
#
# logger = logging.getLogger(__name__)
#
#
# # This file will contain shared dependencies for FastAPI routes
# # For example, authentication, database sessions, etc.
#
# async def get_api_key(x_api_key: Optional[str] = Header(None)):
#     """
#     Dependency for API key authentication
#     """
#     if not x_api_key:
#         raise HTTPException(status_code=401, detail="API Key is missing")
#
#     expected_api_key = os.environ.get("API_KEY")
#     if not expected_api_key:
#         logger.warning("API_KEY environment variable not set!")
#         # In development, allow any key for ease of testing
#         return x_api_key
#
#     if x_api_key != expected_api_key:
#         raise HTTPException(status_code=401, detail="Invalid API Key")
#
#     return x_api_key
#
# # Add more shared dependencies as needed
#
#
# ///////////////////////////

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add the project root to the path so that we can import Django models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django
import django
django.setup()

from fast_api_app.routers import institutions, datasets, data_files

app = FastAPI(
    title="Data Platform API",
    description="API for data processing and management",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(institutions.router, prefix="/api/v1", tags=["institutions"])
app.include_router(datasets.router, prefix="/api/v1", tags=["datasets"])
app.include_router(data_files.router, prefix="/api/v1", tags=["data_files"])


@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Data Platform API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
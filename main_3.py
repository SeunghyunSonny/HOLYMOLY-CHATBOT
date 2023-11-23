import logging
import warnings
from fastapi import FastAPI, Request, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
#from utils import ConnectionManager

from restful_routes import restful_router

#from websocket_routes import websocket_router
"""
# Suppress specific deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="whisper")

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
"""
# Create FastAPI app instance
app = FastAPI()

# Root route
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Include RESTful and WebSocket routers
app.include_router(restful_router)
#app.include_router(websocket_router)

# Global exception handler
# @app.exception_handler(Exception)
# async def global_exception_handler(request: Request, exc: Exception):
#     logger.error(f"Unhandled exception: {exc}")
#     return JSONResponse(
#         status_code=500,
#         content={"message": "Internal server error"}
#     )
#ConnectionManager.initialize()

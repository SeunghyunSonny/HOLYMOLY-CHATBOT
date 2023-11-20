# main.py
import os
import datetime
import uuid
import asyncio

from fastapi import Depends, HTTPException, Request, \
    status as http_status, UploadFile, File, Form, FastAPI
from database.connection import get_db
from chatbot_logic.interaction import Interaction
from chatbot_logic.feedback import Feedback,FeedbackRequest
from chatbot_logic.memory import Memory, EditMemoryRequest
from chatbot import get_bot_response
from audio.text_to_speech import get_text_to_speech
from audio.speech_to_text import get_speech_to_text
from fastapi import FastAPI
from restful_routes import router as restful_router  # Ensure correct import
from websocket_routes import router as websocket_router  # Ensure correct import
import warnings

# Suppress deprecation warnings
warnings.filterwarnings("ignore", module="whisper")

app = FastAPI()

# Include routers for RESTful and WebSocket endpoints
app.include_router(restful_router)
app.include_router(websocket_router)

# Initialization functions for text-to-speech and speech-to-text
# Ensure these functions are defined and imported correctly
get_text_to_speech()
get_speech_to_text()


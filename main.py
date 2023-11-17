import os
import warnings

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

from audio.speech_to_text import get_speech_to_text
from audio.text_to_speech import get_text_to_speech
from character_catalog.catalog_manager import CatalogManager
from memory.memory_manager import MemoryManager
from restful_routes import router as restful_router
from utils import ConnectionManager
from websocket_routes import router as websocket_router

load_dotenv()

app = FastAPI()

app.include_router(restful_router)
app.include_router(websocket_router)

# initializations
overwrite_chroma = os.getenv("OVERWRITE_CHROMA", 'True').lower() in ('true', '1')
CatalogManager.initialize(overwrite=overwrite_chroma)
ConnectionManager.initialize()
MemoryManager.initialize()
get_text_to_speech()
get_speech_to_text()

# suppress deprecation warnings
warnings.filterwarnings("ignore", module="whisper")

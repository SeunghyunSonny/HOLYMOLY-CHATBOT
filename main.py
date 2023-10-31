# 필요한 라이브러리와 모듈을 임포트합니다.
import os
import warnings

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

from realtime_ai_character.audio.speech_to_text import get_speech_to_text
from realtime_ai_character.audio.text_to_speech import get_text_to_speech
from realtime_ai_character.character_catalog.catalog_manager import CatalogManager
from realtime_ai_character.memory.memory_manager import MemoryManager
from realtime_ai_character.restful_routes import router as restful_router
from realtime_ai_character.utils import ConnectionManager
from realtime_ai_character.websocket_routes import router as websocket_router

# 환경 변수를 로드합니다.
load_dotenv()

# FastAPI 앱 인스턴스를 생성합니다.
app = FastAPI()

# CORS 미들웨어를 추가합니다.
app.add_middleware(
    CORSMiddleware,
    # 프로덕션에 배포할 경우 도메인을 변경하세요.
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터를 앱에 포함시킵니다.
app.include_router(restful_router)
app.include_router(websocket_router)

# 웹 빌드 경로를 설정합니다.
web_build_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                              '..', 'client', 'web', 'build')

# 웹 빌드 경로가 존재하는 경우
if os.path.exists(web_build_path):
    app.mount("/static/", 
              StaticFiles(directory=os.path.join(web_build_path, 'static')), 
              name="static")

    # 메인 페이지를 반환합니다.
    @app.get("/", response_class=FileResponse)
    async def read_index():
        return FileResponse(os.path.join(web_build_path, 'index.html'))
                            
    # 정적 파일을 반환합니다.
    @app.get("/{catchall:path}", response_class=FileResponse)
    def read_static(request: Request):
        path = request.path_params["catchall"]
        file = os.path.join(web_build_path, path)

        if os.path.exists(file):
            return FileResponse(file)

        return RedirectResponse("/")
else:
    # 웹 앱이 빌드되지 않았다면 사용자에게 빌드하도록 안내합니다.
    static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
    app.mount("/static/", StaticFiles(directory=static_path), name="static")

    @app.get("/", response_class=FileResponse)
    async def read_index():
        return FileResponse(os.path.join(static_path, '404.html'))

# 초기화 작업들을 수행합니다.
overwrite_chroma = os.getenv("OVERWRITE_CHROMA", 'True').lower() in ('true', '1')
CatalogManager.initialize(overwrite=overwrite_chroma)
ConnectionManager.initialize()
MemoryManager.initialize()
get_text_to_speech()
get_speech_to_text()

# deprecated 경고 메시지를 무시합니다.
warnings.filterwarnings("ignore", module="whisper")

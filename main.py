from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Union
from llm import LocalLlm, Character  # 적절한 모듈 경로로 변경하세요
import asyncio

app = FastAPI()

# CORS 미들웨어 설정
# 모든 출처를 허용하는 경우
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메소드 허용
    allow_headers=["*"],  # 모든 HTTP 헤더 허용
)

@app.get("/stat")
async def root():
    return {"message": "Server is running"}

@app.websocket("/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    llm = LocalLlm()  # LocalLlm 인스턴스 생성
    history = []  # 대화 기록을 저장하는 리스트

    # 캐릭터 객체 생성
    character = None

    async def callback_function(message):
        # 콜백 함수 구현 (예시)
        pass

    try:
        while True:
            user_input = await websocket.receive_text()
            user_input_template = f"User said: {user_input}"  # 사용자 입력 템플릿

            # LocalLlm의 achat 메소드를 사용하여 대화 생성
            response = await llm.achat(
                history,
                user_input,
                user_input_template,
                callback=callback_function,  # 콜백 함수 사용
                character=character
            )

            # 응답을 클라이언트에게 보냄
            await websocket.send_text(response)

    except WebSocketDisconnect:
        print("WebSocket connection disconnected")
    except Exception as e:
        print(f"WebSocket connection closed with exception: {e}")
        await websocket.close(code=1000)

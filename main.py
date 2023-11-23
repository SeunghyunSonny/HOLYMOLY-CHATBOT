from fastapi import FastAPI, WebSocket
from typing import List, Union
from llm import LocalLlm, Character, BaseMessage, HumanMessage  # 적절한 모듈 경로로 변경하세요
import asyncio

app = FastAPI()

@app.websocket("/chat")
async def chat_endpoint(websocket: WebSocket):
    await websocket.accept()
    llm = LocalLlm()  # LocalLlm 인스턴스 생성
    history = []  # 대화 기록을 저장하는 리스트

    try:
        while True:
            user_input = await websocket.receive_text()
            user_input_template = "{query}"  # 사용자 입력 템플릿 (필요에 따라 수정)

            # 캐릭터 객체 생성 (가정)
            character = Character(name="Chatbot", desc="AI Chatbot")

            # LocalLlm의 achat 메소드를 사용하여 대화 생성
            response = await llm.achat(
                history,
                user_input,
                user_input_template,
                callback=None,  # 적절한 콜백 함수로 대체
                character=character
            )

            # 응답을 클라이언트에게 보냄
            await websocket.send_text(response)

    except Exception as e:
        await websocket.close(code=1000)
        print(f"WebSocket connection closed with exception: {e}")
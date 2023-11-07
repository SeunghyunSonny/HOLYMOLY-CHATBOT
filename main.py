# main.py
from fastapi import FastAPI
from models import ChatRequest, ChatResponse
from chatbot import get_bot_response
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
from requests import Session
from sqlalchemy import func





app = FastAPI()

MAX_FILE_UPLOADS = 5



@app.get("/chat/", response_model=ChatResponse)
async def chat(chat_request: ChatRequest):
    reply = get_bot_response(chat_request.message)
    return ChatResponse(reply=reply)

@app.get("/status")
async def status():
    return {"status": "ok", "message": "RealChar is running smoothly!"}


@app.get("/video")
async  def videoworks():
    def get_video_url(user):
        user_path = 'https://storage.googleapis.com/assistly'#(videopath준비)




@app.get("/characters")
async def characters(user=Depends()):
    def get_image_url(character):
        gcs_path = 'https://storage.googleapis.com/assistly'#aws에 스토리지 만들기
        if character.data and 'avatar_filename' in character.data:
            return f'{gcs_path}/{character.data["avatar_filename"]}'
        else:
            return f'{gcs_path}/static/realchar/{character.character_id}.jpg'
    uid = user['uid'] if user else None
    from character_catalog.catalog_manager import CatalogManager
    catalog: CatalogManager = CatalogManager.get_instance()
    return [{
        "character_id": character.character_id,
        "name": character.name,
        "source": character.source,
        "voice_id": character.voice_id,
        "author_name": character.author_name,
        "image_url": get_image_url(character),
        "avatar_id": character.avatar_id,
        "tts": character.tts,
        'is_author': character.author_id == uid,
    } for character in catalog.characters.values()
            if character.author_id == uid or character.visibility == 'public']


@app.get("/configs")
async def configs():
    return {
        'llms': ["beomi/llama-2-ko-7b"],
    }

@app.get("/session_history")
async def get_session_history(session_id: str, db: Session = Depends(get_db)):
    # Read session history from the database.
    interactions = await asyncio.to_thread(
        db.query(Interaction).filter(Interaction.session_id == session_id).all)
    # return interactions in json format
    interactions_json = [Interaction.to_dict() for Interaction in interactions]
    return interactions_json

@app.post("/feedback")
async def post_feedback(feedback_request: FeedbackRequest, db: Session = Depends(get_db)):
    feedback = Feedback(**feedback_request.dict())
    feedback.created_at = datetime.datetime.now()
    await asyncio.to_thread(feedback.save, db)



@app.get("/conversations", response_model=list[dict])
async def get_recent_conversations(user = Depends(), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
    user_id = user['uid']
    stmt = (
        db.query(
            Interaction.session_id,
            Interaction.client_message_unicode,
            Interaction.timestamp,
            func.row_number().over(
                partition_by=Interaction.session_id,
                order_by=Interaction.timestamp.desc()).label("rn")).filter(
                    Interaction.user_id == user_id).subquery()
    )

    results = (
        await asyncio.to_thread(db.query(stmt.c.session_id, stmt.c.client_message_unicode)
        .filter(stmt.c.rn == 1)
        .order_by(stmt.c.timestamp.desc())
        .all)
    )

    # Format the results to the desired output
    return [{
        "session_id": r[0],
        "client_message_unicode": r[1],
        "timestamp": r[2]
    } for r in results]


@app.get("/memory", response_model=list[dict])
async def get_memory(user = Depends(), db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )

    memories = await asyncio.to_thread(db.query(Memory).filter(Memory.user_id == user['uid']).all)

    return [{
        "memory_id": memory.memory_id,
        "source_session_id": memory.source_session_id,
        "content": memory.content,
        "created_at": memory.created_at,
        "updated_at": memory.updated_at,
    } for memory in memories]


@app.post("/delete_memory")
async def delete_memory(memory_id: str, user = Depends(),
                        db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
        )

    memories = await asyncio.to_thread(db.query(Memory).filter(Memory.memory_id == memory_id).all)
    if len(memories) == 0:
        raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f'Memory {memory_id} not found',
            )
    if memories[0].user_id != user['uid']:
        raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
        )

    db.delete(memories[0])
    db.commit()


@app.post("/edit_memory")
async def edit_memory(edit_memory_request: EditMemoryRequest, user = Depends(),
                      db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
        )
    memory_id = edit_memory_request.memory_id
    memories = await asyncio.to_thread(db.query(Memory).filter(Memory.memory_id == memory_id).all)
    if len(memories) == 0:
        raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail=f'Memory {memory_id} not found',
            )
    memory = memories[0]
    if memory.user_id != user['uid']:
        raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
        )
    memory.source_session_id = edit_memory_request.source_session_id
    memory.content = edit_memory_request.content
    memory.updated_at = datetime.datetime.now()

    db.merge(memory)
    db.commit()




import httpx
from memory import Memory
from fastapi import Header,APIRouter, Depends, HTTPException, Request, \
    status as http_status, UploadFile, File, Form
from sqlalchemy import func
import os
import datetime
import uuid
import asyncio
import boto3
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, Header
from sqlalchemy.orm import Session
from database.connection import get_db
from audio.text_to_speech import get_text_to_speech
from chatbot_logic.interaction import Interaction

restful_router = APIRouter()
MAX_FILE_UPLOADS = 5

# 토큰 헤더 검증
async def get_token_header(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

@restful_router.get("/status")
async def status():
    return {"status": "ok"}


"""
@restful_router.get("/characters")
async def characters(user=Depends(get_token_header)):
    def get_image_url(character):
        gcs_path = 'https://storage.googleapis.com/assistly'
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
    # 캐릭터 목록 조회 및 반환 로직
"""
@restful_router.post("/generate_audio")
async def generate_audio(text: str, tts: str = None, user=Depends(get_token_header)):
    if not isinstance(text, str) or text == '':
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail='Text is empty',
        )
    try:
        tts_service = get_text_to_speech(tts)
    except NotImplementedError:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail='Text to speech engine not found',
        )

    audio_bytes = await tts_service.generate_audio(text)

    # AWS S3 설정
    s3_client = boto3.client('s3')
    bucket_name = os.environ.get('AWS_S3_BUCKET_NAME')
    if not bucket_name:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='AWS_S3_BUCKET_NAME is not set',
        )

    # 파일 이름 생성
    file_extension = '.webm' if tts == 'UNREAL_SPEECH' else '.mp3'
    new_filename = (
        f"user_upload/{user['uid']}/"
        f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-"
        f"{uuid.uuid4()}{file_extension}"
    )

    # AWS S3에 파일 저장
    try:
        s3_client.put_object(
            Bucket=bucket_name,
            Key=new_filename,
            Body=audio_bytes,
            ContentType='audio/mpeg'
        )
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    return {
        "filename": new_filename,
        "content-type": "audio/mpeg"
    }
    # 텍스트를 오디오로 변환하고 AWS S3에 저장하는 로직

@restful_router.get("/clone_voice")
async def clone_voice(files: list[UploadFile] = Form(...), user=Depends(get_token_header)):
    if len(files) > MAX_FILE_UPLOADS:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f'Number of files exceeds the limit ({MAX_FILE_UPLOADS})',
        )

    s3_client = boto3.client('s3')
    bucket_name = os.environ.get('AWS_S3_BUCKET_NAME')
    if not bucket_name:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='AWS_S3_BUCKET_NAME is not set',
        )

    voice_request_id = str(uuid.uuid4().hex)
    uploaded_files = []

    for file in files:
        file_extension = os.path.splitext(file.filename)[1]
        new_filename = (
            f"user_upload/{user['uid']}/{voice_request_id}/"
            f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-"
            f"{uuid.uuid4()}{file_extension}"
        )

        contents = await file.read()

        # AWS S3에 파일 저장
        s3_client.put_object(
            Bucket=bucket_name,
            Key=new_filename,
            Body=contents
        )
        uploaded_files.append((file.filename, (new_filename, contents, 'application/octet-stream')))

    # API 요청을 위한 데이터 구성
    data = {
        "name": user['uid'] + "_" + voice_request_id,
    }

    headers = {
        "xi-api-key": os.getenv("ELEVEN_LABS_API_KEY"),
    }

    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.elevenlabs.io/v1/voices/add",
                                    headers=headers, data=data, files=uploaded_files)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
    # 오디오 파일을 받아 AWS S3에 저장하는 로직
"""
@restful_router.get("/conversations")
async def get_recent_conversations(user=Depends(get_token_header), db: Session = Depends(get_db)):
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

    # 최근 대화 목록을 조회하여 반환하는 로직
"""
"""
@restful_router.get("/memory")
async def get_memory(user=Depends(get_token_header), db: Session = Depends(get_db)):
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
    # 메모리 정보 조회 및 반환 로직
"""

"""
@restful_router.get("/delete_memory")
async def delete_memory(memory_id: str, user=Depends(get_token_header), db: Session = Depends(get_db)):
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
    await asyncio.to_thread(db.commit)
"""
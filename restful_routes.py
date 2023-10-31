import os
import datetime
import uuid
import asyncio
import httpx

from fastapi import APIRouter, Depends, HTTPException, Request, \
    status as http_status, UploadFile, File, Form
from google.cloud import storage
from realtime_ai_character.audio.text_to_speech import get_text_to_speech
from realtime_ai_character.database.connection import get_db
from realtime_ai_character.models.interaction import Interaction
from realtime_ai_character.models.feedback import Feedback,FeedbackRequest
from realtime_ai_character.models.character import GeneratePromptRequest
from realtime_ai_character.models.memory import Memory, EditMemoryRequest
from realtime_ai_character.models.quivr_info import QuivrInfo, UpdateQuivrInfoRequest
from realtime_ai_character.llm.system_prompt_generator import generate_system_prompt
from requests import Session
from sqlalchemy import func

from fastapi import FastAPI
from uvicorn import run

# 여기에 위에서 제공한 모든 import 문장을 추가합니다.

app = FastAPI()

# APIRouter 인스턴스를 FastAPI 애플리케이션에 포함시킵니다.


router = APIRouter()

MAX_FILE_UPLOADS = 5

@router.get("/status")
async def status():
    return {"status": "ok", "message": "RealChar is running smoothly!"}


@router.get("/video")
async  def videoworks():
    def get_video_url(user):
        user_path = 'https://storage.googleapis.com/assistly'#(videopath준비)



@router.get("/status")
async def status():
    return {"status": "ok", "message": "RealChar is running smoothly!"}


@router.get("/characters")
async def characters(user=Depends()):
    def get_image_url(character):
        gcs_path = 'https://storage.googleapis.com/assistly'
        if character.data and 'avatar_filename' in character.data:
            return f'{gcs_path}/{character.data["avatar_filename"]}'
        else:
            return f'{gcs_path}/static/realchar/{character.character_id}.jpg'
    uid = user['uid'] if user else None
    from realtime_ai_character.character_catalog.catalog_manager import CatalogManager
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


@router.get("/configs")
async def configs():
    return {
        'llms': ['gpt-3.5-turbo-16k', 'meta-llama/Llama-2-7b-chat-hf'],
    }

@router.get("/session_history")
async def get_session_history(session_id: str, db: Session = Depends(get_db)):
    # Read session history from the database.
    interactions = await asyncio.to_thread(
        db.query(Interaction).filter(Interaction.session_id == session_id).all)
    # return interactions in json format
    interactions_json = [interaction.to_dict() for interaction in interactions]
    return interactions_json

@router.post("/feedback")
async def post_feedback(feedback_request: FeedbackRequest, db: Session = Depends(get_db)):
    feedback = Feedback(**feedback_request.dict())
    feedback.created_at = datetime.datetime.now()
    await asyncio.to_thread(feedback.save, db)


@router.post("/generate_audio")
async def generate_audio(text: str, tts: str = None, user = Depends()):
    if not isinstance(text, str) or text == '':
        raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail='Text is empty',
            )
    if not user:
        raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
    try:
        tts_service = get_text_to_speech(tts)
    except NotImplementedError:
        raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail='Text to speech engine not found',
            )
    audio_bytes = await tts_service.generate_audio(text)
    # save audio to a file on GCS
    storage_client = storage.Client()
    bucket_name = os.environ.get('GCP_STORAGE_BUCKET_NAME')
    if not bucket_name:
        raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='GCP_STORAGE_BUCKET_NAME is not set',
            )
    bucket = storage_client.bucket(bucket_name)

    # Create a new filename with a timestamp and a random uuid to avoid duplicate filenames
    file_extension = '.webm' if tts == 'UNREAL_SPEECH' else '.mp3'
    new_filename = (
        f"user_upload/{user['uid']}/"
        f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-"
        f"{uuid.uuid4()}{file_extension}"
    )

    blob = bucket.blob(new_filename)

    await asyncio.to_thread(blob.upload_from_string, audio_bytes)

    return {
        "filename": new_filename,
        "content-type": "audio/mpeg"
    }


@router.get("/quivr_info")
async def quivr_info(user = Depends(),
                     db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
        )

    quivr_info = await asyncio.to_thread(
        db.query(QuivrInfo).filter(QuivrInfo.user_id == user['uid']).first)

    if not quivr_info:
        return {"success": False}

    return {"success": True, "api_key": quivr_info.quivr_api_key,
            "brain_id": quivr_info.quivr_brain_id}

@router.post("/quivr_info")
async def quivr_info_update(update_quivr_info_request: UpdateQuivrInfoRequest,
                     user = Depends(),
                     db: Session = Depends(get_db)):
    if not user:
        raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
        )

    api_key = update_quivr_info_request.quivr_api_key

    if not update_quivr_info_request.quivr_brain_id or \
        update_quivr_info_request.quivr_brain_id == "":
        # Get default brain ID if not provided
        url = "https://api.quivr.app/brains/default/"
        headers = {"Authorization": f"Bearer {api_key}"}

        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers)
                response.raise_for_status()
            except httpx.HTTPStatusError as exc:
                detail = f"Quivr returns an error status code: {exc.response.status_code}"
                raise HTTPException(status_code=exc.response.status_code, detail=detail)
            except httpx.RequestError:
                raise HTTPException(status_code=500, detail="Failed to get data from Quivr.")

        brain_id = response.json()["id"]
        brain_name = response.json()["name"]
    else:
        brain_id = update_quivr_info_request.quivr_brain_id

    # Verify API key and brain ID
    url = f"https://api.quivr.app/brains/{brain_id}/"
    headers = {"Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            brain_name = response.json()["name"]
        except httpx.HTTPStatusError as exc:
            detail = f"Quivr returns an error status code: {exc.response.status_code}"
            raise HTTPException(status_code=exc.response.status_code, detail=detail)
        except httpx.RequestError:
            raise HTTPException(status_code=500, detail="Failed to get data from Quivr.")

    # Save to database
    quivr_info = QuivrInfo(user_id=user['uid'],
                           quivr_api_key=api_key,
                           quivr_brain_id=brain_id)

    await asyncio.to_thread(quivr_info.save, db)

    return {"success": True, "brain_id": brain_id, "brain_name": brain_name}


@router.post("/clone_voice")
async def clone_voice(
    files: list[UploadFile] = Form(...),
    user = Depends()):
    if not user:
        raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
        )
    if len(files) > MAX_FILE_UPLOADS:
        raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail=f'Number of files exceeds the limit ({MAX_FILE_UPLOADS})',
            )

    storage_client = storage.Client()
    bucket_name = os.environ.get('GCP_STORAGE_BUCKET_NAME')
    if not bucket_name:
        raise HTTPException(
                status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail='GCP_STORAGE_BUCKET_NAME is not set',
            )

    bucket = storage_client.bucket(bucket_name)
    voice_request_id = str(uuid.uuid4().hex)

    for file in files:
        # Create a new filename with a timestamp and a random uuid to avoid duplicate filenames
        file_extension = os.path.splitext(file.filename)[1]
        new_filename = (
            f"user_upload/{user['uid']}/{voice_request_id}/"
            f"{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')}-"
            f"{uuid.uuid4()}{file_extension}"
        )

        blob = bucket.blob(new_filename)

        contents = await file.read()

        await asyncio.to_thread(blob.upload_from_string, contents)

    # Construct the data for the API request
    # TODO: support more voice cloning services.
    data = {
        "name": user['uid'] + "_" + voice_request_id,
    }

    files = [("files", (file.filename, file.file)) for file in files]

    headers = {
        "xi-api-key": os.getenv("ELEVEN_LABS_API_KEY"),
    }

    async with httpx.AsyncClient() as client:
        response = await client.post("https://api.elevenlabs.io/v1/voices/add",
                                     headers=headers, data=data, files=files)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()
#모델 삽입해야하지

@router.post("/system_prompt")
async def system_prompt(request: GeneratePromptRequest, user = Depends()):
    """Generate System Prompt according to name and background."""
    name = request.name
    background = request.background
    if not isinstance(name, str) or name == '':
        raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail='Name is empty',
            )
    if not user:
        raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail='Invalid authentication credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
    return {
        'system_prompt': await generate_system_prompt(name, background)
    }


@router.get("/conversations", response_model=list[dict])
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


@router.get("/memory", response_model=list[dict])
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


@router.post("/delete_memory")
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


@router.post("/edit_memory")
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

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    # Uvicorn을 사용하여 FastAPI 애플리케이션을 실행합니다.
    run(app, host="0.0.0.0", port=8000)

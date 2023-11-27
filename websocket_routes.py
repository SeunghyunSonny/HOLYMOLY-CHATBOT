import asyncio
import os
import uuid
from dataclasses import dataclass
from fastapi import APIRouter, Depends, HTTPException, Path, WebSocket, WebSocketDisconnect, Query
from requests import Session
from audio.speech_to_text import (SpeechToText,
                                  get_speech_to_text)
from audio.text_to_speech import (TextToSpeech,
                                  get_text_to_speech)
from character_catalog.catalog_manager import (
    CatalogManager, get_catalog_manager)

from database.connection import get_db
from llm import LocalLlm, LLM
from models import AsyncCallbackAudioHandler, AsyncCallbackTextHandler
from logger import get_logger
from chatbot_logic.interaction import Interaction

from utils import (ConversationHistory, build_history,
                   get_connection_manager, get_timer)

logger = get_logger(__name__)

websocket_router = APIRouter()

manager = get_connection_manager()

timer = get_timer()

GREETING_TXT_MAP = {
    "en-US": "Hi, my friend, what brings you here today?",
    'ko-KR': "안녕, 내 친구, 오늘 여기 왜 왔어?"
}


@dataclass
class SessionAuthResult:
    is_existing_session: bool
    is_authenticated_user: bool


# WebSocket 엔드포인트 함수는 클래스 밖에 정의
async def websocket_endpoint(websocket: WebSocket,
                             session_id: str = Path(...),
                             api_key: str = Query(None),
                             llm_model: str = Query(default='LocalLlm'),
                             language: str = Query(default='en-US'),
                             token: str = Query(None),
                             character_id: str = Query(None),
                             platform: str = Query(None),
                             db: Session = Depends(get_db),
                             catalog_manager=Depends(get_catalog_manager),
                             speech_to_text=Depends(get_speech_to_text),
                             default_text_to_speech=Depends(get_text_to_speech)):
    user_id = str(session_id)

    # 초기화 로직
    llm = LLM(model=LocalLlm)
    await manager.connect(websocket)

    try:
        main_task = asyncio.create_task(
            handle_receive(websocket, session_id, user_id, db, llm, catalog_manager,
                           character_id, platform, speech_to_text, default_text_to_speech, language))
        await asyncio.gather(main_task)

    except WebSocketDisconnect:
        logger.error(f"WebSocket disconnected for User #{user_id}")
        await manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")


async def handle_receive(websocket: WebSocket, session_id: str, user_id: str, db: Session,
                         llm: LocalLlm, catalog_manager: CatalogManager,
                         character_id: str, platform: str,
                         speech_to_text: SpeechToText,
                         default_text_to_speech: TextToSpeech,
                         language: str, load_from_existing_session: bool = False):
    try:
        conversation_history = ConversationHistory()
        if load_from_existing_session:
            logger.info(f"User #{user_id} is loading from existing session {session_id}")
        await asyncio.to_thread(conversation_history.load_from_db, session_id=session_id, db=db)
        logger.info(f'User #{user_id}:{platform} connected to server with 'f"session_id {session_id}")
        character = None
        if character_id:
            character = catalog_manager.get_character(character_id)
        character_list = [(character.name, character.character_id)
                          for character in catalog_manager.characters.values()
                          if character.source != 'community']
        character_name_list, character_id_list = zip(*character_list)

        text_to_speech, token_buffer, tts_event, user_input_template = await checking_works(character,
                                                                                            conversation_history,
                                                                                            default_text_to_speech,
                                                                                            language, user_id,
                                                                                            websocket)

        async def on_new_token(token):
            return await manager.send_message(message=token, websocket=websocket)

        async def stop_audio():
            if tts_task and not tts_task.done():
                tts_event.set()
                tts_task.cancel()
            if previous_transcript:
                conversation_history.user.append(previous_transcript)
                conversation_history.ai.append(' '.join(token_buffer))
                token_buffer.clear()
            try:
                await tts_task
            except asyncio.CancelledError:
                pass
            tts_event.clear()

        speech_recognition_interim = False
        current_speech = ''
        while True:
            data = await websocket.receive()
            binary_data, msg_data = await decode(character, conversation_history, data, llm, on_new_token, stop_audio,
                                                 text_to_speech, tts_event, websocket)
            if binary_data is None and msg_data is None:
                logger.error("decode fail" + str(data))
                continue

            # 1.음성인식을 시작한다.
            if msg_data.startswith('[&Speech]'):
                speech_recognition_interim = True
                continue

            # 2. 대화가 시작되면 말을 모은다
            if msg_data.startswith('[SpeechFinished]'):
                msg_data = current_speech
                logger.info(f"Full transcript: {current_speech}")
                # Stop recognizing next audio as interim.
                speech_recognition_interim = False
                # Filter noises
                if not current_speech:
                    continue

                await manager.send_message(
                    message=f'[+]You said: {current_speech}', websocket=websocket)
                current_speech = ''

            # 3. 메시지를 보낸다.

            message_id = str(uuid.uuid4().hex)[:16]
            response = await llm.achat(
                history=build_history(conversation_history),
                user_input=msg_data,
                user_input_template=user_input_template,
                callback=AsyncCallbackTextHandler(on_new_token,
                                                  token_buffer),
                audioCallback=AsyncCallbackAudioHandler(
                    text_to_speech, websocket, tts_event, character.voice_id),
                character=character,
                metadata={"message_id": message_id})

            # 3. Send response to client
            await manager.send_message(message=f'[end={message_id}]\n',
                                       websocket=websocket)

            # 4. Update conversation history
            conversation_history.user.append(msg_data)
            conversation_history.ai.append(response)
            token_buffer.clear()
            # 5. Persist interaction in the database
            tools = []

            interaction = Interaction(user_id=user_id,
                                      session_id=session_id,
                                      client_message_unicode=msg_data,
                                      server_message_unicode=response,
                                      platform=platform,
                                      action_type='text',
                                      character_id=character_id,
                                      tools=','.join(tools),
                                      language=language,
                                      message_id=message_id,
                                      llm_config=llm.get_config())
            await asyncio.to_thread(interaction.save, db)
        if speech_recognition_interim:
            interim_transcript: str = (
                await asyncio.to_thread(
                    speech_to_text.transcribe,
                    binary_data,
                    platform=platform,
                    prompt=current_speech,
                    suppress_tokens=[0, 11, 13, 30],
                )
            ).strip()
            speech_recognition_interim = False

            # 1. Transcribe audio
        transcript: str = (await asyncio.to_thread(speech_to_text.transcribe,
                                                   binary_data, platform=platform,
                                                   prompt=character.name)).strip()

        # ignore audio that picks up background noise
        # if (not transcript or len(transcript) < 2):
        # continue

        # start counting time for LLM to generate the first token
        timer.start("LLM First Token")

        # 2. Send transcript to client
        await manager.send_message(
            message=f'[+]You said: {transcript}', websocket=websocket)

        # 3. stop the previous audio stream, if new transcript is received
        await stop_audio()
        previous_transcript = transcript

        async def tts_task_done_call_back(response):
            # Send response to client, [=] indicates the response is done
            await manager.send_message(message='[=]',
                                       websocket=websocket)
            # Update conversation history
            conversation_history.user.append(transcript)
            conversation_history.ai.append(response)
            token_buffer.clear()
            # Persist interaction in the database
            tools = []
            interaction = Interaction(user_id=user_id,
                                      session_id=session_id,
                                      client_message_unicode=transcript,
                                      server_message_unicode=response,
                                      platform=platform,
                                      action_type='audio',
                                      character_id=character_id,
                                      tools=','.join(tools),
                                      language=language,
                                      llm_config=llm.get_config())
            await asyncio.to_thread(interaction.save, db)

        # 5. Send message to LLM
        tts_task = asyncio.create_task(
            llm.achat(history=build_history(conversation_history),
                      user_input=transcript,
                      user_input_template=user_input_template,
                      callback=AsyncCallbackTextHandler(
                          on_new_token, token_buffer,
                          tts_task_done_call_back),
                      audioCallback=AsyncCallbackAudioHandler(
                          text_to_speech, websocket, tts_event,
                          character.voice_id),
                      character=character,

                      ))


    except Exception as e: \
        logger.error(f"User #{user_id} encountered an error: {e}")
    await manager.send_message(message=f'[!]Error: {e}', websocket=websocket)
    await asyncio.to_thread(logger.exception(f"An unexpected error occured: {e}"))


async def checking_works(character, conversation_history, default_text_to_speech, language, user_id, websocket):
    if character.tts:
        text_to_speech = get_text_to_speech(character.tts)

    else:
        text_to_speech = default_text_to_speech
    conversation_history.system_prompt = character.llm_system_prompt
    user_input_template = character.llm_user_prompt
    logger.info(
        f"User #{user_id} selected character: {character.name}")
    tts_event = asyncio.Event()
    tts_task = None
    previous_transcript = None
    token_buffer = []
    greeting_text = GREETING_TXT_MAP[language]
    await manager.send_message(message=greeting_text, websocket=websocket)
    tts_task = asyncio.create_task(
        text_to_speech.stream(
            text=greeting_text,
            websocket=websocket,
            tts_event=tts_event,
            voice_id=character.voice_id,
            first_sentence=True,
            language=language
        ))
    # Send end of the greeting so the client knows when to start listening
    await manager.send_message(message='[end]\n', websocket=websocket)
    return text_to_speech, token_buffer, tts_event, user_input_template


async def decode(character, conversation_history, data, llm, on_new_token, stop_audio, text_to_speech, tts_event,
                 websocket):
    if 'text' in data:
        timer.start("LLM First Token")
        msg_data = data['text']

        if msg_data.startswith('[!'):
            command_end = msg_data.find(']')
            command = msg_data[2:command_end]
            command_content = msg_data[command_end + 1:]
            # 여기서 명령을 처리하는 로직 추가
        if msg_data.startswith('[&]'):
            logger.info(f'Intermediate transcript: {msg_data}')
            asyncio.create_task(stop_audio())
            asyncio.create_task(
                llm.achat_utterances(
                    history=build_history(conversation_history),
                    user_input=msg_data,
                    callback=AsyncCallbackTextHandler(on_new_token, []),
                    audioCallback=AsyncCallbackAudioHandler(text_to_speech, websocket, tts_event, character.voice_id)))

        return None, msg_data

    elif 'bytes' in data:
        binary_data = data['bytes']
        # 바이너리 데이터 처리 로직 추가
        return binary_data, None

# models.py
from pydantic import BaseModel
from chatbot_logic.character import Character
from chatbot_logic.feedback import Feedback
from chatbot_logic.interaction import Interaction
from chatbot_logic.memory import Memory

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# callbacks.py
from abc import ABC, abstractmethod




class AsyncCallbackHandler(ABC):
    @abstractmethod
    async def on_chat_model_start(self, *args, **kwargs):
        pass

    @abstractmethod
    async def on_llm_new_token(self, token: str, *args, **kwargs):
        pass

    @abstractmethod
    async def on_llm_end(self, *args, **kwargs):
        pass

class AsyncCallbackTextHandler(AsyncCallbackHandler):
    def __init__(self, on_new_token=None, on_llm_end=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_new_token = on_new_token
        self.on_llm_end = on_llm_end
        self.token_buffer = []

    async def on_chat_model_start(self, *args, **kwargs):
        pass

    async def on_llm_new_token(self, token: str, *args, **kwargs):
        self.token_buffer.append(token)
        if self.on_new_token:
            await self.on_new_token(token)

    async def on_llm_end(self, *args, **kwargs):
        if self.on_llm_end:
            await self.on_llm_end(''.join(self.token_buffer))
        self.token_buffer.clear()


class AsyncCallbackAudioHandler(AsyncCallbackHandler):
    def __init__(self, text_to_speech=None, websocket=None, tts_event=None, voice_id="",
                 language="en-US", *args, **kwargs):
        super().__init__(*args, **kwargs)
        if text_to_speech is None:
            def text_to_speech(token): return print(
                f'New audio token: {token}')
        self.text_to_speech = text_to_speech
        self.websocket = websocket
        self.current_sentence = ""
        self.voice_id = voice_id
        self.language = language
        self.is_reply = False  # the start of the reply. i.e. the substring after '>'
        self.tts_event = tts_event
        # optimization: trade off between latency and quality for the first sentence
        self.is_first_sentence = True

    async def on_chat_model_start(self, *args, **kwargs):
        pass

    async def on_llm_new_token(self, token: str, *args, **kwargs):
        timer.log("LLM First Token", lambda: timer.start("LLM First Sentence"))
        if (
            not self.is_reply and ">" in token
        ):  # small models might not give ">" (e.g. llama2-7b gives ">:" as a token)
            self.is_reply = True
        elif self.is_reply:
            if token not in {'.', '?', '!'}:
                self.current_sentence += token
            else:
                if self.is_first_sentence:
                    timer.log("LLM First Sentence", lambda: timer.start("TTS First Sentence"))
                await self.text_to_speech.stream(
                    self.current_sentence,
                    self.websocket,
                    self.tts_event,
                    self.voice_id,
                    self.is_first_sentence,
                    self.language)
                self.current_sentence = ""
                if self.is_first_sentence:
                    self.is_first_sentence = False
                timer.log("TTS First Sentence")

    async def on_llm_end(self, *args, **kwargs):
        if self.current_sentence != "":
            await self.text_to_speech.stream(
                self.current_sentence,
                self.websocket,
                self.tts_event,
                self.voice_id,
                self.is_first_sentence,
                self.language)





# llm.py
from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    async def achat(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_config(self):
        pass
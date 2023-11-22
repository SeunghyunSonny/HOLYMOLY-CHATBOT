# models.py
from pydantic import BaseModel

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

# llm.py
from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    async def achat(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_config(self):
        pass
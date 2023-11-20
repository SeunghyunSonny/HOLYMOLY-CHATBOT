from abc import ABC, abstractmethod
from utils import timed


class TextToSpeech(ABC):
    @abstractmethod
    @timed
    async def stream(self, *args, **kwargs):
        pass

    async def generate_audio(self,  *args, **kwargs):
        pass

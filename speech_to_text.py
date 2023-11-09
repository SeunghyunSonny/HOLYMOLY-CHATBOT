from abc import ABC, abstractmethod
from utils import timed
import os

def get_speech_to_text() -> SpeechToText:
    use = os.getenv('SPEECH_TO_TEXT_USE', 'LOCAL_WHISPER')
    if use == 'LOCAL_WHISPER':
        from whisper import Whisper
        Whisper.initialize(use='local')
        return Whisper.get_instance()
    elif use == 'OPENAI_WHISPER':
        from whisper import Whisper
        Whisper.initialize(use='api')
        return Whisper.get_instance()
    else:
        raise NotImplementedError(f'Unknown speech to text engine: {use}')


class SpeechToText(ABC):
    @abstractmethod
    @timed
    def transcribe(
        self, audio_bytes, platform="web", prompt="", language="en-US", suppress_tokens=[-1]
    ) -> str:
        # platform: 'web' | 'mobile' | 'terminal'
        pass

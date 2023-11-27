import os

from audio.text_to_speech.base import TextToSpeech


def get_text_to_speech(tts: str = None) -> TextToSpeech:
    if not tts:
        tts = os.getenv('TEXT_TO_SPEECH_USE', 'ELEVEN_LABS')
    if tts == 'ELEVEN_LABS':
        from audio.text_to_speech.elevenlabs import ElevenLabs
        ElevenLabs.initialize()
        return ElevenLabs.get_instance()
    else:
        raise NotImplementedError(f'Unknown text to speech engine: {tts}')

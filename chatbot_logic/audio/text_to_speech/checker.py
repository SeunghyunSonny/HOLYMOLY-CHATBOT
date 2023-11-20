import pytest
from audio.text_to_speech.elevenlabs import ElevenLabs  # your_module을 실제 모듈 이름으로 변경

@pytest.mark.asyncio
async def test_generate_audio():
    eleven_labs = ElevenLabs()
    text = "Hello, this is a test."  # 테스트할 텍스트
    voice_id = "21m00Tcm4TlvDq8ikWAM"  # 사용할 음성 ID
    language = "en-US"  # 사용할 언어

    audio = await eleven_labs.generate_audio(text, voice_id, language)

    assert isinstance(audio, bytes)  # 음성 데이터가 bytes 형식인지 확인
    assert len(audio) > 0  # 음성 데이터가 비어 있지 않은지 확인
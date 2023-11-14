from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.inspection import inspect
import datetime
from database.base import Base
from pydantic import BaseModel
from typing import Optional


class Character(Base):
    __tablename__ = "characters"

    id = Column(String(), primary_key=True, index=True, nullable=False)
    name = Column(String(1024), nullable=False)
    system_prompt = Column(String(262144), nullable=True)
    user_prompt = Column(String(262144), nullable=True)
    text_to_speech_use = Column(String(100), nullable=True)
    voice_id = Column(String(100), nullable=True)
    author_id = Column(String(100), nullable=True)
    data = Column(JSON(), nullable=True)
    created_at = Column(DateTime(), nullable=False)
    updated_at = Column(DateTime(), nullable=False)
    tts = Column(String(64), nullable=True)
    avatar_id = Column(String(100), nullable=True)

    def to_dict(self):
        return {
            # 컬럼 객체의 'key' 속성을 통해 컬럼 이름을 가져옵니다.
            c.key:
            # getattr 함수를 사용하여 해당 컬럼의 값을 가져옵니다.
            # 만약 해당 값이 datetime 객체라면, isoformat 메서드를 호출하여
            # ISO 8601 형식의 문자열로 변환합니다.
                getattr(self, c.key).isoformat() if isinstance(
                    getattr(self, c.key), datetime.datetime) else
                # 값이 datetime 객체가 아니라면, 값을 그대로 사용합니다.
                getattr(self, c.key)
            # inspect 함수를 사용하여 현재 인스턴스의 모든 컬럼 속성을 가져옵니다.
            # 이 반복문은 모든 컬럼을 순회하며 위의 로직을 적용합니다.
            for c in inspect(self).mapper.column_attrs
        }
    def save(self, db):
        db.add(self)
        db.commit()


class CharacterRequest(BaseModel):
    name: str
    system_prompt: Optional[str] = None
    user_prompt: Optional[str] = None
    tts: Optional[str] = None
    voice_id: Optional[str] = None
    data: Optional[dict] = None
    avatar_id: Optional[str] = None


class EditCharacterRequest(BaseModel):
    id: str
    name: Optional[str] = None
    system_prompt: Optional[str] = None
    user_prompt: Optional[str] = None
    text_to_speech_use: Optional[str] = None
    voice_id: Optional[str] = None
    data: Optional[dict] = None
    avatar_id: Optional[str] = None


class DeleteCharacterRequest(BaseModel):
    character_id: str

class GeneratePromptRequest(BaseModel):
    name: str
    background: Optional[str] = None

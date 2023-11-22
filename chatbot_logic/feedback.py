import datetime  # 날짜와 시간을 다루기 위한 기본 라이브러리

from sqlalchemy import Column, String, DateTime, Unicode  # SQLAlchemy에서 사용하는 다양한 데이터 타입과 컬럼을 정의하기 위한 도구
from sqlalchemy.inspection import inspect  # SQLAlchemy 객체의 속성을 조사하기 위한 도구
from pydantic import BaseModel  # Pydantic 라이브러리의 기본 모델, 데이터 유효성 검사에 사용됨
from database.base import Base  # SQLAlchemy의 Declarative Base, 모든 모델의 기본 클래스
from typing import Optional  # 타입 힌팅을 위한 도구, 필드가 선택적임을 나타냄

# 'Feedback' 클래스는 SQLAlchemy 모델로, 데이터베이스의 'feedbacks' 테이블과 매핑됩니다.
class Feedback(Base):
    __tablename__ = "feedbacks"  # 데이터베이스 내의 테이블 이름

    # 다음은 테이블의 컬럼들을 정의한 것입니다. 각 컬럼은 데이터베이스 필드를 나타냅니다.
    message_id = Column(String(64), primary_key=True)  # 메시지 ID, 기본 키로 사용됩니다.
    session_id = Column(String(50), nullable=True)  # 세션 ID, nullable은 이 필드가 비어 있어도 된다는 것을 의미합니다.
    user_id = Column(String(50), nullable=True)  # 사용자 ID
    server_message_unicode = Column(Unicode(65535), nullable=True)  # 서버 메시지, 유니코드 문자를 저장할 수 있습니다.
    feedback = Column(String(100), nullable=True)  # 사용자의 피드백
    comment = Column(Unicode(65535), nullable=True)  # 사용자의 추가 코멘트
    created_at = Column(DateTime(), nullable=False)  # 피드백이 생성된 시간, 필수 필드입니다.

    # 이 메서드는 모델 인스턴스의 데이터를 딕셔너리로 변환하여 반환합니다. 이는 API 응답 등에서 유용하게 사용됩니다.
    def to_dict(self):
        return {
            c.key:
            # 날짜/시간 필드는 ISO 형식의 문자열로 변환됩니다.
            getattr(self, c.key).isoformat() if isinstance(
                getattr(self, c.key), datetime.datetime) else getattr(
                    self, c.key)  # 다른 필드는 그대로 사용됩니다.
            for c in inspect(self).mapper.column_attrs  # 이 반복문은 모든 컬럼 속성을 순회합니다.
        }

    # 이 메서드는 모델 인스턴스를 데이터베이스에 저장합니다.
        def save(self, db):
            db.add(self)
            db.commit()

class FeedbackRequest(BaseModel):
        message_id: str
        session_id: Optional[str] = None
        server_message_unicode: Optional[str] = None
        feedback: Optional[str] = None
        comment: Optional[str] = None


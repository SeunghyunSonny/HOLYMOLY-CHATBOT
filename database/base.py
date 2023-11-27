from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 URL 설정
DATABASE_URL = "sqlite:///./test.db"

# SQLAlchemy 엔진 생성
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델을 위한 베이스 클래스 생성
Base = declarative_base()

# 데이터베이스 세션 제공자 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 모델 정의 (예: User 모델)
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)

# 데이터베이스 스키마 생성
Base.metadata.create_all(bind=engine)